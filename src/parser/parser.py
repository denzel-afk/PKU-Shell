"""
Parser for PKU Shell.

Parses shell command strings into abstract syntax trees (ASTs),
performs globbing expansion, and flattens compound arguments.
Supports quoting, redirection, substitution, and pipelines.
"""

from lark import Lark, Transformer, Tree, Token
import glob
import os

GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), "grammar.lark")
with open(GRAMMAR_FILE, "r") as f:
    shell_grammar = f.read()

shell_parser = Lark(shell_grammar, start="start")


class ASTBuilder(Transformer):
    """Lark transformer to convert parse tree into a custom
    AST dictionary format.
    """

    def start(self, children):
        return Tree('start', children)

    def statement_list(self, stmts):
        return {"type": "statement_list", "statements": stmts}

    def pipeline(self, commands):
        return {"type": "pipeline", "commands": commands}

    def statement(self, pipelines):
        return pipelines[0]

    def command(self, args_and_redirs):
        if not args_and_redirs:
            return {"type": "command", "args": []}

        merged_args = []
        redirections = []
        current = []

        def flush():
            if current:
                if len(current) == 1:
                    merged_args.append(current[0])
                else:
                    merged_args.append({
                        "type": "arg",
                        "value": current.copy()
                    })
                current.clear()

        for item in args_and_redirs:
            if isinstance(item, dict) and item.get("type") in (
                "input_redirection", "output_redirection"
            ):
                flush()
                redirections.append(item)
            elif isinstance(item, dict) and item.get("type") == "substitution":
                flush()
                merged_args.append(item)
            elif isinstance(item, dict) and item.get("type") == "arg":
                current.append(item)
            elif isinstance(item, Token):
                current.append({"type": "arg", "value": str(item)})
            else:
                current.append({"type": "arg", "value": str(item)})

        flush()

        return {
            "type": "command",
            "args": merged_args,
            "redirections": redirections
        }

    def substitution(self, children):
        return {"type": "substitution", "command": children[0]}

    def substitution_backtick(self, children):
        return {
            "type": "substitution",
            "command": children[0],
            "style": "backtick"
        }

    def QUOTED_SINGLE(self, token):
        literal = token[1:-1]
        return {
            "type": "arg",
            "value": bytes(literal, "utf-8").decode("unicode_escape")
        }

    def quoted_double(self, children):
        """Handle content inside double quotes with substitution merging."""
        final = []

        for child in children:
            if isinstance(child, dict):
                if child.get("type") == "substitution":
                    final.append(child)
                elif child.get("type") == "arg":
                    final.append(str(child["value"]))
                else:
                    final.append(str(child))
            elif isinstance(child, Token):
                final.append(str(child))
            else:
                final.append(str(child))

        if all(isinstance(p, str) for p in final):
            return {"type": "arg", "value": "".join(final)}
        else:
            return {"type": "arg", "value": final}

    def input_redirection(self, children):
        return {"type": "input_redirection", "file": str(children[0])}

    def output_redirection(self, children):
        return {"type": "output_redirection", "file": str(children[0])}

    def input_redirection_nospace(self, children):
        val = str(children[0])
        return {"type": "input_redirection", "file": val[1:]}

    def output_redirection_nospace(self, children):
        val = str(children[0])
        return {"type": "output_redirection", "file": val[1:]}


def expand_globs_in_ast(ast):
    """
    Recursively expand glob patterns like *.txt in AST command arguments.
    Handles both current directory and subdirectory patterns.
    """
    if isinstance(ast, dict):
        if ast.get("type") == "command" and "args" in ast:
            args = ast["args"]
            for i, arg in enumerate(args):
                if isinstance(arg, dict) and arg.get("value") == "-name" \
                        and i < len(args) - 1:
                    if isinstance(args[i + 1], dict):
                        args[i + 1]["skip_glob"] = True
                    break

            new_args = []
            for arg in args:
                if isinstance(arg, dict) and "value" in arg \
                        and not arg.get("skip_glob"):
                    val = arg["value"]
                    if isinstance(val, str) and any(
                        c in val for c in ["*", "?", "["]
                    ):
                        if not os.path.isabs(val):
                            if '/' in val or '\\' in val:
                                base_dir, pattern = os.path.split(val)
                                search_path = os.path.join(
                                    os.getcwd(), base_dir
                                )
                            else:
                                search_path = os.getcwd()
                                pattern = val

                            abs_pattern = os.path.join(
                                search_path, pattern
                            )
                            matches = glob.glob(abs_pattern)
                            matches = [
                                os.path.relpath(m, os.getcwd())
                                .replace("\\", "/")
                                for m in sorted(matches)
                            ]

                            if matches:
                                for m in matches:
                                    new_args.append({
                                        "type": "arg",
                                        "value": m
                                    })
                                continue
                        else:
                            matches = glob.glob(val)
                            if matches:
                                for m in sorted(matches):
                                    new_args.append({
                                        "type": "arg",
                                        "value": m
                                    })
                                continue
                new_args.append(arg)
            ast["args"] = new_args

        for key in ast:
            if isinstance(ast[key], (dict, list)):
                expand_globs_in_ast(ast[key])

    elif isinstance(ast, list):
        for item in ast:
            expand_globs_in_ast(item)

    return ast


def flatten_glob_arguments(ast):
    """
    Flatten quoted globbed arguments split into lists,
    respecting skip_glob flag.
    """
    if isinstance(ast, dict):
        if ast.get("type") == "command" and "args" in ast:
            new_args = []
            for arg in ast["args"]:
                if isinstance(arg, dict):
                    val = arg.get("value")
                    if isinstance(val, list) and not arg.get(
                        "skip_glob", False
                    ):
                        for match in val:
                            new_args.append({
                                "type": "arg",
                                "value": match
                            })
                    else:
                        new_args.append(arg)
                else:
                    new_args.append({
                        "type": "arg",
                        "value": str(arg)
                    })
            ast["args"] = new_args

        for key in ast:
            flatten_glob_arguments(ast[key])

    elif isinstance(ast, list):
        for item in ast:
            flatten_glob_arguments(item)
    return ast


def parse_shell_command(line: str):
    """
    Parse a shell command string into an AST with glob expansion.

    Args:
        line (str): The shell command string.

    Returns:
        dict: The final abstract syntax tree.
    """
    parse_tree = shell_parser.parse(line)
    ast = ASTBuilder().transform(parse_tree)
    if hasattr(ast, "data") and ast.data == "start":
        ast = ast.children[0]
    ast = expand_globs_in_ast(ast)
    ast = flatten_glob_arguments(ast)
    return ast

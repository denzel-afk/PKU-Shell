import os
import io
from typing import List, Dict, Any, Union
from apps.registry import AppRegistry


class ExecutionContext:
    """Maintains shell execution state including working directory and IO."""
    def __init__(self):
        self.working_dir = os.getcwd()
        self.stdin = None
        self.stdout = None
        self.stderr = None
        self.env = os.environ.copy()
        self.pipeline_position = 0
        self.pipeline_total = 1
        self.last_exit_status = 0

    def change_directory(self, path: str):
        """Change directory with validation"""
        new_path = os.path.abspath(os.path.join(self.working_dir, path))
        if not os.path.isdir(new_path):
            raise FileNotFoundError(f"Directory not found: {new_path}")
        self.working_dir = new_path
        os.chdir(new_path)

    def resolve_path(self, path: str) -> str:
        """Resolve relative paths against current directory"""
        if os.path.isabs(path):
            return path
        return os.path.join(self.working_dir, path)


def evaluate_arg(
    arg: Dict[str, Any],
    context: ExecutionContext
) -> Union[str, List[str]]:
    """Evaluate command arguments and substitutions."""
    if arg["type"] == "arg":
        val = arg["value"]
        if isinstance(val, list):
            evaluated = []
            for v in val:
                if isinstance(v, dict):
                    ev = evaluate_arg(v, context)
                    if isinstance(ev, list):
                        evaluated.extend(ev)
                    else:
                        evaluated.append(str(ev))
                else:
                    evaluated.append(str(v))
            return "".join(evaluated).strip()
        elif isinstance(val, dict):
            ev = evaluate_arg(val, context)
            return ev if isinstance(ev, str) else str(ev)
        else:
            return str(val)

    elif arg["type"] == "substitution":
        sub_out = []
        execute_ast(arg["command"], sub_out, context)
        result = "".join(sub_out).strip()
        return result.replace("\n", " ")

    raise ValueError(f"Unhandled argument type: {arg['type']}")


def run_command(
    cmd_name: str,
    cmd_args: List[str],
    context: ExecutionContext
):
    """Execute a single command with given arguments."""
    try:
        app = AppRegistry.get(cmd_name)

        input_content = context.stdin.read() if context.stdin else None
        result = app.run(cmd_args, stdin=input_content)

        if isinstance(result, dict) and result.get("action") == "chdir":
            context.change_directory(result["target"])
            return 0

        return result

    except Exception as e:
        raise Exception(f"Error executing {cmd_name}: {str(e)}")


def run_pipeline(
    pipeline_ast: Dict[str, Any],
    context: ExecutionContext
) -> str:
    """Execute pipeline of commands connected with |."""
    commands = pipeline_ast.get("commands", [])
    if not commands:
        return ""

    context.pipeline_total = len(commands)
    input_stream = context.stdin or io.StringIO()
    final_output = io.StringIO()

    for i, cmd in enumerate(commands):
        context.pipeline_position = i
        output_stream = io.StringIO() if i < len(commands)-1 else final_output

        cmd_context = ExecutionContext()
        cmd_context.working_dir = context.working_dir
        cmd_context.stdin = input_stream
        cmd_context.stdout = output_stream
        cmd_context.stderr = context.stderr
        cmd_context.env = context.env.copy()

        execute_call(cmd, [], cmd_context)

        if i < len(commands)-1:
            input_stream = io.StringIO(output_stream.getvalue())

    return final_output.getvalue()


from executor.redirection import RedirectionHandler  # noqa: E402


def execute_call(
    call_ast: Dict[str, Any],
    out: List[str],
    context: ExecutionContext
):
    """Execute a command call with potential redirections."""
    redir_handler = RedirectionHandler(call_ast, context)
    redir_handler.setup_redirections()
    context.stdin = redir_handler.get_input_stream()
    context.stdout = redir_handler.get_output_stream()

    args = []
    for arg in call_ast.get("args", []):
        if (isinstance(arg, dict) and
                arg.get("type") in
                ["input_redirection", "output_redirection"]):
            continue
        val = evaluate_arg(arg, context)
        args.extend(val) if isinstance(val, list) else args.append(val)

    if not args:
        redir_handler.cleanup()
        return

    cmd_name = args[0]
    cmd_args = args[1:]

    try:
        result = run_command(cmd_name, cmd_args, context)
        if context.stdout and result:
            context.stdout.write(str(result))
    finally:
        redir_handler.cleanup()


def execute_sequence(
    sequence_ast: Dict[str, Any],
    out: List[str],
    context: ExecutionContext
):
    """Execute commands in sequence (separated by ;)."""
    for cmd in sequence_ast.get("commands", []):
        try:
            if cmd.get("type") == "call":
                execute_call(cmd, out, context)
            elif cmd.get("type") == "pipeline":
                result = run_pipeline(cmd, context)
                if result and out is not None:
                    out.append(result)
            else:
                err_msg = f"Unknown command type in sequence:{cmd.get('type')}"
                raise ValueError(err_msg)
        except Exception:
            out.clear()
            break


def execute_ast(
    ast: Dict[str, Any],
    out: List[str],
    context: ExecutionContext
):
    """Main entry point for executing parsed AST."""
    if hasattr(ast, "data") and ast.data == "start":
        ast = ast.children[0]

    if ast.get("type") != "statement_list":
        raise ValueError("AST root must be statement_list")

    for stmt in ast.get("statements", []):
        if stmt.get("type") == "pipeline":
            result = run_pipeline(stmt, context)
            if result and out is not None:
                out.append(result)
        elif stmt.get("type") == "sequence":
            execute_sequence(stmt, out, context)
        elif stmt.get("type") == "call":
            execute_call(stmt, out, context)
        else:
            raise ValueError(f"Unknown statement type: {stmt.get('type')}")

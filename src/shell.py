"""
Main shell entry point for PKU Shell.

Parses and evaluates command lines using custom parser, executor,
and application loader. Supports both interactive and non-interactive modes.
"""

import sys
import os
import io
from collections import deque
from parser.parser import parse_shell_command
from apps.loader import load_all_apps
from executor.executor import execute_ast, ExecutionContext


load_all_apps()


def eval(cmdline, out, stdin=None):
    """
    Evaluate a shell command line.

    Args:
        cmdline (str): The command line input to evaluate.
        out (deque): Output deque to store result lines.
        stdin (str, optional): Simulated input (for piping or redirection).

    Handles parsing, execution, and contextual stdin setup.
    Clears output for pipeline or semicolon errors.
    Appends error messages otherwise.
    """
    try:
        ast = parse_shell_command(cmdline)
        context = ExecutionContext()

        if stdin:
            context.stdin = io.StringIO(stdin)

        execute_ast(ast, out, context)

    except Exception as e:
        if "|" in cmdline or ";" in cmdline:
            out.clear()
        else:
            out.append(f"Error: {e}\n")


if __name__ == "__main__":
    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2 or sys.argv[1] != "-c":
            raise ValueError("Usage: python shell.py -c \"command\"")

        out = deque()
        eval(sys.argv[2], out)
        while out:
            print(out.popleft(), end="")

    else:
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()
            out = deque()
            eval(cmdline, out)
            while out:
                print(out.popleft(), end="")

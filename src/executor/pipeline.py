"""
Pipeline Executor for PKU Shell.

Implements the pipe (`|`) operator by connecting the output of one command
to the input of the next, using in-memory IO streams.
"""

from typing import List, Dict, Any
import io
from executor.executor import ExecutionContext, execute_call


class PipelineExecutor:
    """
    Implements the pipe operator (`|`) using the Chain of
    Responsibility pattern.

    This class connects multiple commands in a pipeline such that the
    output of one command becomes the input of the next.
    """

    def __init__(self):
        """Initialize an empty pipeline."""
        self.commands = []

    def add_command(self, command: Dict[str, Any]):
        """
        Add a command AST node to the pipeline.

        Args:
            command (Dict[str, Any]): A parsed command node from the AST.
        """
        self.commands.append(command)

    def execute(self, out: List[str], context: ExecutionContext):
        """
        Execute the full pipeline of commands.

        Steps:
        1. Use StringIO buffers to pipe output -> input.
        2. Preserve working directory and environment variables.
        3. Collect only the final output in the output list.

        Args:
            out (List[str]): Output list to collect final result.
            context (ExecutionContext): Global execution context.
        """
        if not self.commands:
            return

        # Initial input comes from provided context or empty stream
        input_stream = context.stdin or io.StringIO()

        for i, cmd in enumerate(self.commands):
            # Create a new execution context per command
            cmd_context = ExecutionContext()
            cmd_context.working_dir = context.working_dir
            cmd_context.stdin = input_stream
            cmd_context.env = context.env.copy()

            output_stream = io.StringIO()
            cmd_context.stdout = output_stream

            execute_call(cmd, out, cmd_context)

            # Final command: collect output
            if i == len(self.commands) - 1:
                out.append(output_stream.getvalue())
            else:
                input_stream = io.StringIO(output_stream.getvalue())

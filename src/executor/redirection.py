"""
Redirection handler for PKU Shell.

Provides input (`<`) and output (`>`) redirection logic
using the Decorator design pattern on the execution context.
"""

import os
from typing import Dict, Any, Optional, TextIO
from executor.executor import ExecutionContext


class RedirectionHandler:
    """
    Handles input/output redirection using the Decorator pattern.

    Responsible for managing file opening and closing based on redirection
    operators in the command AST.
    """

    def __init__(self, command: Dict[str, Any], context: ExecutionContext):
        """
        Initialize a redirection handler.

        Args:
            command (Dict[str, Any]): The AST node representing the command.
            context (ExecutionContext): Current execution context.
        """
        self.command = command
        self.context = context
        self.input_file: Optional[TextIO] = None
        self.output_file: Optional[TextIO] = None

    def setup_redirections(self):
        """
        Set up all redirections defined in the command AST.

        This includes opening files for input (`<`) and output (`>`).
        """
        for redir in self.command.get("redirections", []):
            if redir["type"] == "input_redirection":
                self._setup_input_redirection(redir["file"])
            elif redir["type"] == "output_redirection":
                self._setup_output_redirection(redir["file"])

    def _setup_input_redirection(self, file_path: str):
        """
        Set up input redirection (<) by opening the input file.

        Args:
            file_path (str): Path to the file to read from.

        Raises:
            FileNotFoundError: If the input file does not exist.
        """
        resolved_path = self.context.resolve_path(file_path)
        if not os.path.exists(resolved_path):
            raise FileNotFoundError(f"Input file not found: {resolved_path}")
        self.input_file = open(resolved_path, 'r')

    def _setup_output_redirection(self, file_path: str):
        """
        Set up output redirection (>) by opening the output file.

        Args:
            file_path (str): Path to the file to write to.
        """
        resolved_path = self.context.resolve_path(file_path)
        self.output_file = open(resolved_path, 'w')

    def get_input_stream(self):
        """
        Get the effective input stream for the command.

        Returns:
            TextIO or None: Input file stream if redirected,
            otherwise stdin from context.
        """
        return self.input_file if self.input_file else self.context.stdin

    def get_output_stream(self):
        """
        Get the effective output stream for the command.

        Returns:
            TextIO or None: Output file stream if redirected,
            otherwise stdout from context.
        """
        return self.output_file if self.output_file else self.context.stdout

    def cleanup(self):
        """
        Close any opened redirection file handles.
        """
        if self.input_file:
            self.input_file.close()
        if self.output_file:
            self.output_file.close()

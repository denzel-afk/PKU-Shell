from apps.base import BaseApp
from apps.registry import AppRegistry
import fnmatch
import os


class FindApp(BaseApp):
    """
    Application that implements the behavior of the Unix
    `find` command with `-name`.

    Allows searching for files that match a pattern under
    a given directory.
    """

    def run(self, args, stdin=None):
        """
        Execute the find command with a path and -name pattern.

        Args:
            args (List[str]): Arguments including optional path
            and required `-name` [pattern].
            stdin (str, optional): Ignored.

        Returns:
            str: Matching file paths, each on a new line.

        Raises:
            ValueError: If arguments are missing or
            path is invalid.
        """
        if not args or "-name" not in args:
            raise ValueError(
                "find: invalid arguments. "
                "Usage: find [path] -name [pattern]"
            )

        try:
            name_index = args.index("-name")
            pattern_arg = args[name_index + 1]
            pattern = (
                pattern_arg.get("value", "")
                if isinstance(pattern_arg, dict)
                else pattern_arg
            )
        except IndexError:
            raise ValueError(
                "find: missing pattern after -name. "
                "Usage: find [path] -name [pattern]"
            )

        path_arg = args[0] if name_index != 0 else "."
        path = (
            path_arg.get("value", "")
            if isinstance(path_arg, dict)
            else path_arg
        )

        if not os.path.isdir(path):
            raise ValueError(f"find: {path}: No such directory")

        return self.find_files(path, pattern)

    def find_files(self, path, pattern):
        """
        Traverse the file tree starting from `path` and match files
        using the pattern.

        Args:
            path (str): Root directory to begin the search.
            pattern (str): Glob pattern to match filenames.

        Returns:
            str: Relative paths of matched files, each on a separate line.
        """
        result = []
        for root, dirs, files in os.walk(path):
            for filename in files:
                if fnmatch.fnmatch(filename, pattern):
                    full_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(
                        full_path, start=path
                    ).replace("\\", "/")
                    if path == ".":
                        result.append(f"./{rel_path}")
                    else:
                        result.append(
                            os.path.join(path, rel_path).replace("\\", "/")
                        )
        return "\n".join(result)


AppRegistry.register("find", FindApp)

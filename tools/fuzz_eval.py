"""
Advanced Fuzzer for PKU Shell

This script generates randomized shell commands and optional stdin content to
test the shell for crashes or unexpected behavior.

It logs failures and provides a summary at the end.
"""

import sys
import os
import random
import string
from collections import deque
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../src")))

from shell import eval  # noqa: E402

random.seed(42)

SPECIAL_PATTERNS = [
    'echo "unterminated',
    "echo 'nested `echo test`'",
    "cat < missing.txt",
    "sort | grep a",
    "echo `echo \";\"`",
    "uniq -x file.txt",
    "ls *.py",
    "echo a'b\"c",
    "`echo echo` foo",
    "head -n 1000000000"
]


def random_command():
    """
    Generate a random shell command with fuzzed arguments.
    """
    base_cmds = [
        'echo', 'cat', 'grep', 'ls', 'sort', 'uniq', 'wc', 'head', 'tail']
    if random.random() < 0.3:
        return random.choice(SPECIAL_PATTERNS)
    cmd = random.choice(base_cmds)
    arg = ''.join(random.choices(
        string.printable, k=random.randint(3, 25)))
    return f"{cmd} {arg}".strip()


def random_stdin():
    """
    Optionally generate random stdin content.
    """
    if random.random() < 0.5:
        return None
    return ''.join(random.choices(
        string.printable, k=random.randint(5, 50)))


def fuzz_once():
    """
    Generate and run one fuzzing attempt.
    Returns True if successful, False if a crash occurs.
    """
    cmd = random_command()
    stdin_data = random_stdin()
    out = deque()

    try:
        eval(cmd, out, stdin=stdin_data)
        print(f"[OK] {cmd}")
        return True
    except Exception as e:
        log_crash(cmd, stdin_data, e)
        print(f"[CRASH] {cmd}\n→ {type(e).__name__}: {e}")
        return False


def log_crash(command, stdin_data, exception):
    """
    Log crash details to fuzz_crashes.log
    """
    with open("fuzz_crashes.log", "a") as f:
        f.write(f"\n[{datetime.now()}] CRASH\n")
        f.write(f"Command: {command}\n")
        if stdin_data:
            f.write(f"Stdin: {repr(stdin_data)}\n")
        f.write(f"Error: {type(exception).__name__}: {exception}\n")


if __name__ == "__main__":
    total = 100
    success, fail = 0, 0

    print("=== Starting Fuzz Test ===\n")
    for _ in range(total):
        if fuzz_once():
            success += 1
        else:
            fail += 1

    print("\n=== Fuzzing Done ===")
    print(f"✅ Success: {success}")
    print(f"❌ Crashes: {fail}")
    print("📝 Crash log saved to fuzz_crashes.log")

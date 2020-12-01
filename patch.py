#!/usr/bin/env python3
from sparkles import get_stdout_lines

import os
import sys


def needs_a_commit():
    status_lines = get_stdout_lines(["git", "status"])
    return "nothing to commit, working tree clean" not in status_lines


def get_commit_message():
    args_contain_commit_message = len(sys.argv) == 1

    commit_message = (
        get_commit_message_interactive()
        if args_contain_commit_message
        else get_commit_message_from_arguments()
    )

    return escape_quotes_for_bash(commit_message)


def get_commit_message_interactive():
    return input("Commit message? ")


def get_commit_message_from_arguments():
    return " ".join(sys.argv[1:])


def escape_quotes_for_bash(bash_line):
    return bash_line.replace("'", "'\\''")


def commit_changes():
    os.system("git add .")
    os.system(f'git commit -m "{get_commit_message()}"')


def bump_version():
    os.system("bump2version patch")
    os.system("git push")


def publish():
    os.system("flit publish")


if __name__ == "__main__":
    if needs_a_commit():
        commit_changes()
    bump_version()
    publish()

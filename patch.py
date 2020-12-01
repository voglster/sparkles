#!/usr/bin/env python3
from sparkles import get_stdout_lines

import os
import sys


def need_to_commit():
    status_lines = get_stdout_lines(["git", "status"])
    return "nothing to commit, working tree clean" not in status_lines


def get_commit_message():
    commit_msg_in_args = len(sys.argv) > 1

    commit_message = (
        get_commit_message_from_arguments()
        if commit_msg_in_args
        else ask_user_for_commit_message()
    )

    return escape_quotes_for_bash(commit_message)


def ask_user_for_commit_message():
    return input("Commit message? ")


def get_commit_message_from_arguments():
    return " ".join(sys.argv[1:])


def escape_quotes_for_bash(bash_line):
    return bash_line.replace("'", "'\\''")


def commit_changes(commit_message):
    os.system("git add .")
    os.system(f'git commit -m "{commit_message}"')


def bump_version():
    os.system("bump2version patch")
    os.system("git push")


def publish():
    os.system("flit publish")


if __name__ == "__main__":
    if need_to_commit():
        commit_changes(get_commit_message())
    bump_version()
    publish()

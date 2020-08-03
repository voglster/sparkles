#!/usr/bin/env python3

import os
import sys

if len(sys.argv) == 1:
    commit_message = input("Commit message? ")
else:
    commit_message = " ".join(sys.argv[1:])

clean_commit_message = commit_message.replace("'", "'\\''")

os.system("git add .")
os.system(f'git commit -m "{clean_commit_message}"')
os.system("bump2version patch")
os.system("git push")

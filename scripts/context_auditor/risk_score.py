#!/usr/bin/env python3
"""Simple regex-based risk scoring."""
import re, argparse, pathlib

DANGER_PATTERNS = [
    re.compile(r'\bDO NOT\b', re.I),
    re.compile(r'\bmust refuse\b', re.I),
    re.compile(r'\bdisallowed content\b', re.I),
]

def score(diff_text):
    removed_lines = [l[1:] for l in diff_text.splitlines() if l.startswith('-')]
    for line in removed_lines:
        for pat in DANGER_PATTERNS:
            if pat.search(line):
                return "HIGH"
    return "LOW"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('diff_md')
    args = parser.parse_args()
    diff = pathlib.Path(args.diff_md).read_text()
    print(score(diff))

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""Offline summarizer: extracts first N changed lines."""
import argparse, pathlib

def summarize(diff_text, max_lines=40):
    lines = [l for l in diff_text.splitlines() if l.startswith(('+', '-'))]
    return '\n'.join(lines[:max_lines])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()

    p = pathlib.Path(args.input)
    diff_md = p.read_text()
    summary = summarize(diff_md)
    p.write_text(diff_md + "\n\n### Summary\n```
" + summary + "\n```\n")
    print("[context-auditor] summary appended")

if __name__ == "__main__":
    main()
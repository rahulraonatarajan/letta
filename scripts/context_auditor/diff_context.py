#!/usr/bin/env python3
"""Generate a diff of contextual files and write markdown report."""
import argparse, subprocess, yaml, pathlib, datetime, fnmatch

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def git_diff():
    try:
        diff = subprocess.check_output(["git", "diff", "--unified=0", "HEAD~1", "HEAD"], text=True)
    except subprocess.CalledProcessError as e:
        diff = e.output
    return diff

def filter_diff(diff, globs, ignores):
    lines = diff.splitlines()
    keep = []
    current_file = None
    keep_file = False
    for line in lines:
        if line.startswith('diff --git'):
            parts = line.split(' b/')
            current_file = parts[1] if len(parts) >= 2 else None
            keep_file = any(fnmatch.fnmatch(current_file, g) for g in globs) and not any(fnmatch.fnmatch(current_file, ig) for ig in ignores)
        if keep_file:
            keep.append(line)
    return '\n'.join(keep)

def write_report(diff, out_path):
    ts = datetime.datetime.utcnow().isoformat(timespec='seconds')
    md = f"## Context Diff — {ts} UTC\n```diff\n{diff}\n```\n"
    pathlib.Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out_path).write_text(md)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    cfg = load_config(args.config)
    raw = git_diff()
    filtered = filter_diff(raw, cfg.get('watch_globs', []), cfg.get('ignore_globs', []))
    write_report(filtered, args.output)
    print(f"[context-auditor] diff written to {args.output}")

if __name__ == "__main__":
    main()
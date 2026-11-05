#!/usr/bin/env python3
"""Check project Markdown without third-party dependencies."""
from pathlib import Path
import os
import re
import sys
from urllib.parse import unquote, urlsplit


def main():
    root = Path(__file__).resolve().parents[1]
    errors = []
    # Prune caches and temporary clones; also works from the ZIP without Git.
    excluded = {'.git', 'tmp', 'output', '.venv', 'node_modules', '__pycache__', '.pytest_cache'}
    files = []
    for directory, subdirs, names in os.walk(root):
        subdirs[:] = [name for name in subdirs if name not in excluded]
        files.extend(Path(directory) / name for name in names if name.endswith('.md'))
    files.sort()
    for path in files:
        relative = path.relative_to(root)
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            errors.append(f'{relative}: invalid UTF-8')
            continue
        if '\ufffd' in text:
            errors.append(f'{relative}: Unicode replacement character')
        if re.search(r'\[cite:\s*[\d, ]+\]', text):
            errors.append(f'{relative}: unresolved citation placeholder')
        if re.search(r'^(<<<<<<< |=======\s*$|>>>>>>> )', text, re.M):
            errors.append(f'{relative}: unresolved merge conflict')
        fence = None
        for line_number, line in enumerate(text.splitlines(), 1):
            marker = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line)
            if marker:
                mark, rest = marker.groups()
                if fence is None:
                    fence = mark
                elif mark[0] == fence[0] and len(mark) >= len(fence) and not rest.strip():
                    fence = None
                continue
            if fence:
                continue
            # Inline code contains example paths, not actual links.
            visible = re.sub(r'`[^`]*`', '', line)
            for match in re.finditer(r'!?\[[^\]]*\]\(<?([^\s)>]+)>?(?:\s+"[^"]*")?\)', visible):
                href = match.group(1)
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target = (path.parent / unquote(parsed.path)).resolve()
                if not target.exists():
                    errors.append(f'{relative}:{line_number}: missing link target: {href}')
        if fence:
            errors.append(f'{relative}: unclosed fenced code block')
    checklist = root / 'tasks-assignment.md'
    if checklist.exists():
        ids = re.findall(r'^- \[[ xX]\] \*\*(W\d+-TV\d+-\d+)\*\*', checklist.read_text(encoding='utf-8'), re.M)
        if len(ids) != len(set(ids)):
            errors.append('tasks-assignment.md: duplicate task IDs')
        expected = {f'W{week}-TV{member}-{task:02d}'
                    for week in range(1, 5) for member in range(1, 6) for task in range(1, 6)}
        if set(ids) != expected:
            errors.append('tasks-assignment.md: expected all 100 assigned task IDs')
        status = root / 'docs/00-management/completion-status.md'
        if status.exists():
            status_ids = re.findall(r'^\| (W\d+-TV\d+-\d+) \|', status.read_text(encoding='utf-8'), re.M)
            if len(status_ids) != len(set(status_ids)) or set(status_ids) != expected:
                errors.append('completion-status.md: task rows must match the 100 assigned tasks')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'OK: {len(files)} Markdown files; UTF-8, local links, code fences and task IDs checked.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

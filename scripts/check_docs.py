#!/usr/bin/env python3
"""Check project Markdown without third-party dependencies."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def main():
    root = Path(__file__).resolve().parents[1]
    errors = []
    files = sorted(p for p in root.rglob('*.md') if '.git' not in p.parts)
    for path in files:
        relative = path.relative_to(root)
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            errors.append(f'{relative}: invalid UTF-8')
            continue
        if '\ufffd' in text:
            errors.append(f'{relative}: Unicode replacement character')
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
        ids = re.findall(r'^- \[[ xX]\] \*\*(W\d+-TV\d+-\d+)\*\*', checklist.read_text(), re.M)
        if len(ids) != len(set(ids)):
            errors.append('tasks-assignment.md: duplicate task IDs')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'OK: {len(files)} Markdown files; UTF-8, local links, code fences and task IDs checked.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

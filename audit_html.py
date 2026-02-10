import os

file_path = 'index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Search for style=
for i, line in enumerate(lines):
    if 'style=' in line:
        print(f"L{i+1}: Style found: {line.strip()}")

# Search for interactive without title
interactive = ['<button', '<select', '<a ']
for i, line in enumerate(lines):
    for tag in interactive:
        if tag in line:
            if 'title=' not in line and 'title =' not in line:
                # Check next line if it's multiline
                if '>' not in line or 'title=' not in lines[i+1]:
                     print(f"L{i+1}: Interactive without title: {line.strip()}")

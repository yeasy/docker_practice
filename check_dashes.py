import os
import re

count = 0
for root, dirs, files in os.walk("/Users/baohua/Github/books/docker_practice"):
    if ".git" in root or "node_modules" in root:
        continue
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                # match optional spaces, then exactly one dash, then no space and no dash
                m = re.match(r'^(\s*)-([^- \t\n].*)$', line)
                if m:
                    print(f"{filepath}:{i+1}:{line.rstrip()}")
                    count += 1

print(f"Total found: {count}")

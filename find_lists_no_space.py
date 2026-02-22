import os
import re

count = 0
for root, _, files in os.walk("/Users/baohua/Github/books/docker_practice"):
    if ".git" in root or "node_modules" in root: continue
    for f in files:
        if f.endswith(".md"):
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
            except Exception:
                continue
                
            in_code_block = False
            for i, line in enumerate(lines):
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    continue
                
                if not in_code_block:
                    # Look for lines starting with space(s) and a single dash, followed by word char, * or _
                    # skip html comment '<!--' or horizontal rule '---' or yaml '---'
                    m = re.match(r'^(\s*)-([*_\w\u4e00-\u9fa5].*)$', line)
                    if m:
                        print(f"{path}:{i+1}:{line.rstrip()}")
                        count += 1
                        if count > 50:
                            print("More than 50 found. Stopping.")
                            import sys
                            sys.exit(0)

print(f"Total outside code blocks: {count}")

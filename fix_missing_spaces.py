import os
import re

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    in_code_block = False
    in_frontmatter = False
    changed = False

    for i in range(len(lines)):
        line = lines[i]
        
        # Checking for yaml frontmatter
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter and line.strip() == "---":
            in_frontmatter = False
            continue
        if in_frontmatter:
            continue
        
        # Checking for code block
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
            
        if not in_code_block:
            # We want to find lines like:
            # -foo
            # -**bold**
            # Match optional whitespace, then a single dash, then something not space, not -, not <
            m = re.match(r'^(\s*)-([^\s\-<].*)$', line)
            if m:
                # To distinguish from command line arguments like -p or -v which might legitimately appear outside code blocks 
                # (though usually they shouldn't), let's be careful. The user specifically asked to fix all list symbols -.
                # We will just insert a space.
                new_line = m.group(1) + "- " + m.group(2) + "\n"
                lines[i] = new_line
                changed = True

    if changed:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"Fixed: {filepath}")
        except Exception as e:
            print(f"Error writing {filepath}: {e}")

count = 0
for root, dirs, files in os.walk("/Users/baohua/Github/books/docker_practice"):
    # ALWAYS modify dirs in-place to prevent os.walk from entering them
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "dist", "build")]
    
    for file in files:
        if file.endswith(".md"):
            process_file(os.path.join(root, file))

print("Done fixing.")


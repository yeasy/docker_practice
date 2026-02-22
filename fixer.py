import os
import re

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Could not read file {filepath}: {e}")
        return False
        
    if not lines:
        return False

    new_lines = []
    in_code_block = False
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Code block tracking
        if line_stripped.startswith('```'):
            in_code_block = not in_code_block
            
        # 1. Full-width parentheses `（` `）`
        # We replace them with space + half-width parenthesis except if it's already spaced
        if not in_code_block and ('（' in line or '）' in line):
             # Replace left parenthesis
             line = re.sub(r'([^\s])（', r'\1 (', line)
             line = re.sub(r'\s*（', r' (', line)
             # Replace right parenthesis
             line = re.sub(r'）([^\s.,;?!:，。；？！：])', r') \1', line)
             line = re.sub(r'）\s*', r')', line)
             
             # Also a quick hack to replace any leftover （ ）
             line = line.replace('（', '(').replace('）', ')')

        # 3. Missing blank line before list item
        is_list_item = re.match(r'^(\s*[-*+]\s|\s*\d+\.\s)', line)
        if not in_code_block and is_list_item and i > 0:
            prev_line = lines[i-1]
            prev_line_stripped = prev_line.strip()
            
            # If prev line is not empty, and not already a list item, header, quote, HTML, or table
            if prev_line_stripped and not prev_line_stripped.startswith('#') and not prev_line_stripped.startswith('>'):
                if not re.match(r'^(\s*[-*+]\s|\s*\d+\.\s)', prev_line) and not prev_line_stripped.startswith('<!--') and not prev_line_stripped.startswith('|'):
                    # Insert a blank line
                    if new_lines and new_lines[-1] != '\n':
                        new_lines.append('\n')

        new_lines.append(line)
        
        # 2. Missing intro text after headers
        if not in_code_block and line_stripped.startswith('#') and not line_stripped.startswith('# '):
           pass # might be a comment in code, but we already handled code blocks. Should be a real header.
        
        if not in_code_block and re.match(r'^#{1,6}\s', line):
            # Check what comes next
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines):
                next_line = lines[j].strip()
                if next_line.startswith('```'):
                    new_lines.append('\n示例代码如下：\n')
                elif next_line.startswith('|') and len(next_line.split('|')) > 2:
                    new_lines.append('\n相关信息如下表：\n')
                elif next_line.startswith('!['):
                    new_lines.append('\n相关图示如下：\n')
                    
    # Only keep one EOF newline
    while len(new_lines) > 1 and new_lines[-1] == '\n' and new_lines[-2] == '\n':
        new_lines.pop()

    # Make sure text ends with newline
    if new_lines and not new_lines[-1].endswith('\n') and getattr(new_lines[-1], "endswith", None):
        if new_lines[-1] != "":
            new_lines[-1] += '\n'

    # Did anything change?
    if new_lines != lines:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return True
        except Exception as e:
            print(f"Could not write file {filepath}: {e}")
            return False
    return False

def main():
    summary_path = 'SUMMARY.md'
    if not os.path.exists(summary_path):
        print(f"Error: {summary_path} not found in {os.getcwd()}")
        return
        
    with open(summary_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    md_files = re.findall(r'\(([^)]*\.md)\)', content)
    md_files = list(dict.fromkeys(md_files))
    
    fixed_count = 0
    
    for md_file in md_files:
        filepath = os.path.join(os.path.dirname(summary_path), md_file)
        if os.path.exists(filepath):
            if fix_file(filepath):
                print(f"Fixed: {md_file}")
                fixed_count += 1
                
    print(f"\nTotal files fixed: {fixed_count}")

if __name__ == '__main__':
    main()

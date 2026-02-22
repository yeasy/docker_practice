import os
import re

def check_file(filepath):
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return [f"Could not read file: {e}"]
        
    in_code_block = False
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Code block tracking
        if line_stripped.startswith('```'):
            in_code_block = not in_code_block
            
        if in_code_block:
            continue
            
        # 1. Full-width parentheses `（` `）`
        if '（' in line or '）' in line:
            if line_stripped.startswith('#'):
                issues.append(f"Line {i+1}: Header contains full-width parentheses '（' or '）'")
            else:
                issues.append(f"Line {i+1}: Text contains full-width parentheses '（' or '）'")
                
        # 2. Missing intro text after headers
        if line_stripped.startswith('#'):
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines):
                next_line = lines[j].strip()
                if next_line.startswith('```'):
                    issues.append(f"Line {i+1}: Header immediately followed by code block without text")
                elif next_line.startswith('|') and len(next_line.split('|')) > 2:
                    issues.append(f"Line {i+1}: Header immediately followed by table without text")
                elif next_line.startswith('#') and next_line.count('#') == line_stripped.count('#') + 1:
                    issues.append(f"Line {i+1}: Header immediately followed by sub-header (missing text between)")
                elif next_line.startswith('!['):
                    issues.append(f"Line {i+1}: Header immediately followed by image without text")

        # 3. Missing blank line before list item
        # Is this line a list item?
        is_list_item = re.match(r'^(\s*[-*+]\s|\s*\d+\.\s)', line)
        if is_list_item and i > 0:
            prev_line = lines[i-1]
            prev_line_stripped = prev_line.strip()
            
            # If prev line is not empty, and not already a list item, header, quote, or HTML comment
            if prev_line_stripped and not prev_line_stripped.startswith('#') and not prev_line_stripped.startswith('>'):
                if not re.match(r'^(\s*[-*+]\s|\s*\d+\.\s)', prev_line) and not prev_line_stripped.startswith('<!--') and not prev_line_stripped.startswith('|'):
                    issues.append(f"Line {i+1}: Missing blank line before list item")
                    
    # Check EOF newlines
    if set(lines) == {'\n'}:
        pass
    elif len(lines) > 0 and not lines[-1].endswith('\n') and not lines[-1] == '':
         # Note: file.read().splitlines() drops the last empty lines, so simple ends with '\n' might be enough
         pass
    if len(lines) > 1 and lines[-1] == '\n' and lines[-2] == '\n':
         issues.append("EOF: Multiple empty lines at end of file")

    return issues

def main():
    summary_path = 'SUMMARY.md'
    if not os.path.exists(summary_path):
        print(f"Error: {summary_path} not found in {os.getcwd()}")
        return
        
    with open(summary_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all .md files in SUMMARY.md
    md_files = re.findall(r'\(([^)]*\.md)\)', content)
    md_files = list(dict.fromkeys(md_files)) # deduplicate
    
    total_issues = 0
    
    summary_out = open('format_report.txt', 'w', encoding='utf-8')
    
    for md_file in md_files:
        filepath = os.path.join(os.path.dirname(summary_path), md_file)
        if os.path.exists(filepath):
            issues = check_file(filepath)
            if issues:
                print(f"--- {md_file} ---")
                summary_out.write(f"--- {md_file} ---\n")
                for issue in issues:
                    print(issue)
                    summary_out.write(issue + "\n")
                print()
                summary_out.write("\n")
                total_issues += len(issues)
        else:
            print(f"Warning: File not found {filepath}")
            
    summary_out.write(f"Total issues found: {total_issues}\n")
    summary_out.close()
    
    print(f"Total issues found: {total_issues}. Report saved to format_report.txt.")

if __name__ == '__main__':
    main()

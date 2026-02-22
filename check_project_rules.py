import os
import re
import argparse

def check_file(filepath, verbose=False):
    violations = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    filename = os.path.basename(filepath)
    is_readme = filename.lower() == 'readme.md'
    is_summary = filename.lower() == 'summary.md'
    is_section = re.match(r'^\d+\.\d+_.*\.md$', filename)

    # 1.1 Bold Text: No spaces inside the bold markers
    for i, line in enumerate(lines):
        if '** ' in line or ' **' in line:
            # We must be careful: '** ' might be a bold start with space inside, but it could also be regular text.
            # Let's use a simpler, line-bound regex line by line
            if re.search(r'\*\*\s+[^*]+\*\*|\*\*[^*]+\s+\*\*', line):
                violations.append(f"1.1 Bold Text: Space inside bold markers at line {i+1}")

    # 1.4 Trailing Newline
    if not content.endswith('\n') or content.endswith('\n\n'):
        if content: # ignore empty files
            violations.append("1.4 Trailing Newline: File must end with exactly one newline character")

    headers = []
    for i, line in enumerate(lines):
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text = m.group(2)
            headers.append({'line': i, 'level': level, 'text': text})
            
            # 1.2 Header Spacing
            if i + 1 < len(lines):
                next_line = lines[i+1].strip()
                if next_line != '':
                    violations.append(f"1.2 Header Spacing: Header at line {i+1} not followed by a blank line")
            if i + 2 < len(lines):
                if lines[i+1].strip() == '' and lines[i+2].strip() == '':
                    violations.append(f"1.2 Header Spacing: Header at line {i+1} followed by multiple blank lines")

    # 1.3 Header Hierarchy
    for j in range(len(headers) - 1):
        curr_level = headers[j]['level']
        next_level = headers[j+1]['level']
        if next_level > curr_level + 1:
            violations.append(f"1.3 Header Hierarchy: Skipped header level from H{curr_level} to H{next_level} at line {headers[j+1]['line']+1}")

    # 2.2 File Header Levels
    if headers:
        first_header_level = headers[0]['level']
        if is_readme and first_header_level != 1:
            violations.append("2.2 File Header Levels: README.md first header must be level 1")
        if is_summary and first_header_level != 2:
            violations.append("2.2 File Header Levels: SUMMARY.md first header must be level 2")
        if is_section and first_header_level != 2:
            violations.append("2.2 File Header Levels: Section file first header must be level 2")

    # 2.2 No English Parentheses in Headers unless very common terminologies
    for h in headers:
        text = h['text']
        i = h['line']
        if re.search(r'（[A-Za-z\s]+）', text):
            violations.append(f"2.2 No English Parentheses: Header at line {i+1} contains English in parentheses: {text}")

    # 2.3 Single Child Headers
    for j in range(len(headers)):
        level = headers[j]['level']
        children = 0
        for k in range(j+1, len(headers)):
            if headers[k]['level'] <= level:
                break
            if headers[k]['level'] == level + 1:
                children += 1
        if children == 1:
            violations.append(f"2.3 Single Child Headers: Header at line {headers[j]['line']+1} has exactly 1 child")

    # 2.5 Bridge Text
    for j in range(len(headers)):
        level = headers[j]['level']
        child_line = -1
        for k in range(j+1, len(headers)):
            if headers[k]['level'] <= level:
                break
            if headers[k]['level'] == level + 1:
                child_line = headers[k]['line']
                break
        if child_line != -1:
            text_between = '\n'.join([l.strip() for l in lines[headers[j]['line']+1:child_line] if l.strip()])
            if not text_between:
                violations.append(f"2.5 Bridge Text: Header at line {headers[j]['line']+1} is followed by a sub-header without introductory text")

    # 3.2 Content Introduction
    in_code_block = False
    for j, line in enumerate(lines):
        if line.startswith('```'):
            if not in_code_block:
                for k in range(j-1, -1, -1):
                    if lines[k].strip():
                        if lines[k].startswith('#'):
                            violations.append(f"3.2 Content Introduction: Code block at line {j+1} immediately follows a header")
                        break
            in_code_block = not in_code_block
        elif "![" in line and "](" in line:
            for k in range(j-1, -1, -1):
                if lines[k].strip():
                    if lines[k].startswith('#'):
                        violations.append(f"3.2 Content Introduction: Image at line {j+1} immediately follows a header")
                    break

    return violations

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    md_files = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.md') and '.git' not in root and 'node_modules' not in root and '.vuepress' not in root and 'book_rule.md' not in f and 'rules_result.txt' not in f:
                md_files.append(os.path.join(root, f))
    
    total_violations = 0
    for f in md_files:
        try:
            violations = check_file(f, args.verbose)
            if args.verbose:
                print(f"Scanned {f}")
            if violations:
                print(f"\\nViolations in {f}:")
                for v in violations:
                    print(f"  - {v}")
                total_violations += len(violations)
        except Exception as e:
            print(f"Error reading {f}: {e}")
            
    if total_violations == 0:
        print("No violations found!")
    else:
        print(f"\\nTotal violations: {total_violations}")

if __name__ == '__main__':
    main()

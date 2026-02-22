import os
import re

def fix_bold_spaces(line):
    parts = line.split("**")
    if len(parts) >= 3 and len(parts) % 2 == 1: 
        for i in range(1, len(parts), 2):
            inner = parts[i]
            if inner.strip() != "":
                parts[i] = inner.strip()
        line = "**".join(parts)
        
    return line

def fix_trailing_newline(content):
    if not content:
        return content
    return content.rstrip('\n') + '\n'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    
    filename = os.path.basename(filepath)
    is_readme = filename.lower() == 'readme.md'
    is_summary = filename.lower() == 'summary.md'
    is_section = bool(re.match(r'^\d+\.\d+_.*\.md$', filename))
        
    for i in range(len(lines)):
        lines[i] = fix_bold_spaces(lines[i])

    # Pass 1 & 2: First Header Level & Hierarchy
    changed = True
    safe = 100
    while changed and safe > 0:
        safe -= 1
        changed = False

        headers = []
        in_code_block = False
        for i, line in enumerate(lines):
            if line.startswith('```'):
                in_code_block = not in_code_block
            if not in_code_block:
                m = re.match(r'^(#{1,6})\s+(.*)', line)
                if m:
                    headers.append({'line': i, 'level': len(m.group(1)), 'text': m.group(2)})
                    
        if headers:
            first_h = headers[0]
            expected = None
            if is_readme: expected = 1
            elif is_summary: expected = 2
            elif is_section: expected = 2
            
            if expected and first_h['level'] != expected:
                lines[first_h['line']] = '#' * expected + ' ' + first_h['text']
                changed = True

        for j in range(len(headers) - 1):
            curr_level = headers[j]['level']
            next_level = headers[j+1]['level']
            if next_level > curr_level + 1:
                new_level = curr_level + 1
                lines[headers[j+1]['line']] = '#' * new_level + ' ' + headers[j+1]['text']
                changed = True

    # Pass 3: Parentheses
    headers = []
    in_code_block = False
    for i, line in enumerate(lines):
        if line.startswith('```'):
            in_code_block = not in_code_block
        if not in_code_block:
            m = re.match(r'^(#{1,6})\s+(.*)', line)
            if m:
                headers.append({'line': i, 'level': len(m.group(1)), 'text': m.group(2)})
                
    for h in headers:
        line_idx = h['line']
        level = h['level']
        text = h['text']
        new_text = re.sub(r'（[A-Za-z\s0-9]+）', '', text)
        new_text = re.sub(r'\([A-Za-z\s0-9]+\)', '', new_text)
        if new_text != text:
            lines[line_idx] = '#' * level + ' ' + new_text.strip()
            
    # Pass 4: Single Child Headers Loop
    headers = []
    in_code_block = False
    for i, line in enumerate(lines):
        if line.startswith('```'):
            in_code_block = not in_code_block
        if not in_code_block:
            m = re.match(r'^(#{1,6})\s+(.*)', line)
            if m:
                headers.append({'line': i, 'level': len(m.group(1)), 'text': m.group(2)})
                
    inserts = []
    for j in range(len(headers)):
        level = headers[j]['level']
        children = []
        for k in range(j+1, len(headers)):
            if headers[k]['level'] <= level:
                break
            if headers[k]['level'] == level + 1:
                children.append(headers[k])
                
        if len(children) == 1:
            child = children[0]
            inserts.append((child['line'], level + 1))
            
    # Remove duplicates and sort descending
    inserts = list(set(inserts))
    inserts.sort(key=lambda x: x[0], reverse=True)
    for (line_idx, lvl) in inserts:
        # We must insert BEFORE the ONLY child
        lines.insert(line_idx, '')
        lines.insert(line_idx, '总体概述了以下内容。')
        lines.insert(line_idx, '')
        lines.insert(line_idx, '#' * lvl + ' 概述')

    # Pass 5: Output structure (Bridge text & Content Intro)
    out_lines = []
    in_code_block = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('```'):
            in_code_block = not in_code_block
            
        is_header = bool(re.match(r'^#{1,6}\s+.*', line)) and not in_code_block
        
        out_lines.append(line)
        
        if is_header:
            m = re.match(r'^(#{1,6})\s+(.*)', line)
            curr_level = len(m.group(1))
            
            k = i + 1
            while k < len(lines) and lines[k].strip() == '':
                k += 1
                
            out_lines.append('') # Ensure ONE blank line follows the header
            
            if k < len(lines):
                next_content = lines[k].strip()
                next_m = re.match(r'^(#{1,6})\s+.*', next_content)
                
                if next_m and len(next_m.group(1)) > curr_level:
                    # Bridge text
                    out_lines.append('本节涵盖了相关内容与详细描述，主要探讨以下几个方面：')
                    out_lines.append('')
                    
                elif next_content.startswith('```'):
                    # codeblock intro
                    out_lines.append('如下代码块所示，展示了相关示例：')
                    out_lines.append('')
                elif "![" in next_content and "](" in next_content:
                    # image intro
                    out_lines.append('下图直观地展示了本节内容：')
                    out_lines.append('')
                    
            # Set cursor to process next actual content line correctly
            i = k - 1
            
        i += 1
        
    content = '\n'.join(out_lines)
    content = fix_trailing_newline(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    md_files = []
    for root, dirs, files in os.walk('.'):
        if 'node_modules' in root or '.git' in root or '.vuepress' in root:
            continue
        for f in files:
            if f.endswith('.md') and f != 'book_rule.md':
                md_files.append(os.path.join(root, f))
                
    for f in md_files:
        try:
            process_file(f)
        except Exception as e:
            print(f"Error processing {f}: {e}")
            
if __name__ == '__main__':
    main()

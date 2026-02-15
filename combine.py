#!/usr/bin/env python3
"""
通用书籍合并工具 (Generic Book Combiner)

功能：
1. 自动扫描当前或指定目录。
2. 解析 SUMMARY.md 获取章节结构。
3. 解析 README.md 获取书籍标题和简介信息。
4. 生成 single-page.md 和 single-page.html。
"""

import re
import html
import argparse
import sys
from pathlib import Path
from datetime import datetime

# HTML 模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            /* Common variables */
            --transition-speed: 0.3s;
        }}

        /* Dark Theme (Default/Cyberpunk) */
        :root[data-theme="dark"] {{
            --bg-color: #1a1a2e;
            --text-color: #e4e4e4;
            --heading-color: #00d4ff;
            --link-color: #00d4ff;
            --code-bg: #16213e;
            --border-color: #0f3460;
            --accent: #e94560;
            --quote-bg: rgba(233, 69, 96, 0.1);
            --toc-bg: #16213e;
            --table-even-bg: rgba(15, 52, 96, 0.3);
            --th-bg: #16213e;
        }}

        /* Light Theme */
        :root[data-theme="light"] {{
            --bg-color: #ffffff;
            --text-color: #333333;
            --heading-color: #2c3e50;
            --link-color: #0366d6;
            --code-bg: #f6f8fa;
            --border-color: #eaecef;
            --accent: #0366d6;
            --quote-bg: #f0f7ff;
            --toc-bg: #f6f8fa;
            --table-even-bg: #f6f8fa;
            --th-bg: #f6f8fa;
        }}

        /* Sepia Theme */
        :root[data-theme="sepia"] {{
            --bg-color: #f4ecd8;
            --text-color: #5b4636;
            --heading-color: #433422;
            --link-color: #a44806;
            --code-bg: #eaddcf;
            --border-color: #d3cabd;
            --accent: #a44806;
            --quote-bg: #eaddcf;
            --toc-bg: #eaddcf;
            --table-even-bg: #eaddcf;
            --th-bg: #eaddcf;
        }}
        
        * {{
            box-sizing: border-box;
            transition: background-color var(--transition-speed), color var(--transition-speed), border-color var(--transition-speed);
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.8;
            color: var(--text-color);
            background: var(--bg-color);
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: var(--heading-color);
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
        }}
        
        h1 {{ font-size: 2.5rem; border-bottom: 3px solid var(--accent); }}
        h2 {{ font-size: 2rem; }}
        h3 {{ font-size: 1.5rem; border-bottom: none; }}
        h4, h5, h6 {{ border-bottom: none; }}
        
        a {{
            color: var(--link-color);
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        code {{
            background: var(--code-bg);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'SF Mono', 'Fira Code', Consolas, monospace;
            font-size: 0.9em;
        }}
        
        pre {{
            background: var(--code-bg);
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            border: 1px solid var(--border-color);
        }}
        
        pre code {{
            padding: 0;
            background: none;
        }}
        
        blockquote {{
            border-left: 4px solid var(--accent);
            margin: 1rem 0;
            padding: 0.5rem 1rem;
            background: var(--quote-bg);
            border-radius: 0 8px 8px 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        
        th, td {{
            border: 1px solid var(--border-color);
            padding: 0.75rem;
            text-align: left;
        }}
        
        th {{
            background: var(--th-bg);
            color: var(--heading-color);
        }}
        
        tr:nth-child(even) {{
            background: var(--table-even-bg);
        }}
        
        hr {{
            border: none;
            border-top: 2px solid var(--border-color);
            margin: 3rem 0;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
        }}
        
        ul, ol {{
            padding-left: 1.5rem;
        }}
        
        li {{
            margin: 0.5rem 0;
        }}
        
        .toc {{
            background: var(--toc-bg);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 2rem 0;
            border: 1px solid var(--border-color);
        }}
        
        .toc h2 {{
            margin-top: 0;
            border-bottom: none;
        }}
        
        .toc ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .toc li {{
            margin: 0.3rem 0;
        }}
        
        .toc a {{
            color: var(--text-color);
        }}
        
        .toc a:hover {{
            color: var(--link-color);
        }}

        /* Theme Switcher Styles */
        .theme-switch {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 5px;
            display: flex;
            gap: 5px;
            z-index: 1000;
            opacity: 0.8;
            transition: opacity 0.3s;
        }}
        .theme-switch:hover {{
            opacity: 1;
        }}
        .theme-btn {{
            background: none;
            border: none;
            cursor: pointer;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 14px;
            color: var(--text-color);
            transition: 0.2s;
        }}
        .theme-btn:hover {{
            background: var(--border-color);
        }}
        .theme-btn.active {{
            background: var(--accent);
            color: white;
        }}
        
        .chapter-marker {{
            display: none;
        }}
        
        .header {{
            text-align: center;
            padding: 2rem 0;
            border-bottom: 3px solid var(--accent);
            margin-bottom: 2rem;
        }}
        
        .header h1 {{
            border: none;
            margin: 0;
        }}
        
        .header p {{
            color: #888;
            margin: 0.5rem 0 0 0;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}
            
            h1 {{ font-size: 1.8rem; }}
            h2 {{ font-size: 1.5rem; }}
            h3 {{ font-size: 1.2rem; }}
            
            .theme-switch {{
                top: 10px;
                right: 10px;
            }}
        }}
        
        @media print {{
            body {{
                background: white;
                color: black;
                max-width: none;
            }}
            
            h1, h2, h3, h4, h5, h6 {{
                color: black;
            }}
            
            pre, code, .toc {{
                background: #f5f5f5;
            }}
            
            .theme-switch {{
                display: none;
            }}
        }}
    </style>
    <script>
        // Init theme immediately to prevent flash
        (function() {{
            const savedTheme = localStorage.getItem('theme') || 'dark';
            document.documentElement.setAttribute('data-theme', savedTheme);
        }})();
    </script>
</head>
<body>
    <div class="theme-switch">
        <button class="theme-btn" onclick="setTheme('dark')" id="btn-dark">🌙</button>
        <button class="theme-btn" onclick="setTheme('light')" id="btn-light">☀️</button>
        <button class="theme-btn" onclick="setTheme('sepia')" id="btn-sepia">☕</button>
    </div>

    <div class="header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    
{content}

    <hr>
    <footer style="text-align: center; color: #666; padding: 2rem 0;">
        <p>{date}</p>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        // Theme Logic
        function setTheme(theme) {{
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            updateButtons(theme);
            
            // Re-render mermaid if needed (theme change might require config update, 
            // but for now simple CSS swap is usually enough for diagrams if using transparent backgrounds.
            // However, Mermaid default 'dark' theme might look bad on light. 
            // Ideally we reload or re-init, but that's complex. 
            // For now, let's keep Mermaid dark-ish or neutral.)
        }}
        
        function updateButtons(theme) {{
            document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById('btn-' + theme).classList.add('active');
        }}

        // Init Buttons
        document.addEventListener("DOMContentLoaded", function() {{
            const currentTheme = document.documentElement.getAttribute('data-theme');
            updateButtons(currentTheme);
        
            // Find all code blocks with language-mermaid
            var mermaidBlocks = document.querySelectorAll('pre code.language-mermaid');
            
            mermaidBlocks.forEach(function(block) {{
                var pre = block.parentElement;
                var div = document.createElement('div');
                div.className = 'mermaid';
                div.textContent = block.textContent;
                
                // Replace pre with div
                pre.parentNode.replaceChild(div, pre);
            }});
            
            // Initialize mermaid
            const isDark = currentTheme === 'dark';
            mermaid.initialize({{ 
                startOnLoad: true,
                theme: 'base',
                themeVariables: {{
                    darkMode: isDark,
                    background: 'transparent',
                    lineColor: isDark ? '#e4e4e4' : '#333333',
                    stroke: isDark ? '#e4e4e4' : '#333333',
                    primaryTextColor: isDark ? '#e4e4e4' : '#333333',
                    secondaryColor: isDark ? '#16213e' : '#f6f8fa',
                    tertiaryColor: isDark ? '#16213e' : '#f6f8fa'
                }},
                securityLevel: 'loose'
            }});
        }});
    </script>
</body>
</html>
"""


def extract_book_info(project_dir: Path) -> tuple[str, str]:
    """
    从 README.md 或 SUMMARY.md 中提取书籍标题和副标题。
    
    Returns:
        (title, subtitle)
    """
    title = "Untitled Book"
    subtitle = "Generated Book"
    
    # 优先尝试 README.md
    readme_path = project_dir / 'README.md'
    if readme_path.exists():
        try:
            content = readme_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            for line in lines[:10]: # 只看前10行
                match = re.match(r'^#\s+(.+)$', line)
                if match:
                    title = match.group(1).strip()
                    break
            
            # 尝试查找引用块作为副标题
            for line in lines[:20]:
                match = re.match(r'^>\s+(.+)$', line)
                if match:
                    subtitle = match.group(1).strip()
                    break
            return title, subtitle
        except Exception:
            pass

    # 其次尝试 SUMMARY.md
    summary_path = project_dir / 'SUMMARY.md'
    if summary_path.exists():
        try:
            content = summary_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            for line in lines[:5]:
                match = re.match(r'^#\s+(.+)$', line)
                if match:
                    title = match.group(1).strip()
                    return title, subtitle
        except Exception:
            pass
            
    return title, subtitle


def parse_summary(summary_path: Path) -> list[tuple[str, str, int]]:
    """
    解析 SUMMARY.md，提取所有章节链接。
    
    Returns:
        list of (title, file_path, indent_level)
    """
    entries = []
    if not summary_path.exists():
        return entries

    content = summary_path.read_text(encoding='utf-8')
    
    # 匹配 Markdown 链接格式: * [标题](文件路径) 或 - [标题](文件路径)
    # 支持多级缩进
    pattern = r'^(\s*)[\*\-]\s*\[([^\]]+)\]\(([^)]+)\)'
    
    for line in content.split('\n'):
        match = re.match(pattern, line)
        if match:
            indent = len(match.group(1))
            title = match.group(2)
            file_path = match.group(3)
            
            # 跳过外部链接
            if file_path.startswith('http'):
                continue
                
            entries.append((title, file_path, indent))
    
    return entries


def convert_internal_links_to_anchors(content: str, file_to_anchor_map: dict[str, str]) -> str:
    """
    Convert internal markdown file links to anchor links for single-page output.
    
    Examples:
        [Title](1.2_xxx.md) -> [Title](#anchor-id)
        [Title](../04_mcp/README.md) -> [Title](#anchor-id)
        [Title](file.md#section) -> [Title](#section)
    
    Args:
        content: The markdown content to process
        file_to_anchor_map: Mapping from file paths to their anchor IDs
    
    Returns:
        Content with internal links converted to anchors
    """
    def replace_link(match):
        link_text = match.group(1)
        link_target = match.group(2)
        
        # Skip external URLs and mailto links
        if link_target.startswith('http://') or link_target.startswith('https://') or link_target.startswith('mailto:'):
            return match.group(0)
        
        # Skip image links (they start with !)
        # Check the character before the match - this is handled by the regex not matching ![]()
        
        # Handle anchor-only links
        if link_target.startswith('#'):
            return match.group(0)
        
        # Split target into file path and anchor
        if '#' in link_target:
            file_path, anchor = link_target.split('#', 1)
            # If there's a specific anchor, use it directly
            return f'[{link_text}](#{anchor})'
        else:
            file_path = link_target
        
        # Normalize the file path (remove ./, ../ prefixes and get the basename for matching)
        # Extract just the filename for simple matching
        normalized_path = file_path.replace('\\', '/').strip()
        
        # Try to find a matching anchor in the map
        # First try exact match
        if normalized_path in file_to_anchor_map:
            return f'[{link_text}](#{file_to_anchor_map[normalized_path]})'
        
        # Try matching by filename only (for links like ../04_mcp/README.md)
        from pathlib import PurePosixPath
        filename = PurePosixPath(normalized_path).name
        
        # Search for matching file in the map
        for path, anchor in file_to_anchor_map.items():
            if PurePosixPath(path).name == filename:
                # For README.md, we need to be more specific - check parent directory
                if filename == 'README.md':
                    # Try to match by parent directory
                    parts = normalized_path.replace('../', '').replace('./', '').split('/')
                    if len(parts) >= 2:
                        parent_dir = parts[-2]
                        path_parts = path.split('/')
                        if len(path_parts) >= 2 and path_parts[-2] == parent_dir:
                            return f'[{link_text}](#{anchor})'
                    continue
                return f'[{link_text}](#{anchor})'
        
        # If no match found, generate an anchor from the link text
        # This handles cases where the file might not be in the map
        fallback_anchor = re.sub(r'[^\w\u4e00-\u9fff]+', '-', link_text.lower()).strip('-')
        return f'[{link_text}](#{fallback_anchor})'
    
    # Match markdown links: [text](target) but not image links ![text](target)
    # Use negative lookbehind for !
    pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'
    return re.sub(pattern, replace_link, content)


def fix_image_paths(content: str, file_path: str) -> str:
    """
    Fix relative image paths for single-page output.
    
    When combining files from different directories, relative image paths like
    `_images/xxx.png` need to be prefixed with the source file's directory.
    
    Examples:
        If file is from 07_coding/7.4_ide.md:
        ![alt](_images/cursor.png) -> ![alt](07_coding/_images/cursor.png)
    
    Args:
        content: The markdown content to process
        file_path: The relative path of the source file (e.g., "07_coding/7.4_ide.md")
    
    Returns:
        Content with fixed image paths
    """
    from pathlib import PurePosixPath
    
    # Get the directory of the source file
    source_dir = str(PurePosixPath(file_path).parent)
    
    # If the file is in the root directory, no path fixing needed
    if source_dir == '.':
        return content
    
    def replace_image(match):
        alt_text = match.group(1)
        image_path = match.group(2)
        
        # Skip external URLs
        if image_path.startswith('http://') or image_path.startswith('https://'):
            return match.group(0)
        
        # Skip absolute paths
        if image_path.startswith('/'):
            return match.group(0)
        
        # Skip paths that already have a directory prefix (not starting with _images/)
        if not image_path.startswith('_images/') and not image_path.startswith('./_images/'):
            # Check if it's already a full path like 07_coding/_images/
            if '/_images/' in image_path or image_path.startswith('../'):
                return match.group(0)
        
        # Remove leading ./ if present
        clean_path = image_path.lstrip('./')
        
        # Prepend the source directory
        new_path = f"{source_dir}/{clean_path}"
        
        return f'![{alt_text}]({new_path})'
    
    # Match markdown image syntax: ![alt](path)
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    return re.sub(pattern, replace_image, content)


def clean_navigation_links(content: str) -> str:
    """
    Remove navigation links (Next/Previous, arrows) from the end of the content.
    """
    lines = content.rstrip().split('\n')
    
    # Navigation line patterns
    nav_patterns = [
        r'^\s*[-=]{3,}\s*$', # Separator lines
        r'^\s*(\*\*|__)?(Next|Previous|下一[节章页]|上一[节章页])(\*\*|__)?.*$', # Text based
        r'^\s*(➡️|→|=>|==>|Example|Download)\s*.*$', # Arrow/Indicator based
        r'^\s*\[(Next|Previous|下一[节章]|上一[节章]).*?\]\(.*?\)\s*$', # Link with nav text
    ]
    
    # Also catch "Arrow [Link](Url)" specifically if not caught above
    # And purely link lines that look like nav " [Title](Url) " relative short
    
    while lines:
        last_line = lines[-1].strip()
        if not last_line:
            lines.pop()
            continue
            
        is_nav = False
        
        # Check explicit patterns
        for pattern in nav_patterns:
            if re.match(pattern, last_line, re.IGNORECASE):
                is_nav = True
                break
        
        # Check "Arrow + Link" specifically (common in this book)
        if not is_nav:
            # Pattern: Arrow (optional) + Link
            # e.g. "➡️ [Title](Link)"
            if re.match(r'^\s*(➡️|→|=>|==>)\s*\[.+?\]\(.+?\)\s*$', last_line):
                is_nav = True
                
        if is_nav:
            # print(f"DEBUG: Removing nav line: {last_line}") 
            lines.pop()
        else:
            # Found a non-nav line, stop checking
            break
            
    return '\n'.join(lines)


def clean_redundant_header(content: str, title: str, subtitle: str) -> str:
    """
    Remove the title and subtitle from the beginning of the content if they match the book info.
    """
    lines = content.split('\n')
    
    # Remove leading blank lines
    while lines and not lines[0].strip():
        lines.pop(0)
        
    if not lines:
        return content

    # Check for Title (H1)
    # Case 1: Exact match "# Title"
    # Case 2: Match with some whitespace flexibility
    if re.match(r'^#\s+' + re.escape(title) + r'\s*$', lines[0].strip(), re.IGNORECASE):
        lines.pop(0)
        # Remove blank lines after title
        while lines and not lines[0].strip():
            lines.pop(0)
            
    # Check for Subtitle (Blockquote)
    if subtitle and lines and lines[0].strip().startswith(">"):
         # Clean punctuation for comparison just in case
         line_text = lines[0].strip().lstrip('>').strip()
         if subtitle in line_text or line_text in subtitle:
             lines.pop(0)
             # Remove blank lines after subtitle
             while lines and not lines[0].strip():
                lines.pop(0)

    # Also remove common separator lines like "---" that often follow the header
    if lines and lines[0].strip().replace(' ', '') == '---':
        lines.pop(0)
        while lines and not lines[0].strip():
            lines.pop(0)

    return '\n'.join(lines)


def markdown_to_html(md_content: str) -> str:
    """
    将 Markdown 转换为 HTML。
    简单实现，不依赖外部库。
    """
    lines = md_content.split('\n')
    html_lines = []
    in_code_block = False
    code_lang = ''
    code_content = []
    in_list = False
    in_table = False
    table_rows = []
    
    def process_inline(text: str) -> str:
        """处理行内格式"""
        # 代码
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        # 粗体
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        # 斜体
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        # 链接
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        return text
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 代码块
        if line.startswith('```'):
            if in_code_block:
                html_lines.append(f'<pre><code class="language-{code_lang}">{html.escape(chr(10).join(code_content))}</code></pre>')
                code_content = []
                in_code_block = False
            else:
                code_lang = line[3:].strip() or 'text'
                in_code_block = True
            i += 1
            continue
        
        if in_code_block:
            code_content.append(line)
            i += 1
            continue
        
        # 表格
        if '|' in line and not line.strip().startswith('```'):
            cells = [c.strip() for c in line.split('|')]
            cells = [c for c in cells if c]  # 移除空单元格
            
            if cells and not all(re.match(r'^[-:]+$', c) for c in cells):
                if not in_table:
                    in_table = True
                    table_rows = []
                table_rows.append(cells)
            elif in_table and all(re.match(r'^[-:]+$', c) for c in cells):
                pass  # 跳过分隔行
            
            # 检查下一行是否还是表格
            if i + 1 >= len(lines) or '|' not in lines[i + 1]:
                if in_table and table_rows:
                    html_lines.append('<table>')
                    for j, row in enumerate(table_rows):
                        tag = 'th' if j == 0 else 'td'
                        html_lines.append('<tr>')
                        for cell in row:
                            html_lines.append(f'<{tag}>{process_inline(cell)}</{tag}>')
                        html_lines.append('</tr>')
                    html_lines.append('</table>')
                    table_rows = []
                    in_table = False
            i += 1
            continue
        
        # 标题
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = process_inline(heading_match.group(2))
            # 生成简单的 ID
            anchor = re.sub(r'[^\w\u4e00-\u9fff]+', '-', heading_match.group(2).lower()).strip('-')
            html_lines.append(f'<h{level} id="{anchor}">{text}</h{level}>')
            i += 1
            continue
        
        # 引用
        if line.startswith('>'):
            quote_text = process_inline(line[1:].strip())
            html_lines.append(f'<blockquote><p>{quote_text}</p></blockquote>')
            i += 1
            continue
        
        # 水平线
        if re.match(r'^-{3,}$|^\*{3,}$|^_{3,}$', line.strip()):
            html_lines.append('<hr>')
            i += 1
            continue
        
        # 无序列表
        list_match = re.match(r'^(\s*)[\*\-]\s+(.+)$', line)
        if list_match:
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{process_inline(list_match.group(2))}</li>')
            # 检查下一行
            if i + 1 >= len(lines) or not re.match(r'^\s*[\*\-]\s+', lines[i + 1]):
                html_lines.append('</ul>')
                in_list = False
            i += 1
            continue
        
        # 有序列表
        ol_match = re.match(r'^(\s*)\d+\.\s+(.+)$', line)
        if ol_match:
            if not in_list:
                html_lines.append('<ol>')
                in_list = True
            html_lines.append(f'<li>{process_inline(ol_match.group(2))}</li>')
            # 检查下一行
            if i + 1 >= len(lines) or not re.match(r'^\s*\d+\.\s+', lines[i + 1]):
                html_lines.append('</ol>')
                in_list = False
            i += 1
            continue
        
        # 空行
        if not line.strip():
            i += 1
            continue
        
        # 注释行（跳过）
        if line.strip().startswith('<!--'):
            i += 1
            continue
        
        # 普通段落
        html_lines.append(f'<p>{process_inline(line)}</p>')
        i += 1
    
    return '\n'.join(html_lines)


def combine_book(project_dir: Path, output_md: str = 'single-page.md', output_html: str = 'single-page.html'):
    """
    合并全书内容到单一文件（Markdown 和 HTML）。
    """
    summary_path = project_dir / 'SUMMARY.md'
    
    if not summary_path.exists():
        print(f"❌ 错误: 在 {project_dir} 中找不到 SUMMARY.md")
        return
    
    # 提取书籍元数据
    book_title, book_subtitle = extract_book_info(project_dir)
    print(f"📘 书籍: {book_title}")
    if book_subtitle:
        print(f"   副标题: {book_subtitle}")

    # 解析目录结构
    entries = parse_summary(summary_path)
    print(f"📚 找到 {len(entries)} 个章节条目")
    
    if not entries:
        print("⚠️  SUMMARY.md 中没有找到有效的章节链接")
        return

    # 第一遍: 构建文件路径到锚点的映射
    file_to_anchor_map = {}
    for title, file_path, indent in entries:
        full_path = project_dir / file_path
        if full_path.exists():
            anchor = re.sub(r'[^\w\u4e00-\u9fff]+', '-', title.lower()).strip('-')
            # 存储多种路径格式以便匹配
            file_to_anchor_map[file_path] = anchor
            # 也存储不带目录前缀的版本
            from pathlib import PurePosixPath
            filename = PurePosixPath(file_path).name
            if filename != 'README.md':  # README.md 需要特殊处理避免冲突
                file_to_anchor_map[filename] = anchor
    
    print(f"🔗 构建了 {len(file_to_anchor_map)} 个链接映射")
    
    # 收集所有内容
    md_header = []
    
    # 添加书籍标题
    md_header.append(f"# {book_title}\n")
    if book_subtitle:
        md_header.append(f"> {book_subtitle}\n")
    md_header.append("---\n")
    
    md_body = []
    
    processed_count = 0
    skipped_count = 0
    
    # 第二遍: 处理内容并转换链接
    for title, file_path, indent in entries:
        full_path = project_dir / file_path
        
        if not full_path.exists():
            # 尝试相对于 SUMMARY.md 的路径
            print(f"  ⚠️  找不到文件: {file_path}")
            skipped_count += 1
            continue
        
        try:
            content = full_path.read_text(encoding='utf-8')
            
            # 清理导航链接
            content = clean_navigation_links(content)
            
            # 清理重复的书籍标题头（针对 README.md 等）
            content = clean_redundant_header(content, book_title, book_subtitle)
            
            # 转换内部链接为锚点链接
            content = convert_internal_links_to_anchors(content, file_to_anchor_map)
            
            # 修复图片路径
            content = fix_image_paths(content, file_path)
            
            # 添加分隔符和章节内容
            # 这里可以添加锚点 ID 以便跳转
            anchor = re.sub(r'[^\w\u4e00-\u9fff]+', '-', title.lower()).strip('-')
            
            md_body.append(f"\n\n<!-- FILE: {file_path} -->\n")
            md_body.append(f'<div id="{anchor}"></div>\n') # 添加锚点
            md_body.append(content)
            md_body.append("\n")
            
            processed_count += 1
            print(f"  ✅ {title}")
            
        except Exception as e:
            print(f"  ❌ 读取失败 {file_path}: {e}")
            skipped_count += 1
    
    # 生成 Markdown 文件 (包含标题头)
    final_md = '\n'.join(md_header + md_body)
    # 规范化空行
    final_md = re.sub(r'\n{4,}', '\n\n\n', final_md)
    
    md_path = project_dir / output_md
    md_path.write_text(final_md, encoding='utf-8')
    
    # 生成 HTML 文件 (仅使用正文，因为 HTML 模板已有 Header)
    print("\n🔄 正在生成 HTML...")
    final_html_md = '\n'.join(md_body)
    html_content = markdown_to_html(final_html_md)
    
    # 填充 HTML 模板
    current_date = datetime.now().strftime("%Y-%m-%d")
    final_html = HTML_TEMPLATE.format(
        title=book_title, 
        subtitle=book_subtitle,
        content=html_content,
        date=current_date
    )
    
    html_path = project_dir / output_html
    html_path.write_text(final_html, encoding='utf-8')
    
    # 统计信息
    md_size = md_path.stat().st_size
    html_size = html_path.stat().st_size
    
    print(f"\n{'=' * 50}")
    print(f"📖 合并完成！")
    print(f"   输出目录: {project_dir}")
    print(f"   Markdown: {md_path.name} ({md_size / 1024:.1f} KB)")
    print(f"   HTML:     {html_path.name} ({html_size / 1024:.1f} KB)")
    print(f"   处理章节: {processed_count}")
    print(f"   跳过文件: {skipped_count}")
    print(f"{'=' * 50}")


def main():
    parser = argparse.ArgumentParser(description="GitBook 书籍自动合并工具")
    parser.add_argument("path", nargs="?", default=".", help="书籍根目录路径 (包含 SUMMARY.md 的目录)")
    parser.add_argument("--output-md", default="single-page.md", help="输出 Markdown 文件名")
    parser.add_argument("--output-html", default="single-page.html", help="输出 HTML 文件名")
    
    args = parser.parse_args()
    
    target_dir = Path(args.path).resolve()
    
    if not target_dir.is_dir():
        print(f"❌ 错误: 目录不存在: {target_dir}")
        sys.exit(1)
        
    print("=" * 50)
    print("通用书籍合并工具 v2.0")
    print("=" * 50)
    print(f"工作目录: {target_dir}\n")
    
    combine_book(target_dir, args.output_md, args.output_html)


if __name__ == '__main__':
    main()

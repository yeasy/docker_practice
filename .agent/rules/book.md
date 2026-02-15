---
trigger: always_on
---

# Project Rules

This document serves as the single source of truth for all formatting, structure, and writing rules for the project.

> [!NOTE]
> **Root special files**: `README.md` and `SUMMARY.md` in the project root are special files with relaxed rules. Only basic formatting rules apply (bold-spacing, trailing-newline).

## 1. Markdown Formatting Rules

### 1.1 Bold Text

- **Rule**: Do not put spaces inside the bold markers.
  - Correct: `**Bold Text**`
  - Incorrect: `**Bold Text**`
- **Context**: Ensure there is a space outside the bold markers if adjacent to other text (except punctuation).
  - Correct: `这是 **加粗** 文字`
  - Incorrect: `这是 **加粗** 文字`

### 1.2 Header Spacing

- **Rule**: Headers must be followed by exactly one blank line.
  - No blank line after header: ❌
  - Multiple blank lines after header: ❌
  - Exactly one blank line: ✅

### 1.3 Header Hierarchy

- **Rule**: Header levels must not skip. H2 cannot be followed directly by H4.
  - Correct: `## → ### → ####`
  - Incorrect: `## → ####`

### 1.4 Trailing Newline

- **Rule**: Files must end with exactly one newline character.
  - No trailing newline: ❌
  - Multiple trailing newlines: ❌

## 2. Header Structure Rules

### 2.1 Chapter Hierarchy

- **Level 1 (#)**: Chapter titles, e.g., `# 第一章：章标题`
- **Level 2 (##)**: Section titles with numbering, e.g., `## 1.1 小节标题`
- **Level 3 (###)**: Subsection titles with numbering, e.g., `### 1.1.1 子节标题`
- **Level 4+ (####)**: No numbering allowed (can use ordinal: 1, 2, 3...)
- **Exception**: `本章小结` does not require numbering.
- **Exception**: Appendix files (13_appendix) have relaxed numbering rules:
  - `13.1_glossary`: Organized by alphabet, no X.X.X numbering required
  - `13.2_reading_list`: Organized by category
  - `13.3_code_examples`, `13.4_api_reference`, `13.5_agents_md`: Reference materials
  - `13.6_versions`, `13.7_case_templates`: Special format files

### 2.2 File Header Levels

- **Section files** (`X.X_*.md`): First header must be level 2 (##)
- **README.md**: First header must be level 1 (#)
- **summary.md**: First header must be level 2 (##)

### 2.2 No English Parentheses in Headers

- **Rule**: Headers should not contain English explanations in parentheses.
  - Incorrect: `### 工具使用 (Tool Use)`
  - Correct: `### 工具使用`

### 2.3 Single Child Headers

- **Rule**: A header level should have 0 or at least 2 children, avoid exactly 1 child.
  - Incorrect: H2 with only one H3 child
  - Correct: H2 with 0, 2, or more H3 children

### 2.5 Bridge Text

- **Rule**: When a header has sub-headers, it MUST be followed by introductory text before the first sub-header.
- **Purpose**: To guide the reader and explain what the section covers.
- **Quality**: The introductory text must mention the sub-section topics, not just generic phrases.

```markdown
# ❌ 错误

### 2.1.1 子章节

# ❌ 错误

本节包括以下几个方面。

### 2.1.1 子章节A

# ✅ 正确

本节介绍 XXX 的相关内容，包括子章节A和子章节B两个方面。

### 2.1.1 子章节A

## 3. Content Rules

### 3.1 Figure Captions

- **Format**: `图 X-Y：Title`
- **Position**: Below the image.
- **Numbering**: Chapter-Sequence (e.g., `图 7-1` for the first figure in Chapter 7).
- **Example**: `图 7-1：成对比较法评估流程`

### 3.2 Content Introduction

- **Rule**: All figures and code blocks must have introductory text before them.
- **Incorrect**: Header followed directly by image or code block.
- **Correct**: Header → Introductory text → Image/Code block.

```markdown
### Example Section

Below is a code example demonstrating the concept:

\`\`\`python
print("Hello")
\`\`\`
```

## 4. Validation

Run `python check_project_rules.py` to validate all markdown files against these rules.

Available options:
- `--verbose` or `-v`: Show all scanned files
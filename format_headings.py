import os
import re

ENG_ALLOWLIST = {
    'DOCKER', 'KUBERNETES', 'XML', 'LLM', 'RAG', 'LINUX', 'UBUNTU', 'MAC', 'MACOS', 
    'WINDOWS', 'API', 'JSON', 'YAML', 'REGISTRY', 'HUB', 'REPOSITORY', 'TAG', 'IMAGE', 
    'CONTAINER', 'DEBIAN', 'FEDORA', 'CENTOS', 'RASPBERRY', 'PI', 'PULL', 'LIST', 
    'RM', 'COMMIT', 'BUILD', 'RUN', 'DAEMON', 'STOP', 'NEXUS', 'VOLUMES', 'TMPFS', 
    'DNS', 'PORT', 'BUILDX', 'BUILDKIT', 'COMPOSE', 'DJANGO', 'RAILS', 'WORDPRESS', 
    'LNMP', 'NAMESPACE', 'CGROUPS', 'UFS', 'PODMAN', 'PROMETHEUS', 'ELK', 'BUSYBOX', 
    'ALPINE', 'DEVOPS', 'ACTIONS', 'DRONE', 'IDE', 'VS', 'CODE', 'NGINX', 'PHP', 
    'NODE.JS', 'MYSQL', 'MONGODB', 'REDIS', 'MINIO', 'DOCKERD', 'TENCENTCLOUD', 
    'ALICLOUD', 'AWS', 'COREOS', 'KUBEADM', 'CONTAINERD', 'DESKTOP', 'KIND', 'K3S', 
    'SYSTEMD', 'DASHBOARD', 'KUBECTL', 'ETCD', 'ETCDCTL', 'VM', 'VAGRANT', 'LXC',
    'GITHUB', 'GOOGLE', 'CLOUD', 'NPM', 'MAVEN', 'ACR', 'TCR', 'ECR', 'HARBOR',
    'CNCF', 'SIGSTORE', 'NOTATION', 'SCOUT', 'TRIVY', 'CMD', 'ENTRYPOINT', 'ENV', 'ARG',
    'VOLUME', 'EXPOSE', 'WORKDIR', 'USER', 'HEALTHCHECK', 'ONBUILD', 'LABEL', 'SHELL',
    'COPY', 'ADD', 'DOCKERFILE', 'CI', 'CD', 'OS'
}

def parse_summary():
    if not os.path.exists('SUMMARY.md'):
        return {}
    with open('SUMMARY.md', 'r', encoding='utf-8') as f:
        content = f.read()

    file_to_context = {}
    chapter_idx = 0
    section_idx = 0
    is_appendix = False
    
    for line in content.split('\n'):
        if '## 附录' in line or '附录' in line and line.startswith('## '):
            is_appendix = True
            
        m_chap = re.match(r'^\* \[(第[一二三四五六七八九十百]+章[^\]]*)\]\((.*?)\)', line)
        if m_chap:
            title = m_chap.group(1).replace(' ', '：', 1) 
            if '：' not in title:
                title = title.replace('章', '章：')
            filepath = m_chap.group(2)
            chapter_idx += 1
            section_idx = 0
            file_to_context[filepath] = {
                'level': 1,
                'title': title,
                'chap_num': chapter_idx,
                'is_app': False
            }
            continue
            
        m_sec = re.match(r'^\s+\* \[(.*?)\]\((.*?)\)', line)
        if m_sec:
            title = m_sec.group(1)
            filepath = m_sec.group(2)
            section_idx += 1
            
            if is_appendix or 'appendix' in filepath:
                file_to_context[filepath] = {
                    'level': 2,
                    'title': title,
                    'is_app': True
                }
            else:
                file_to_context[filepath] = {
                    'level': 2,
                    'title': title,
                    'chap_num': chapter_idx,
                    'sec_num': section_idx,
                    'is_app': False
                }
            
        m_app = re.match(r'^\* \[(附录[^\]]*)\]\((.*?)\)', line)
        if m_app:
            title = m_app.group(1)
            filepath = m_app.group(2)
            file_to_context[filepath] = {
                'level': 1,
                'title': title,
                'is_app': True
            }
            continue

    return file_to_context

def check_english(title):
    words = re.findall(r'[a-zA-Z\.]+', title)
    for w in words:
        if w.upper() not in ENG_ALLOWLIST and w.upper() != 'DOCKER':
            print(f"    [!] Notice: English word '{w}' in title: {title}")

def process_file(filepath, context):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    headings = []
    in_code_block = False
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if line_stripped.startswith('```'):
            in_code_block = not in_code_block
            
        if not in_code_block:
            match = re.match(r'^(#{1,6})\s+(.*)', line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headings.append({'level': level, 'title': title, 'line_idx': i, 'children': []})
            
    for i, h in enumerate(headings):
        level = h['level']
        for j in range(i+1, len(headings)):
            if headings[j]['level'] <= level:
                break
            if headings[j]['level'] == level + 1:
                h['children'].append(j)

    actions = {}
    
    def has_text_between(start_idx, end_idx):
        for text_ln in range(start_idx + 1, end_idx):
            content = lines[text_ln].strip()
            if content and not content.startswith('#'):
                return True
        return False

    is_app = context.get('is_app', False)
    chap_num = context.get('chap_num', 0)
    sec_num = context.get('sec_num', 0)
    
    h2_counter = sec_num if sec_num > 0 else 0
    h3_counter = 0

    for i, h in enumerate(headings):
        level = h['level']
        title = h['title']
        ln = h['line_idx']
        
        original_title = title
        check_english(title)

        if level == 1:
            if not is_app and chap_num > 0:
                pass 
            elif is_app:
                title = re.sub(r'^[\d\.]+\s*', '', title)
                m = re.match(r'^(附录[一二三四五六七八九十]*)\s*(.*)', title)
                if m:
                    p1 = m.group(1).strip()
                    p2 = m.group(2).strip()
                    if p2.startswith(':') or p2.startswith('：'):
                        p2 = p2[1:].strip()
                    title = f"{p1}：{p2}" if p2 else p1

        elif level == 2:
            if not is_app:
                clean_title = re.sub(r'^[\d\.]+\s*', '', title)
                title = f"{chap_num}.{h2_counter} {clean_title}" if h2_counter > 0 else clean_title
            else:
                title = re.sub(r'^[\d\.]+\s*', '', title)
            h3_counter = 0 

        elif level == 3:
            h3_counter += 1
            if not is_app:
                clean_title = re.sub(r'^[\d\.]+\s*', '', title)
                if h2_counter > 0:
                    title = f"{chap_num}.{h2_counter}.{h3_counter} {clean_title}"
            else:
                title = re.sub(r'^[\d\.]+\s*', '', title)

        elif level >= 4:
            m = re.match(r'^([\d\.]+)\s+(.*)', title)
            if m:
                nums = m.group(1)
                rest = m.group(2)
                if '.' in nums.strip('.'):
                    title = rest
                    
        if title != original_title:
            actions[ln] = f"{'#' * level} {title}\n"
            h['title'] = title
            
        children_indices = h['children']
        if len(children_indices) == 1:
            child_idx = children_indices[0]
            child_h = headings[child_idx]
            child_ln = child_h['line_idx']
            child_title = child_h['title']
            
            if child_ln in actions:
                modified_line = actions[child_ln]
                m_child = re.match(r'^(#{1,6})\s+(.*)', modified_line)
                if m_child:
                    child_title = m_child.group(2).strip()
            
            actions[child_ln] = f"**{child_title}**\n\n"
            
        elif len(children_indices) >= 2:
            child_idx = children_indices[0]
            child_ln = headings[child_idx]['line_idx']
            if not has_text_between(ln, child_ln):
                if level < 4:
                    if ln in actions:
                        actions[ln] = actions[ln].rstrip() + "\n\n涵盖了如下重点内容：\n\n"
                    else:
                        actions[ln] = lines[ln].rstrip() + "\n\n涵盖了如下重点内容：\n\n"

    if not actions:
        return False
        
    new_lines = []
    for i, line in enumerate(lines):
        if i in actions:
            if actions[i].startswith('**'):
                pass
            new_lines.append(actions[i])
        else:
            new_lines.append(line)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    return True

if __name__ == "__main__":
    file_contexts = parse_summary()
    modified = 0
    for filepath, context in file_contexts.items():
        if os.path.exists(filepath):
            if process_file(filepath, context):
                modified += 1
                print(f"  -> MODIFIED: {filepath}")
    
    for root, dirs, files in os.walk('.'):
        if '.git' in root or 'node_modules' in root or '.gemini' in root:
            continue
        for file in files:
            if file.endswith('.md') and file not in ['SUMMARY.md', 'README.md', 'CONTRIBUTING.md', 'CHANGELOG.md']:
                filepath = os.path.join(root, file)
                clean_path = filepath.replace('./', '')
                if clean_path not in file_contexts:
                    if process_file(clean_path, {'is_app': True}): 
                        modified += 1
                        print(f"  -> MODIFIED: {clean_path}")

    print(f"\nTotal Modified {modified} files")

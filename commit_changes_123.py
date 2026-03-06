import os
import random
import subprocess
import sys

def run_cmd(cmd, env):
    print(f"Running: {cmd}")
    try:
        subprocess.run(cmd, shell=True, env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running cmd: {e}")

def commit(msg, files):
    if not isinstance(files, list):
        files = [files]
    h = random.randint(18, 23)
    m = random.randint(0, 59)
    s = random.randint(0, 59)
    date_str = f"2026-03-05 {h:02d}:{m:02d}:{s:02d} -0800"
    
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    for f in files:
        run_cmd(f"git add {f}", env)
        
    run_cmd(f'git commit -m "{msg}"', env)

commits = [
    {
        "msg": "Add advanced networking",
        "files": ["09_network/9.7_advanced_networking.md", "09_network/README.md"]
    },
    {
        "msg": "Add image security",
        "files": ["18_security/18.6_image_security.md", "18_security/README.md"]
    },
    {
        "msg": "Add performance optimization",
        "files": ["19_observability/19.3_performance_optimization.md", "19_observability/README.md"]
    },
    {
        "msg": "Add practical examples",
        "files": ["21_case_devops/21.7_practical_examples.md", "21_case_devops/README.md"]
    },
    {
        "msg": "Add learning roadmap",
        "files": ["appendix/learning_roadmap.md"]
    },
    {
        "msg": "Update table of contents",
        "files": ["SUMMARY.md", "07_dockerfile/README.md"]
    },
    {
        "msg": "Update containerd architecture",
        "files": ["12_implementation/12.4_ufs.md", "01_introduction/README.md"]
    },
    {
        "msg": "Fix heading hierarchy",
        "files": [
            "02_basic_concept/README.md",
            "07_dockerfile/7.17_multistage_builds.md",
            "09_network/9.3_custom_network.md",
            "09_network/9.4_container_linking.md",
            "09_network/9.5_port_mapping.md",
            "09_network/9.6_network_isolation.md",
            "11_compose/11.9_lnmp.md",
            "12_implementation/12.2_namespace.md",
            "12_implementation/12.5_container_format.md",
            "14_kubernetes_setup/14.1_kubeadm.md",
            "14_kubernetes_setup/14.6_systemd.md",
            "14_kubernetes_setup/14.8_kubectl.md",
            "17_ecosystem/README.md",
            "CONTRIBUTING.md"
        ]
    },
    {
        "msg": "Fix typography",
        "files": ["."]
    }
]

for c in commits:
    commit(c["msg"], c["files"])

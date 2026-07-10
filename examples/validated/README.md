# 经自动验证的示例

本目录保存书中四类关键示例的单一真相源：Compose、Dockerfile、Kubernetes 清单和 GitHub Actions 工作流。`tools/test_examples.py` 会调用这些工具各自的原生校验命令；CI 中缺少任一工具都会失败，本地环境缺少工具则明确报告 `SKIP`。

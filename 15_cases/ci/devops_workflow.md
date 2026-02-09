## DevOps 工作流完整示例

本章将演示一个基于 Docker, Kubernetes 和 Jenkins/GitLab CI 的完整 DevOps 工作流。

### 工作流概览

1. **Code**: 开发人员提交代码到 GitLab。
2. **Build**: GitLab CI 触发构建任务。
3. **Test**: 运行单元测试和集成测试。
4. **Package**: 构建 Docker 镜像并推送到 Harbor/Registry。
5. **Deploy (Staging)**: 自动部署到测试环境 Kubernetes 集群。
6. **Verify**: 人工或自动化验证。
7. **Release (Production)**: 审批后自动部署到生产环境。

### 关键配置示例

#### 1. Dockerfile 多阶段构建

使用 Docker 多阶段构建可以有效减小镜像体积。


Dockerfile 内容如下：

```dockerfile
## Build stage

FROM golang:1.18 AS builder
WORKDIR /app
COPY . .
RUN go build -o main .

## Final stage

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/main .
CMD ["./main"]
```

#### 2. GitLab CI 配置

GitLab CI（.gitlab-ci.yml）配置如下：


```yaml
stages:
  - test
  - build
  - deploy

unit_test:
  stage: test
  image: golang:1.18
  script:
    - go test ./...

build_image:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

deploy_staging:
  stage: deploy
  image: dtzar/helm-kubectl
  script:
    - kubectl config set-cluster k8s --server=$KUBE_URL --insecure-skip-tls-verify=true
    - kubectl config set-credentials admin --token=$KUBE_TOKEN
    - kubectl config set-context default --cluster=k8s --user=admin
    - kubectl config use-context default
    - kubectl set image deployment/myapp myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA -n staging
  only:
    - develop
```

### 最佳实践

1. **不可变基础设施**: 一旦镜像构建完成，在各个环境（Dev, Staging, Prod）中都应该使用同一个镜像 tag (通常是 commit hash)，而不是重新构建。
2. **配置分离**: 使用 ConfigMap 和 Secret 管理环境特定的配置，不要打包进镜像。
3. **GitOps**: 考虑引入 ArgoCD，将部署配置也作为代码存储在 Git 中，实现 Git 驱动的部署同步。

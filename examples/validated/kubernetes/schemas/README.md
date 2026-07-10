# Kubernetes schema provenance

- schema set: `v1.31.0-standalone-strict`
- upstream: [`yannh/kubernetes-json-schema`](https://github.com/yannh/kubernetes-json-schema)
- upstream commit: `5e4d7a8ff7c9d783a27cf08ab2ba54a7dd8b8d03`
- source paths: `v1.31.0-standalone-strict/deployment-apps-v1.json` and `v1.31.0-standalone-strict/service-v1.json`
- vendoring transformation: append one POSIX terminal newline; JSON content is otherwise unchanged

Upstream SHA-256 before newline normalization:

- `deployment-apps-v1.json`: `3e3008f66a5f68cee3984485ac1892dbedc7f072b3a87064116bab294874e99e`
- `service-v1.json`: `f489d6102675238b913898caf6fef6f472403950fc9e5895ef718f3c4f1c4351`

Committed SHA-256 used by the offline validator:

- `deployment-apps-v1.json`: `d3b29ff1d1f202e33b9f0d3c9a2b777a4f45d5ff8210285e62e2c7bef1d09057`
- `service-v1.json`: `314be70ae72a72233561ed3dbeeba71e64cf84004ab611ca1727d5384bf400ed`

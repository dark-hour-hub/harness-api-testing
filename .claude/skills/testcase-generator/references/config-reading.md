# 配置读取

## config.yaml 读取规则

### 后端项目

遍历 `source.backend[]`，跳过 `enabled: false` 的项。每个 `path` 是一个独立项目，单独生成用例。

### 当前环境

`current_environment` 的值作为 key，从 `environments` 中取对应配置。

### base_url

`environments.${current_environment}.backend[]` 中与 `source.backend[].name` 匹配的 `url`。

若一个项目对应多个 backend 条目（微服务），分别记录各服务的 base_url。

### 测试账号

从 `accounts[]` **原样读取所有字段**，不修改字段名或值。不同项目的账号字段可能不同（如有的含 username/password，有的还含额外的认证参数如 clientKey/tenantId 等），保持原样。

### 输出

每个项目提取出：
- `source_path`：源码根目录
- `base_url`：当前环境的基础 URL
- `accounts`：账号列表（原样）
- `services`：多服务时各服务的 name → url 映射

---
name: api-doc-assemble
description: 回填主文档模块概览、汇总已知问题、校验模块文档完整性。读取主文档骨架 + _manifest.yaml + 所有 modules/*.md，统计实际接口数，回填主文档，验证链接和格式。触发：api-doc 全流程最后一步、/api-doc-assemble。
---

# API 文档汇总与校验

回填主文档的模块概览表和已知问题，校验模块文档的完整性。

## 前置输入

1. `tests/baseline/_workflow/03-api-docs/API接口文档.md` — 主文档骨架
2. `tests/baseline/_workflow/03-api-docs/_manifest.yaml` — 模块清单
3. `tests/baseline/_workflow/03-api-docs/modules/` — 所有模块文档
4. `tests/baseline/_workflow/03-api-docs/entities/_index.yaml` — 实体索引

## 输出产物

- 更新 `API接口文档.md`（回填模块概览 + 已知问题）
- 可选：更新 `_manifest.yaml`（回写实际接口数）

---

## 流程

### Step 1 — 扫描模块文档统计实际接口数

对 `modules/` 目录下每个 `.md` 文件，用正则 `^### \d+ ` 统计实际接口数。

### Step 2 — 回填主文档"模块概览"表

用 Step 1 的实际数据更新模块概览表，每行包含：

| 模块 | 路由前缀 | 接口数量 | 说明 | 文档链接 |

- 文档链接使用相对路径 `modules/{文件名}.md`
- 接口数量使用实际统计值
- 确保表行数 = 模块文件数

### Step 3 — 汇总已知问题

从所有 Agent 的生成过程中收集已知问题，写入"已知问题与注意事项"表：

| # | 问题 | 影响接口/模块 | 说明 | 建议 |

常见问题类型：
- **类名不一致**：manifest 预期类名 vs 源码实际类名
- **权限缺失**：模块无 @SaCheckPermission 注解
- **返回类型差异**：预期 vs 实际
- **缺失实体**：manifest 列出但源码不存在的 DTO/VO

从 `entities/_index.yaml` 的 `corrections` 字段和 Agent 返回结果中提取。

### Step 4 — 模块文档格式校验

对每个模块文档，检查以下规则（输出问题列表但不自动修改）：

- [ ] 接口数 > 0
- [ ] 无摘要表格（搜索"其余接口"、"接口.*略"、"以下略"）
- [ ] 无内联字段替代实体引用（搜索 `（含.*等.*字段）` 正则）
- [ ] 每个文档有 `#### 请求` 和 `#### 响应` 标题
- [ ] 每个文档有请求头引用块（`[认证]` 或 `[公开]`）
- [ ] 无未替换 `{xxx}` 占位符

### Step 5 — 更新 manifest

将 Step 1 的实际接口数回写到 `_manifest.yaml` 每个模块的 `interface_count` 字段。

---

## 禁止

- 修改模块文档内容（只读校验）
- 重新读取源码或调用 CodeGraph
- 生成新的模块文档

# 覆盖度计算规则

Phase D 用于量化评估每个模块的用例覆盖度。预计值在 Phase A2 步骤 4 预计算，写入 shared-context.yaml §6 每条路由的 `expected` 字段。Phase D 据此与实际产出对比。

## 预期用例数计算公式

### 正向用例

| 条件 | 最低 (min_positive) | 理想 (ideal_positive) |
|------|--------------------|-----------------------|
| 所有路由 | 1 | 1 |
| 路由有可选字段（DTO 中至少一个字段 required=false） | - | 额外 +1（仅必填参数变体） |

### 反向用例

| 条件 | 最低 (min_negative) | 理想 (ideal_negative) |
|------|--------------------|-----------------------|
| `auth_probe_code ≠ 200`（路由需认证） | +1（无 token） | +1 |
| 每个 DTO 字段标记 `required: true`（@NotBlank/@NotNull/@NotEmpty） | +1（缺该字段） | +1 |
| GET/{id}、PUT、DELETE 路由 | +1（资源不存在） | +1 |
| 每个 DTO 字段有 @Length/@Size/@Min/@Max 约束 | - | 额外 +1（边界值） |
| 每个 DTO 字段有 @Email/@Pattern 约束 | - | 额外 +1（格式错误） |
| 每个 DTO 枚举字段 | - | 额外 +1（非法枚举值） |
| 接口依赖 SMS/Email/OSS 等外部服务且 `environment.capabilities` 标记 `false` | 取 1 条代表性用例（不是每个接口各 1） | +1 |

### 汇总

```
min_total = Σ(min_positive + min_negative)  # 所有路由求和
ideal_total = Σ(ideal_positive + ideal_negative)
```

## 实际覆盖统计

从 YAML 中提取：

```
actual_positive[route] = count(用例 tags 含 "正常" AND 匹配该 route)
actual_negative[route] = count(用例 tags 含 "异常" AND 匹配该 route)
actual_total = Σ(actual_positive + actual_negative)
```

## 评分公式

对每个模块独立计算：

```
positive_coverage = count(routes where actual_positive[route] >= min_positive[route]) / total_routes
negative_coverage = min(actual_total_negative / expected_min_total_negative, 1.0)

score = positive_coverage × 0.5 + negative_coverage × 0.5
```

## 判定矩阵

| 评分 | 判定 | 动作 |
|------|------|------|
| ≥ 1.0 | **通过** | 进入交付 |
| 0.7 – 0.99 | **警告** | 记录风险，允许交付但标注 |
| < 0.7 | **不通过** | 触发返工（D4） |

### 硬性红线（触发即不通过，无视评分数值）

1. **正向缺漏**：任一模块存在路由完全没有正向用例（positive_coverage < 1.0）
2. **必填字段漏洞**：任一模块的必填字段反向覆盖 < 50%（即超过一半的必填字段没有对应反向用例）

## 返工策略

| 缺口 | Agent prompt 要点 |
|------|------------------|
| 正向缺失 | 列出缺失路由，各生成 1 条，追加到 YAML |
| 反向缺失（必填字段） | 列出缺失字段 + 所属路由，各生成 1 条"缺该字段"用例 |
| 反向缺失（认证/资源不存在/外部依赖） | 列出缺失类型 + 所属路由，按 case-design.md 补齐 |

返工后重新执行 D1-D3，最多循环 2 次。2 次后仍不通过 → 记录"人工介入"到报告。

## 示例

### POST /system/user（DTO: SysUserBo，假设 3 个必填字段 + 2 个 @Length 约束 + auth_probe_code=401）

```
min_positive:  1  (完整参数)
min_negative:  5  (1 无token + 3 缺必填 + 1 资源不存在)
ideal_positive: 2  (完整参数 + 仅必填参数)
ideal_negative: 7  (5 最低 + 2 边界值)
---
min_total:     6
ideal_total:   9
```

### GET /system/user/list（DTO: SysUserBo 用于查询参数，auth_probe_code=200）

```
min_positive:  1  (正常分页查询)
min_negative:  0  (auth_probe_code=200 无认证用例)
ideal_positive: 1
ideal_negative: 0
---
min_total:     1
ideal_total:   1
```

### GET /system/user/{userId}（无 DTO，auth_probe_code=401）

```
min_positive:  1  (查询存在用户)
min_negative:  2  (1 无token + 1 资源不存在)
ideal_positive: 1
ideal_negative: 2
---
min_total:     3
ideal_total:   3
```

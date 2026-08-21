---
name: yaml-to-jmx
description: 从性能场景 YAML（perf-scenario.yaml）生成 JMeter .jmx 压测脚本。触发：/yaml-to-jmx、YAML转jmx、生成jmx脚本、生成压测脚本、yaml to jmx、generate jmeter script、生成性能测试脚本。
---

# 性能场景 YAML → JMeter .jmx 生成器

从性能场景 YAML 定义生成可执行的 JMeter 5.x 测试计划（`.jmx`）。

## 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|:---:|--------|------|
| `mode` | enum | 否 | `baseline` | `baseline` = 全量模式；`diff` = 增量模式 |

路径决议（按 mode）：

| 路径变量 | `baseline` | `diff` |
|---------|----------|--------|
| `YAML_DIR` | `tests/baseline/_workflow/05-perf-scenarios` | `tests/diff/_workflow/03-diff-perf-scenarios` |
| `OUTPUT_DIR` | `tests/baseline/generated/api-perf` | `tests/diff/generated/api-perf` |

## 输入

| 来源 | 路径 | 用途 |
|------|------|------|
| 性能场景 YAML | `${YAML_DIR}/*.yaml` | 场景定义（字段见 api-doc-to-perf/references/perf-schema.md） |
| 片段模板 | `template/jmx_fragments.py` | JMeter 元素 XML 片段 |

## 输出

```
${OUTPUT_DIR}/
├── perf_auth_001.jmx       # 每个场景一个独立 jmx（单 ThreadGroup）
├── perf_user_001.jmx
├── _scenarios.json         # 场景清单（jmx → id/title/thresholds/load）
└── ...
```

每个 scenario 生成一个独立 `.jmx`（文件名 = `{scenario_id}.jmx` 小写），
同时输出 `_scenarios.json` 清单，供 perf-runner 读取 thresholds / load 元信息。

## 生成规则

- 每个 scenario → 独立 jmx，单 `ThreadGroup`（`users` / `ramp_up` / `duration`）
- `base_url` 解析为 `protocol` / `domain` / `port` 写入 HTTPSampler
- 主请求 sampler `testname` = scenario id（作为 .jtl 的 label，统计时据此区分场景）
- `auth.required: true` 时自动生成：
  - `OnceOnlyController`（每个并发线程只登录一次）
  - 登录 HTTPSampler（`testname` = `login`，`login_endpoint` + `login_body`）
  - JSON Extractor（`token_jsonpath` → `${token}`）
- 认证头放在主请求 sampler 子树内，只作用主请求，不污染登录请求
- POST/PUT/PATCH 用 Raw Post Body（JSON）；GET 用查询参数

## 执行

```bash
# 全量模式（默认）
python .opencode/skills/yaml-to-jmx/scripts/generate_jmx.py --mode baseline

# 增量模式
python .opencode/skills/yaml-to-jmx/scripts/generate_jmx.py --mode diff

# 显式指定路径（优先级高于 --mode）
python .opencode/skills/yaml-to-jmx/scripts/generate_jmx.py \
  --yaml-dir tests/baseline/_workflow/05-perf-scenarios \
  --output-dir tests/baseline/generated/api-perf
```

生成后自动用 ElementTree 校验每个 `.jmx` 的 XML well-formed。

## 禁止项

- 禁止在 `.jmx` 中硬编码账号密码以外的业务数据（账号密码来自 YAML `auth_setup`）
- 禁止修改 `jmx_fragments.py` 中已对齐的 JMeter 元素结构（缩进/属性名）
- 禁止生成不存在的 YAML 字段引用

# 测试生成计划

**模块**: <module_name>
**生成时间**: <generated_timestamp>
**基于分析**: <apis.json路径>

## 测试范围

### 模块概述
- 模块名称: <模块中文名>
- 模块路径: <源码路径>
- API 数量: <数量>

### 测试对象
| 类型 | 数量 | 说明 |
|------|------|------|
| API 接口 | <N> | 包含 CRUD 和业务接口 |
| Controller | <N> | 控制器数量 |
| Service | <N> | 服务层接口 |

## 测试类型

### API 接口测试
- **数量**: <N> 个接口
- **覆盖**:
  - 正向用例: 验证正常业务逻辑
  - 反向用例: 验证异常处理和错误提示
  - 安全用例: 验证权限和认证

### 测试优先级

| 优先级 | 数量 | 说明 |
|--------|------|------|
| P0 | <N> | 核心业务流程，必须通过 |
| P1 | <N> | 主要功能，正常场景 |
| P2 | <N> | 边界条件，详细验证 |

## 预计脚本数量

### 按模块统计

| 模块 | 接口数 | 用例数 | 预计脚本 |
|------|--------|--------|----------|
| <module1> | <N> | <M> | test_<module1>.py |
| <module2> | <N> | <M> | test_<module2>.py |

### 按测试类型统计

| 测试类型 | 用例数 | 占比 |
|----------|--------|------|
| 正向用例 | <N> | <X>% |
| 反向用例 | <N> | <X>% |
| 安全用例 | <N> | <X>% |

## 测试数据

### 认证信息
```yaml
admin:
  username: admin
  password: macro123
  token: ${admin_token}

test_user:
  username: testuser_${timestamp}
  password: Test123456
```

### 测试数据变量
| 变量名 | 说明 | 生成方式 |
|--------|------|----------|
| ${timestamp} | 时间戳 | datetime.now().strftime("%Y%m%d%H%M%S") |
| ${login_token} | 登录Token | 动态获取 |
| ${admin_token} | 管理员Token | 动态获取 |

## 输出文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 分析报告 | tests/baseline/specs/{module}/*-analysis.md | 源码分析结果 |
| 规格文件 | tests/baseline/specs/{module}/*-spec.yaml | API规格定义 |
| 接口文件 | tests/baseline/_workflow/02-analysis-plan/apis.json | 完整API信息 |
| 测试计划 | tests/baseline/_workflow/02-analysis-plan/generation-plan.md | 本文件 |
| 测试用例 | tests/baseline/_workflow/02-analysis-plan/testcases/{module}-testcases.yaml | YAML用例 |
| pytest脚本 | tests/baseline/api/{module}/test_*.py | 生成的pytest代码 |

## 执行顺序

1. **前置准备**
   - [ ] 初始化数据库
   - [ ] 启动服务
   - [ ] 获取认证Token

2. **测试执行**
   - [ ] 执行 P0 级用例（冒烟测试）
   - [ ] 执行 P1 级用例（回归测试）
   - [ ] 执行 P2 级用例（详细测试）

3. **测试清理**
   - [ ] 清理测试数据
   - [ ] 恢复环境

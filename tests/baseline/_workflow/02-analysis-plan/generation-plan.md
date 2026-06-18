# 测试生成计划

**模块**: ums (用户管理系统)
**生成时间**: 2026-06-18T10:00:00
**基于分析**: tests/baseline/_workflow/02-analysis-plan/apis.json

## 测试范围

### 模块概述
- 模块名称: 用户管理系统 (UMS)
- 模块路径: D:/java/project/mall-tiny
- API 数量: 41
- Controller 数量: 5

### 测试对象
| 类型 | 数量 | 说明 |
|------|------|------|
| API 接口 | 41 | 包含 CRUD 和业务接口 |
| Controller | 5 | UmsAdminController, UmsRoleController, UmsMenuController, UmsResourceController, UmsResourceCategoryController |
| Service | 5 | 对应5个Service接口及实现 |

## 测试类型

### API 接口测试
- **数量**: 41 个接口
- **覆盖**:
  - 正向用例: 验证正常业务逻辑 (每个API 1个核心正向用例)
  - 反向用例: 验证异常处理和错误提示 (必填项缺失、无效参数、错误密码等)
  - 安全用例: 验证权限和认证 (无Token、过期Token)

### 测试优先级

| 优先级 | 数量 | 说明 |
|--------|------|------|
| P0 | 12 | 核心业务流程：登录、注册、CRUD核心路径 |
| P1 | 40 | 主要功能：列表查询、状态修改、角色/菜单/资源分配 |
| P2 | 30 | 边界条件：空值、特殊字符、分页边界、参数格式校验 |

## 预计脚本数量

### 按模块统计

| 模块 | 接口数 | 用例数 | 预计脚本 |
|------|--------|--------|----------|
| ums | 41 | 82 | test_ums.py |

### 按测试类型统计

| 测试类型 | 用例数 | 占比 |
|----------|--------|------|
| 正向用例 | 41 | 50% |
| 反向用例 | 31 | 38% |
| 安全用例 | 5 | 6% |
| 清理用例 | 5 | 6% |

## 测试数据

### 认证信息
```yaml
admin:
  username: macro
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
| ${test_user_id} | 测试创建的用户ID | CREATE用例产生 |
| ${test_role_id} | 测试创建的角色ID | CREATE用例产生 |
| ${test_menu_id} | 测试创建的菜单ID | CREATE用例产生 |
| ${test_resource_id} | 测试创建的资源ID | CREATE用例产生 |
| ${test_category_id} | 测试创建的分类ID | CREATE用例产生 |

## 输出文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 分析报告 | tests/baseline/specs/ums/ums-analysis.md | 源码分析结果 ✓ |
| 规格文件 | tests/baseline/specs/ums/ums-spec.yaml | API规格定义 ✓ |
| 接口文件 | tests/baseline/_workflow/02-analysis-plan/apis.json | 完整API信息 ✓ |
| 测试计划 | tests/baseline/_workflow/02-analysis-plan/generation-plan.md | 本文件 |
| 测试用例 | tests/baseline/_workflow/02-analysis-plan/testcases/ums-testcases.yaml | YAML用例 |
| pytest脚本 | tests/baseline/generated/api-test/test_ums.py | 生成的pytest代码 |

## 执行顺序

1. **前置准备**
   - [ ] 确认 mall-tiny 服务运行在 http://localhost:8080
   - [ ] 获取 admin 登录 Token

2. **测试执行**
   - [ ] 执行 P0 级用例（登录、注册、核心CRUD）
   - [ ] 执行 P1 级用例（列表查询、状态修改、分配操作）
   - [ ] 执行 P2 级用例（边界值、参数校验、特殊字符）
   - [ ] 执行清理用例（DELETE cleanup、REVERT）

3. **测试清理**
   - [ ] 删除测试创建的用户
   - [ ] 删除测试创建的角色
   - [ ] 恢复修改的数据

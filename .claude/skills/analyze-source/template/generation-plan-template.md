# 源码分析计划

**模块**: <module_name>
**生成时间**: <timestamp>
**分析方式**: CodeGraph 深度源码分析

---

## 一、分析范围

| 类型 | 数量 | 说明 |
|------|------|------|
| 后端源码 | <N> | Java/Python/Node.js 源码目录 |
| Controller | <N> | 控制器数量 |
| API 接口 | <N> | 接口数量 |
| DTO/VO 类 | <N> | 请求体和响应体结构 |

## 二、技术栈

| 类型 | 框架 | 说明 |
|------|------|------|
| 后端 | <框架> | <版本> |
| 前端 | <框架> | <版本> |
| 数据库 | <数据库> | <版本> |
| 认证框架 | <框架> | <说明> |

## 三、校验规则提取

从代码中提取的字段校验规则（用于生成边界值用例）：

| 字段 | 类型 | 必填 | 校验规则 | 来源 |
|------|------|------|----------|------|
| username | string | true | maxLength=32, minLength=3 | @Length |
| email | string | false | format=email | @Email |
| age | integer | false | min=0, max=150 | @Min/@Max |

## 四、错误消息追踪

从代码追踪的真实错误消息（用于生成反向用例断言）：

| 场景 | Code | Message | 追踪路径 |
|------|------|---------|----------|
| 用户名为空 | 500 | 用户名不能为空 | Controller → @NotBlank |
| 邮箱格式错误 | 500 | 邮箱格式不正确 | Controller → @Email |
| 资源不存在 | 404 | 请求地址不存在 | GlobalExceptionHandler |

## 五、输出文件

| 文件 | 路径 |
|------|------|
| 分析报告 | tests/baseline/specs/{module}/*-analysis.md |
| 规格文件 | tests/baseline/specs/{module}/*-spec.yaml |
| 接口文件 | tests/baseline/_workflow/02-analysis-plan/apis.json |
| 生成计划 | tests/baseline/_workflow/02-analysis-plan/generation-plan.md |

## 六、下一步

使用 `test-case-generator` skill 生成测试用例 YAML。

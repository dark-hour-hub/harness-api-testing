# SysUserProfileBo -- 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysUserProfileBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysUserProfileBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 系统管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置（继承 BaseEntity） |
| **说明** | 个人信息修改请求对象，用于 `/system/user/profile` 修改当前登录用户的基本信息（昵称、邮箱、手机、性别） |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| searchValue | `searchValue` | string | 否 | — | — | 搜索值（不参与序列化 `@JsonIgnore`） | — |
| createDept | `createDept` | number | 否 | 插入时自动填充 | — | 创建部门 | `103` |
| createBy | `createBy` | number | 否 | 插入时自动填充 | — | 创建者 | `1` |
| createTime | `createTime` | string | 否 | 插入时自动填充 | — | 创建时间 | `"2026-07-14 10:00:00"` |
| updateBy | `updateBy` | number | 否 | 插入/更新时自动填充 | — | 更新者 | `1` |
| updateTime | `updateTime` | string | 否 | 插入/更新时自动填充 | — | 更新时间 | `"2026-07-14 12:00:00"` |
| params | `params` | object | 否 | — | `{}` | 请求参数 | — |
| nickName | `nickName` | string | 否 | `@Xss`（防脚本注入）；`@Size(min=0, max=30)` | — | 用户昵称 | `"张三"` |
| email | `email` | string | 否 | `@Email`；`@Size(min=0, max=50)`；`@Sensitive(strategy=EMAIL)` | — | 用户邮箱（脱敏存储，策略 EMAIL） | `"zhangsan@example.com"` |
| phonenumber | `phonenumber` | string | 否 | `@Pattern(regexp=RegexConstants.MOBILE)`；`@Sensitive(strategy=PHONE)` | — | 手机号码（正则校验 `RegexConstants.MOBILE`，脱敏策略 PHONE） | `"13800138001"` |
| sex | `sex` | string | 否 | — | — | 用户性别（`0` 男、`1` 女、`2` 未知） | `"0"` |

**字段备注**:
- `email`: 标注 `@Sensitive(strategy = SensitiveStrategy.EMAIL)`，以脱敏形式存储/返回
- `phonenumber`: 标注 `@Pattern(regexp = RegexConstants.MOBILE)`（正则校验手机号格式）和 `@Sensitive(strategy = SensitiveStrategy.PHONE)`

---

## JSON 示例

```json
{
  "nickName": "张三",
  "email": "zhangsan@example.com",
  "phonenumber": "13800138001",
  "sex": "0"
}
```

---

*基于 `org.dromara.system.domain.bo.SysUserProfileBo` 源码生成 * 2026-07-14*

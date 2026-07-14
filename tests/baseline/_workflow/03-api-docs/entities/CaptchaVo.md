# CaptchaVo — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `CaptchaVo` |
| **全限定名** | `org.dromara.web.domain.vo.CaptchaVo` |
| **类型** | 响应体 VO |
| **所属模块** | 认证模块 (auth) |
| **父类** | 无 |
| **序列化特性** | 无特殊配置 |
| **说明** | 验证码响应体，返回验证码开关状态、唯一标识及验证码图片（Base64） |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| captchaEnabled | `captchaEnabled` | boolean | — | — | `true` | 验证码开关，`true` 表示当前系统启用验证码功能 | `true` |
| uuid | `uuid` | string | — | — | — | 唯一标识，前端登录时需将此值回传，用于关联 Redis 中的验证码缓存 | `"a1b2c3d4e5f6"` |
| img | `img` | string | — | — | — | 验证码图片 Base64 编码字符串，前端可直接渲染为图片 | `"data:image/gif;base64,R0lGODlh..."` |

---

## JSON 示例

```json
{
  "captchaEnabled": true,
  "uuid": "a1b2c3d4e5f6",
  "img": "data:image/gif;base64,R0lGODlh..."
}
```

---

*基于 `org.dromara.web.domain.vo.CaptchaVo` 源码生成 · 2026-07-14*

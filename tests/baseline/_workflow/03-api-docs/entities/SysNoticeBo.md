# SysNoticeBo — 请求体 DTO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysNoticeBo` |
| **全限定名** | `org.dromara.system.domain.bo.SysNoticeBo` |
| **类型** | 请求体 DTO |
| **所属模块** | 系统管理 |
| **父类** | `BaseEntity` |
| **序列化特性** | 无特殊配置 |
| **说明** | 通知公告业务对象，用于通知/公告的新增、修改、查询等操作的请求参数绑定 |

---

## 字段定义

### 请求体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| noticeId | `noticeId` | number | 否 | — | — | 公告ID（修改时必传） | `1` |
| noticeTitle | `noticeTitle` | string | 是 | `@NotBlank`, `@Xss`（禁止脚本字符）, `@Size(min=0, max=50)` | — | 公告标题 | `"关于系统升级的通知"` |
| noticeType | `noticeType` | string | 否 | — | — | 公告类型（1=通知, 2=公告） | `"1"` |
| noticeContent | `noticeContent` | string | 否 | — | — | 公告内容（支持富文本 HTML） | `"<p>系统将于2024年7月...</p>"` |
| status | `status` | string | 否 | — | — | 公告状态（0=正常, 1=关闭） | `"0"` |
| remark | `remark` | string | 否 | — | — | 备注 | `""` |
| createByName | `createByName` | string | 否 | — | — | 创建人名称（仅用于接收参数，不持久化） | `""` |
| createDept | `createDept` | number | 否 | — | 自动填充 | 创建部门（数据库自动填充） | `103` |
| createBy | `createBy` | number | 否 | — | 自动填充 | 创建者（数据库自动填充） | `1` |
| createTime | `createTime` | string | 否 | — | 自动填充 | 创建时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-01-15 10:30:00"` |
| updateBy | `updateBy` | number | 否 | — | 自动填充 | 更新者（数据库自动填充） | `1` |
| updateTime | `updateTime` | string | 否 | — | 自动填充 | 更新时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-06-20 14:00:00"` |
| params | `params` | object | 否 | — | `{}` | 请求参数（扩展查询条件，非空时才序列化，不映射数据库字段） | `{}` |

**字段备注**:
- `searchValue` (继承自 `BaseEntity`): `@JsonIgnore` 标记，不参与序列化，不映射数据库字段，仅用于前端搜索框传值。
- `noticeTitle`: 带 `@Xss` 校验，禁止包含 `<script>` 等脚本字符，防止 XSS 攻击。
- `noticeContent`: 公告内容通常为富文本 HTML，长度无限制，前端一般使用编辑器组件。
- `createDept` / `createBy` / `createTime`: 继承自 `BaseEntity`，由 MyBatis-Plus 在 INSERT 时自动填充。
- `updateBy` / `updateTime`: 继承自 `BaseEntity`，由 MyBatis-Plus 在 INSERT 和 UPDATE 时自动填充。
- `params`: 继承自 `BaseEntity`，`@JsonInclude(NON_EMPTY)`。

---

## JSON 示例

```json
{
  "noticeTitle": "关于系统升级的通知",
  "noticeType": "1",
  "noticeContent": "<p>系统将于2024年7月20日进行升级维护，届时请勿登录系统。</p>",
  "status": "0"
}
```

---

*基于 `org.dromara.system.domain.bo.SysNoticeBo` 源码生成 · 2026-07-14*

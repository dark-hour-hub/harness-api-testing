# SysNoticeVo — 响应体 VO

## 基本信息

| 属性 | 值 |
|------|-----|
| **类名** | `SysNoticeVo` |
| **全限定名** | `org.dromara.system.domain.vo.SysNoticeVo` |
| **类型** | 响应体 VO |
| **所属模块** | 系统管理 |
| **父类** | 无（直接实现 `Serializable`） |
| **序列化特性** | 无特殊配置 |
| **说明** | 通知公告视图对象，用于通知/公告列表查询、详情查看等接口的响应数据封装 |

---

## 字段定义

### 响应体字段

| 字段路径 | JSON 键名 | 类型 | 必填 | 约束/校验规则 | 默认值 | 说明 | 示例值 |
|----------|-----------|------|:---:|------------|--------|------|--------|
| noticeId | `noticeId` | number | — | — | — | 公告ID | `1` |
| noticeTitle | `noticeTitle` | string | — | — | — | 公告标题 | `"关于系统升级的通知"` |
| noticeType | `noticeType` | string | — | — | — | 公告类型（1=通知, 2=公告） | `"1"` |
| noticeContent | `noticeContent` | string | — | — | — | 公告内容（富文本 HTML） | `"<p>系统将于2024年7月...</p>"` |
| status | `status` | string | — | — | — | 公告状态（0=正常, 1=关闭） | `"0"` |
| remark | `remark` | string | — | — | — | 备注 | `""` |
| createBy | `createBy` | number | — | — | — | 创建者ID | `1` |
| createByName | `createByName` | string | — | — | — | 创建人名称（通过 `@Translation` 从 `createBy` 自动翻译） | `"管理员"` |
| createTime | `createTime` | string | — | — | — | 创建时间（格式: yyyy-MM-dd HH:mm:ss） | `"2024-01-15 10:30:00"` |

**字段备注**:
- `createByName`: 由 `@Translation(type=USER_ID_TO_NAME, mapper="createBy")` 翻译注解自动填充，根据 `createBy` 用户ID 查询用户名称。
- `noticeType`: 1=通知（一般信息）, 2=公告（重要声明）。
- `status`: 0=正常（显示在前端）, 1=关闭（不显示）。

---

## JSON 示例

```json
{
  "noticeId": 1,
  "noticeTitle": "关于系统升级的通知",
  "noticeType": "1",
  "noticeContent": "<p>系统将于2024年7月20日进行升级维护，届时请勿登录系统。</p>",
  "status": "0",
  "remark": "",
  "createBy": 1,
  "createByName": "管理员",
  "createTime": "2024-01-15 10:30:00"
}
```

---

*基于 `org.dromara.system.domain.vo.SysNoticeVo` 源码生成 · 2026-07-14*

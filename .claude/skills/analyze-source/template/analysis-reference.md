# 分析参考

## Java 类型 → JSON Schema 类型映射

| Java 类型 | JSON Schema 类型 |
|-----------|------------------|
| String | string |
| Integer, Long | integer |
| BigDecimal | number |
| Boolean | boolean |
| List<?> | array |
| Map<?,?> | object |
| LocalDateTime | string (datetime) |
| MultipartFile | file |

## DTO/VO 分析流程

```
Controller (@RequestBody UserDTO)
    ↓
UserDTO.java (分析类源码)
    ├── String username (@NotBlank, @Length(max=32))
    ├── String password (@NotBlank, @Length(min=6,max=128))
    ├── String email (@Email)
    └── List<String> roles
    ↓
request_body:
  properties:
    username: {type: string, required: true, maxLength: 32}
    password: {type: string, required: true, minLength: 6, maxLength: 128}
    email: {type: string, format: email}
    roles: {type: array, items: {type: string}}

Result<UserVO> (分析返回值)
    ↓
UserVO.java (分析类源码)
    ├── Long id
    ├── String username
    ├── String email
    └── LocalDateTime createTime
    ↓
response_fields:
  properties:
    code: {type: integer}
    message: {type: string}
    data:
      properties:
        id: {type: integer}
        username: {type: string}
        email: {type: string}
        createTime: {type: string, format: datetime}
```

## 常见 DTO/VO 命名模式

| 类型 | 命名模式 | 所在目录 |
|------|----------|---------|
| 请求DTO | `*DTO`, `*Request`, `*Command` | `dto/`, `request/`, `command/` |
| 响应VO | `*VO`, `*Response`, `*Result` | `vo/`, `response/` |
| 业务对象 | `*BO` | `bo/` |
| 分页对象 | `*Page`, `*PageDTO` | 继承 `PageImpl` 或类似 |

## 必填字段判定

- 字段有 `@NotNull`, `@NotBlank`, `@NotEmpty` 注解 → `required: true`
- 主键字段（id）通常 → `required: false`（创建时）
- 无校验注解 → `required: false`

## CodeGraph 查找 DTO/VO

```bash
codegraph_search "UserDTO"
codegraph_search "UserVO"
```

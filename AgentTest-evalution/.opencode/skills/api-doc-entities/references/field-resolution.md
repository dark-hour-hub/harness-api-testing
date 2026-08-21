# 字段名解析

确定 Java DTO/VO 字段对应的 JSON 键名。Java 字段名 ≠ JSON 键名——必须检查序列化注解。

## JSON 键名优先级链

按以下顺序查找，命中即停止：

| 优先级 | 来源 | 示例 |
|--------|------|------|
| 1 | 字段级注解 | `@JsonProperty("userName")` → JSON 键 `"userName"` |
| 1 | | `@JSONField(name="userName")` → JSON 键 `"userName"` |
| 1 | | `@SerializedName("userName")` → JSON 键 `"userName"` |
| 2 | 类级命名策略 | `@JsonNaming(SnakeCaseStrategy.class)` → `user_name` → `"userName"` |
| 3 | 全局配置 | `spring.jackson.property-naming-strategy: SNAKE_CASE`（查 application.yml） |
| 4 | 默认 | Java 字段名即为 JSON 键名（Jackson 默认） |

## 请求体字段（DTO）

1. 从 Controller 的 `@RequestBody` 参数找到 DTO 全限定名
2. 用 `codegraph_node` 读取 DTO 源码，列出所有字段及其类型
3. 按优先级链确定每个字段的 JSON 键名
4. 从校验注解确定必填/可选：
   - 必填：`@NotNull`, `@NotBlank`, `@NotEmpty`
   - 约束：`@Length`, `@Size`, `@Pattern`, `@Min`, `@Max`, `@Email` 等
5. DTO 有父类 → 递归追踪父类字段
6. 有 `@Valid` 嵌套对象 → 递归追踪嵌套 DTO

## 响应体字段（VO）

1. 从 Controller 返回类型泛型获取 VO 全限定名（`R<XxxVo>` → `XxxVo`）
2. 用 `codegraph_node` 读取 VO 源码
3. 按优先级链确定 JSON 键名
4. 返回 `R<Void>` 或无泛型 → data 为 null，无法 extract
5. `@JsonInclude(Include.NON_NULL)` → null 字段不返回

## 特殊类型处理

### 枚举

- `@JsonValue` 注解的 getter → 序列化为该返回值
- 无注解 → `name()` 返回枚举常量名（字符串）

### 日期

- `@JsonFormat(pattern="yyyy-MM-dd HH:mm:ss")` → 按此格式
- 无注解 → 检查全局 Jackson 日期配置

### 泛型/嵌套

- `List<XxxVo>` → 数组中每个元素按 XxxVo 解析
- `Map<String, Object>` → value 类型不确定，按实际响应推断

## 类型映射

| Java 类型 | JSON 类型 |
|-----------|-----------|
| String, char, CharSequence | string |
| int, long, Integer, Long, BigInteger | number |
| float, double, BigDecimal | number |
| boolean, Boolean | boolean |
| List, Set, Array | array |
| Map, Object | object |
| Date, LocalDateTime | string/number（取决于配置） |
| Enum | string/number（取决于配置） |

# i18n 消息解析

## 适用场景

API 响应的 `business_message` 来源于项目的 i18n 消息文件（如 `messages.properties`），而非源码中直接写死的字符串。若 YAML 中直接写注解/代码里的 i18n key，运行时服务端返回的是翻译后的值，断言必然失败。

## 通用模式

三种来源的消息，最终到达客户端前都会经过 i18n 解析：

| 来源 | 原始形式 | 解析时机 | 最终输出 |
|------|---------|---------|---------|
| 校验注解 message | `{key}`（占位符） | Spring MessageSource / Validator 校验时 | properties 文件中的值 |
| 业务代码中 `MessageUtils.message(key)` | `key`（字符串） | MessageUtils 运行时调用 getMessage() | properties 文件中的值 |
| 硬编码字符串 | 字面字符串 | 无需解析 | 原值 |

**关键事实**：前两种来源中，原始 key 永远不会出现在 HTTP 响应中。必须从 properties 文件查找翻译后的值作为 YAML 的 `business_message`。

## 解析步骤

### 第一步：识别消息来源

**优先从 shared-context.yaml 的 `dto_index` 获取校验注解 message**（已预索引）。仅当 dto_index 未覆盖时，用 `codegraph_explore` 批量读取缺失的 DTO。

对每个错误路径，按以下顺序判断消息来源：

1. **校验注解**：从 dto_index（或批量读取的 DTO 源码）读字段上的 `@NotBlank`/`@NotNull`/`@Size` 等注解的 `message` 属性
   - 若值为 `{xxx}` 格式 → i18n key → 进入第二步
   - 若值为普通字符串（如 `"不能为空"`) → 直接用，无需查表
2. **异常抛出点**：追踪 `throw` 语句 → 看 `e.getMessage()` 的构造方式
   - 调了 `MessageUtils.message(key)` 或类似工具方法 → 提取 key → 进入第二步
   - 直接 `new XxxException("硬编码字符串")` → 直接用
   - 调了带参数的 i18n 方法 → 提取 key + 参数 → 进入第二步
3. **全局异常处理器的格式化**：检查 `@ExceptionHandler` 方法是否在运行时对原始消息做了二次加工（字段名拼接、固定前缀等）→ 最终 message 可能是 `处理后的格式`

### 第二步：定位 properties 文件

按以下优先级搜索项目中的 i18n 资源文件：

1. `{当前模块}/src/main/resources/i18n/messages_{locale}.properties`（当前运行时 locale 精确匹配，默认 `zh_CN`）
2. `{当前模块}/src/main/resources/i18n/messages.properties`（默认 locale 回退）
3. `{主应用模块}/src/main/resources/i18n/messages_{locale}.properties`
4. `{主应用模块}/src/main/resources/i18n/messages.properties`
5. 遍历各 `common` 模块下的 `i18n/` 目录，重复上述 locale 匹配
6. 搜索 `ValidationMessages.properties`（JSR-380 标准校验消息的 i18n，若存在）

> 对 properties 文件名的 locale 后缀，使用 `config.yaml` 中环境的 locale 设定（若配置），否则按服务端默认 `zh_CN` 处理。

### 第三步：查表解析

- key 匹配时**精确匹配**（不含 `{` `}` 包裹符）
- properties 文件使用 `ISO 8859-1` 编码，非 ASCII 字符以 `\uXXXX` Unicode 转义存储 → 读取时需解码
- 若 key 带参数（如 `java.lang.String.format` 风格 `%s`），记录格式化模式，YAML 中按模式填入预期值

### 第四步：Fallback

若在所有 properties 文件中均未找到对应 key：

- 非 i18n key 格式（不以 `{` 开头）→ **直接作为 `business_message`**
- i18n key 格式但未找到翻译 → 记录为 **TODO 项**，YAML 中保留原始 key，附加注释 `# TODO: i18n key not found in properties, verify manually`
- JSR-380 标准注解（`@NotNull`/`@NotBlank` 等）未指定 `message` → 使用 JSR-380 默认模板（参考 error-tracing.md 附录）

## 禁止

- 禁止假设 i18n key 就是最终返回的 message
- 禁止跳过 properties 文件搜索直接用注解 message
- 禁止仅在当前模块搜索 properties 文件而忽略主应用模块和 common 模块

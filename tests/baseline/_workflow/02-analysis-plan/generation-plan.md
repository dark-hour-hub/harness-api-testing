# 源码分析计划

**模块**: spring-petclinic
**生成时间**: 2026-07-10
**分析方式**: CodeGraph 深度源码分析

---

## 一、分析范围

| 类型 | 数量 | 说明 |
|------|------|------|
| 后端源码 | 1 | `D:\java\project\spring-petclinic` (Spring Boot) |
| Controller | 6 | OwnerController, PetController, VisitController, VetController, WelcomeController, CrashController |
| API 接口 | 17 | 全部为 GET/POST，无 PUT/DELETE 接口；100% 收录于 apis.json |
| 实体类 (Entity) | 8 | Owner, Pet, Visit, PetType, Vet, Specialty, Person, NamedEntity, BaseEntity |
| DTO/VO 类 | 0 | 该项目为传统 Spring MVC，直接使用 Entity 绑定表单，无独立 DTO/VO |
| Repository | 4 | OwnerRepository, PetTypeRepository, VetRepository（均为 Spring Data JPA） |

### 按模块分布

| 模块 | Controller | API 数量 | 说明 |
|------|-----------|---------|------|
| owner | 3 | 13 | Owner、Pet、Visit 的 CRUD 操作 |
| vet | 1 | 2 | 兽医列表（HTML + JSON） |
| system | 2 | 2 | 欢迎页、异常演示 |
| **合计** | **6** | **17** | — |

### 排除的路由

| 排除类型 | 数量 | 原因 |
|----------|------|------|
| 无 | 0 | CodeGraph 枚举的 17 条路由全部为业务路由，无不适用类型 |

## 二、技术栈

| 类型 | 框架 | 说明 |
|------|------|------|
| 后端 | Spring Boot 3.x | spring-boot-starter-web, spring-boot-starter-data-jpa |
| 模板引擎 | Thymeleaf | 服务端渲染 HTML 页面 |
| 数据库 | H2 (默认) / MySQL / PostgreSQL | 通过 spring.profiles.active 切换 |
| 缓存 | JCache | 仅对 vets 列表启用缓存 |
| 认证框架 | 无 | 无 Spring Security、无 Shiro，所有接口开放访问 |
| 前端框架 | Thymeleaf 模板 | 非 SPA，无 Vue/React |
| 校验框架 | Jakarta Bean Validation | @NotBlank, @Size, @Pattern + 自定义 PetValidator |
| 国际化 | Spring i18n + LocaleChangeInterceptor | 通过 ?lang= 参数切换语言 |
| 构建工具 | Maven | pom.xml |

## 三、校验规则提取

从代码中提取的字段校验规则（用于生成边界值用例）：

| 字段 | 类型 | 必填 | 校验规则 | 来源 |
|------|------|------|----------|------|
| firstName | string | true | maxLength=30, @NotBlank | Person.java @Size + @NotBlank |
| lastName | string | true | maxLength=30, @NotBlank | Person.java @Size + @NotBlank |
| address | string | true | @NotBlank | Owner.java |
| city | string | true | @NotBlank | Owner.java |
| telephone | string | true | @Pattern(regexp="\\d{10}") | Owner.java — 10位数字 |
| pet.name | string | true | @NotBlank (via NamedEntity), PetValidator required | PetValidator.java |
| pet.birthDate | date | true | PetValidator required, 不能在未来 | PetValidator + PetController |
| pet.type | object | true (新建时) | PetValidator required | PetValidator.java |
| visit.description | string | true | @NotBlank | Visit.java |
| visit.date | date | true | 必须在将来 (after today) | VisitController.processNewVisitForm |

## 四、错误消息追踪

从代码追踪的真实错误消息（用于生成反向用例断言）：

| 场景 | HTTP 状态 | 异常/消息 | 追踪路径 |
|------|----------|----------|----------|
| Owner 不存在 (GET) | 500 | `IllegalArgumentException`: "Owner not found with id: X. Please ensure the ID is correct and the owner exists in the database." | OwnerController.findOwner → orElseThrow |
| Owner 不存在 (POST) | 500 | `IllegalArgumentException`: "Owner not found with id: X. Please ensure the ID is correct " | PetController.findOwner → orElseThrow |
| Owner 不存在 (Visit) | 500 | `IllegalArgumentException`: "Owner not found with id: X. Please ensure the ID is correct " | VisitController.loadPetWithVisit → orElseThrow |
| Pet 不存在 | 500 | `IllegalArgumentException`: "Pet with id X not found for owner with id Y." | VisitController.loadPetWithVisit |
| 表单校验失败 (Owner 创建) | 200 | Flash error: "There was an error in creating the owner." | OwnerController.processCreationForm |
| 表单校验失败 (Owner 更新) | 200 | Flash error: "There was an error in updating the owner." | OwnerController.processUpdateOwnerForm |
| Owner ID 不匹配 | 302 | Flash error: "Owner ID mismatch. Please try again." | OwnerController.processUpdateOwnerForm |
| Pet 名称重复 | 200 | Field error: "already exists" (code: duplicate) | PetController.processCreationForm / processUpdateForm |
| Pet 日期在未来 | 200 | Field error: "typeMismatch.birthDate" | PetController.processCreationForm / processUpdateForm |
| Visit 日期不在将来 | 200 | Field error: "typeMismatch.visitDate" | VisitController.processNewVisitForm |
| 电话号码格式错误 | 200 | `{telephone.invalid}` (i18n 消息键) | Owner.java @Pattern |
| 必填字段为空 | 200 | "required" (PetValidator) / Bean Validation 默认消息 | PetValidator + @NotBlank |
| 异常演示 (/oups) | 500 | `RuntimeException`: "Expected: controller used to showcase what happens when an exception is thrown" | CrashController.triggerException |
| Owner 查找无结果 | 200 | Field error: "not found" (code: notFound) | OwnerController.processFindForm |

## 五、输出文件

| 文件 | 路径 |
|------|------|
| 分析报告 | tests/baseline/specs/spring-petclinic/spring-petclinic-analysis.md |
| 规格文件 | tests/baseline/specs/spring-petclinic/spring-petclinic-spec.yaml |
| 接口文件 | tests/baseline/_workflow/02-analysis-plan/apis.json |
| 生成计划 | tests/baseline/_workflow/02-analysis-plan/generation-plan.md |

## 六、特殊说明

1. **非 RESTful API**：该项目是传统 Spring MVC 服务端渲染应用，Controller 返回视图名称而非 JSON。仅 `/vets` 接口通过 `@ResponseBody` 返回 JSON。
2. **无认证**：系统无任何安全框架，所有接口完全开放，无需分析 token/header 认证。
3. **无独立 DTO/VO**：Controller 直接使用 JPA Entity 绑定表单数据，通过 `@InitBinder` 设置 `setDisallowedFields("id", "*.id")` 防止 mass assignment。
4. **表单验证**：使用 Jakarta Bean Validation (`@Valid`) + 自定义 `PetValidator` 双重验证。
5. **重定向 + Flash 属性**：成功操作后 redirect 并携带 flash message，失败则返回表单视图并展示错误。

## 七、下一步

使用 `yaml-to-pytest` skill 生成 pytest 测试脚本，或使用 `api-doc-to-testcases` 系列 skill 生成测试用例 YAML。

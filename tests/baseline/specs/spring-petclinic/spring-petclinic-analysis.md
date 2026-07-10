# Spring PetClinic 模块分析报告

**分析时间**: 2026-07-10
**分析方式**: CodeGraph 深度源码分析
**源码路径**: `D:\java\project\spring-petclinic`

---

## 技术栈

- 后端：Java Spring Boot 3.x + Spring MVC + Spring Data JPA
- 模板引擎：Thymeleaf（服务端渲染）
- 数据库：H2 (默认) / MySQL / PostgreSQL（通过 profile 切换）
- 缓存：JCache（vets 列表缓存）
- 校验：Jakarta Bean Validation + 自定义 Validator
- 国际化：Spring i18n + LocaleChangeInterceptor
- 构建工具：Maven

## 认证机制

- 类型：**无认证**
- 系统无 Spring Security、Shiro 或任何自定义安全 Filter
- 所有接口均可匿名访问
- 唯一的拦截器：`LocaleChangeInterceptor`，用于国际化语言切换（通过 `?lang=` 参数），无安全功能

## 拦截器/请求头

| 拦截器 | 路径前缀 | 必填 Header | 可选 Header | 说明 |
|--------|----------|-------------|-------------|------|
| LocaleChangeInterceptor | /* | - | - | 仅处理语言切换参数 `?lang=` |

## 实体模型层级

```
BaseEntity (id: Integer)
├── NamedEntity (name: String @NotBlank)
│   ├── Pet (birthDate: LocalDate, type: PetType, visits: Set<Visit>)
│   ├── PetType (无额外字段)
│   └── Specialty (无额外字段)
├── Person (firstName @NotBlank @Size(max=30), lastName @NotBlank @Size(max=30))
│   ├── Owner (address @NotBlank, city @NotBlank, telephone @NotBlank @Pattern(\d{10}), pets: List<Pet>)
│   └── Vet (specialties: Set<Specialty>)
└── Visit (date: LocalDate, description: String @NotBlank)
```

## API 端点

### system 模块 (2)

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | / | 欢迎首页 | 否 |
| GET | /oups | 异常演示（抛 RuntimeException） | 否 |

### vet 模块 (2)

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | /vets.html | 分页展示兽医列表（HTML） | 否 |
| GET | /vets | 获取兽医列表（JSON） | 否 |

### owner 模块 (13)

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | /owners/new | 显示创建 Owner 表单 | 否 |
| POST | /owners/new | 创建新 Owner | 否 |
| GET | /owners/find | 显示查找 Owner 表单 | 否 |
| GET | /owners | 按 lastName 查找 Owner（分页） | 否 |
| GET | /owners/{ownerId} | 查看 Owner 详情 | 否 |
| GET | /owners/{ownerId}/edit | 显示编辑 Owner 表单 | 否 |
| POST | /owners/{ownerId}/edit | 更新 Owner 信息 | 否 |
| GET | /owners/{ownerId}/pets/new | 显示添加 Pet 表单 | 否 |
| POST | /owners/{ownerId}/pets/new | 创建新 Pet | 否 |
| GET | /owners/{ownerId}/pets/{petId}/edit | 显示编辑 Pet 表单 | 否 |
| POST | /owners/{ownerId}/pets/{petId}/edit | 更新 Pet 信息 | 否 |
| GET | /owners/{ownerId}/pets/{petId}/visits/new | 显示添加 Visit 表单 | 否 |
| POST | /owners/{ownerId}/pets/{petId}/visits/new | 添加新 Visit | 否 |

## 前端页面

该项目为 Thymeleaf 服务端渲染，无独立前端 SPA。

| 模板路径 | 说明 |
|----------|------|
| welcome.html | 欢迎页 |
| owners/findOwners.html | Owner 查找表单 |
| owners/ownersList.html | Owner 列表页 |
| owners/ownerDetails.html | Owner 详情页 |
| owners/createOrUpdateOwnerForm.html | Owner 创建/编辑表单 |
| pets/createOrUpdatePetForm.html | Pet 创建/编辑表单 |
| pets/createOrUpdateVisitForm.html | Visit 创建表单 |
| vets/vetList.html | 兽医列表页 |
| error.html | 错误页 |

## Controller 详情

### OwnerController
- **路径前缀**: 无（各方法独立路径）
- **依赖**: OwnerRepository
- **特殊处理**: `@InitBinder` 禁止绑定 `id` 字段；`@ModelAttribute("owner")` 从路径变量 `ownerId` 加载 Owner

### PetController
- **路径前缀**: `/owners/{ownerId}`
- **依赖**: OwnerRepository, PetTypeRepository
- **特殊处理**: 双重 `@InitBinder`（owner + pet）；自定义 `PetValidator` 校验 name/type/birthDate；Controller 层额外校验名称唯一性和日期非未来

### VisitController
- **依赖**: OwnerRepository
- **特殊处理**: `@InitBinder` 禁止绑定 `id`；`@ModelAttribute("visit")` 自动加载 Pet 并初始化 Visit

### VetController
- **路径前缀**: 无
- **依赖**: VetRepository
- **特殊处理**: `/vets` 使用 `@ResponseBody` 返回 JSON；`/vets.html` 分页返回 HTML

### WelcomeController
- **路径**: `/`
- **返回**: "welcome" 视图

### CrashController
- **路径**: `/oups`
- **行为**: 直接抛出 RuntimeException，演示异常处理

## 校验规则汇总

| 校验器 | 字段 | 规则 |
|--------|------|------|
| Bean Validation | Person.firstName | @NotBlank, @Size(max=30) |
| Bean Validation | Person.lastName | @NotBlank, @Size(max=30) |
| Bean Validation | Owner.address | @NotBlank |
| Bean Validation | Owner.city | @NotBlank |
| Bean Validation | Owner.telephone | @NotBlank, @Pattern("\d{10}") |
| Bean Validation | NamedEntity.name | @NotBlank |
| Bean Validation | Visit.description | @NotBlank |
| PetValidator | Pet.name | required (非空) |
| PetValidator | Pet.type | required (新建时) |
| PetValidator | Pet.birthDate | required (非空) |
| Controller 层 | Pet.name | 同一 Owner 下唯一 |
| Controller 层 | Pet.birthDate | 不能在未来 |
| Controller 层 | Visit.date | 必须在将来 (after today) |
| Controller 层 | Owner.id (POST edit) | 必须与 URL 中 ownerId 一致 |

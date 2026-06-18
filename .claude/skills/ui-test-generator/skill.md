---
name: ui-test-generator
description: "根据前端页面和测试计划生成Playwright UI测试脚本。使用场景：用户要求生成UI测试、创建Playwright测试脚本、生成E2E测试。触发短语：生成UI测试、generate UI test、create playwright tests、生成E2E测试脚本"
---

# UI 测试生成器

根据前端页面配置和测试计划，使用Playwright生成可靠的UI自动化测试脚本。

## 输入文件

### 1. config.yaml（项目根目录）
包含以下配置信息：
- `source.backend[].path` - 后端工程代码路径
- `source.frontend[].path` - 前端工程代码路径
- `environments.<env>.frontend[].url` - 前端服务地址
- `environments.<env>.frontend[].accounts` - 测试账号信息

### 2. 测试生成计划文件
默认路径：`tests/baseline/_workflow/02-analysis-plan/generation-plan.md`

包含测试范围、优先级、测试场景等信息。

## 输出目录

```
tests/baseline/generated/ui-test/
```

## 输出文件结构

```
tests/baseline/generated/ui-test/
├── conftest.py              # Playwright配置和共享fixture
├── test_login.py           # 登录流程测试
├── test_dashboard.py       # 仪表盘测试
├── test_<模块名>.py         # 按功能模块划分的测试文件
├── pages/                  # Page Object模型
│   ├── base_page.py        # 基础页面类
│   ├── login_page.py       # 登录页面
│   └── ...
├── requirements.txt        # Python依赖
└── README.md              # 使用说明
```

## 技术栈

- **测试框架**：pytest
- **浏览器自动化**：Playwright
- **Page Object模式**：封装页面元素和操作

## 测试设计原则

### 1. Page Object模式
每个页面对应一个Page类，封装：
- 页面元素定位器（支持多选择器回退）
- 页面操作方法
- 页面URL和标识

```python
class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    # 多选择器回退机制
    USERNAME_INPUTS = ["#username", "input[name='username']", "input[placeholder*='用户名']"]
    PASSWORD_INPUTS = ["#password", "input[name='password']", "input[placeholder*='密码']"]
    LOGIN_BUTTONS = ["button[type='submit']", "button:has-text('登录')", ".el-button--primary"]

    def find_element(self, selectors):
        """查找第一个匹配的选择器"""
        for selector in selectors:
            if self.page.query_selector(selector):
                return selector
        return None

    def login(self, username, password):
        input_sel = self.find_element(self.USERNAME_INPUTS)
        pass_sel = self.find_element(self.PASSWORD_INPUTS)
        btn_sel = self.find_element(self.LOGIN_BUTTONS)

        if input_sel:
            self.page.fill(input_sel, username)
        if pass_sel:
            self.page.fill(pass_sel, password)
        if btn_sel:
            self.page.click(btn_sel)
```

### 2. 可靠的断言策略
- **成功操作**：验证页面跳转、内容显示、元素存在
- **错误操作**：验证错误提示、页面不变
- **等待策略**：使用智能等待而非固定sleep
- **强制断言**：元素不存在时使用 `pytest.fail()` 使测试失败

### 3. 测试独立性
- 每个测试用例独立运行
- 使用fixture管理登录状态
- 测试后自动清理状态

### 4. 分层fixture设计
```
conftest.py:
├── base_url              # 前端服务地址
├── browser             # Playwright浏览器实例 (session scope)
├── page                 # Playwright页面实例 (function scope - 默认)
├── logged_in_page      # 已登录的页面实例
├── visitor_logged_in_page  # 普通用户已登录
├── check_frontend_running  # 前端连接检查
└── assert_*              # 断言辅助函数
```

**重要**：`scope` 参数只支持 `function`、`class`、`module`、`session`，不支持 `page`。

### 5. 前端连接检查
每个测试开始前检查前端服务是否可达：

```python
@pytest.fixture
def check_frontend_running(page, base_url):
    """检查前端服务是否运行"""
    try:
        response = page.goto(f"{base_url}/", timeout=5000)
        if response and response.status >= 400:
            pytest.fail(f"Frontend not running at {base_url}")
    except Exception:
        pytest.fail(f"Cannot connect to frontend at {base_url}")
```

### 6. Vue SPA路由处理
Vue单页应用的路由使用hash模式，URL格式为 `http://localhost:5173/#/admin/list`

**重要**：导航时必须添加 `/#/` 前缀：
```python
# 错误 - 会导致路由重定向到home
page.goto(f"{base_url}/admin/list")  # 最终变成 /admin/list#/

# 正确 - hash模式路由
page.goto(f"{base_url}/#/admin/list")
```

**登录URL也需要正确格式**：
```python
login_urls = [
    f"{base_url}/#/login",
    f"{base_url}/#/login/",
    f"{base_url}/login",
    f"{base_url}/login/",
]
```

### 7. 灵活的选择器策略
- 元素选择器支持多个备选
- 按优先级尝试每个选择器
- 截图用于调试

## 生成步骤

### Step 1: 读取配置文件
从`config.yaml`提取：
- 前端工程路径 (`source.frontend`)
- 前端服务URL (`environments.<env>.frontend[].url`)
- 测试账号凭据 (`environments.<env>.frontend[].accounts`)

### Step 2: 解析测试计划
从`generation-plan.md`提取：
- 测试场景列表
- 测试优先级
- 测试数据

### Step 3: 分析前端页面（可选）
如果前端工程存在，分析页面结构：
- 页面路由
- 表单元素
- 按钮和链接

### Step 4: 生成测试文件

#### conftest.py
- Playwright配置
- 浏览器fixture
- 页面fixture
- 认证fixture
- 测试账号fixture

#### pages/目录
- base_page.py - 基础页面类
- login_page.py - 登录页面
- dashboard_page.py - 仪表盘页面
- 按需生成其他页面

#### test_*.py
按测试场景生成测试文件：
- test_login.py - 登录流程测试
- test_dashboard.py - 仪表盘测试
- test_<module>.py - 各功能模块测试

### Step 5: 确保输出目录存在
创建`tests/baseline/generated/ui-test/`及子目录（如不存在）。

### Step 6: 写入测试文件
将生成的文件写入输出目录。

## 模板使用

技能目录下的`template/`子目录包含Jinja2模板文件：

- `conftest.py.j2` - Playwright配置文件模板
- `base_page.py.j2` - 基础Page类模板
- `test_module.py.j2` - 测试模块模板

生成时读取模板，使用项目配置进行渲染。

## 依赖项

生成的`requirements.txt`包含：
```
pytest>=7.0.0
playwright>=1.40.0
pytest-playwright>=0.4.0
pytest-html>=3.0.0
```

## 常见测试场景

### 登录流程
- 成功登录 → 跳转仪表盘
- 错误密码 → 提示错误信息
- 空用户名 → 提示必填
- 无权限用户 → 禁止访问

### 仪表盘
- 页面加载 → 显示统计数据
- 侧边栏菜单 → 正确高亮
- 用户信息 → 正确显示

### CRUD操作
- 列表页加载 → 显示数据
- 新增功能 → 弹窗/跳转表单
- 编辑功能 → 预填表单数据
- 删除功能 → 确认/删除成功

## 质量检查清单

生成完成后，检查以下项目：

- [ ] Page Object封装页面元素，支持多选择器回退
- [ ] 使用智能等待而非固定sleep
- [ ] 测试用例可独立运行
- [ ] 元素不存在时使用 `pytest.fail()` 而非失败
- [ ] 错误场景有对应测试
- [ ] 测试数据使用配置中的账号
- [ ] 包含前端连接检查fixture
- [ ] 包含截图调试功能
- [ ] fixture scope 只使用 function/class/module/session（不使用 page）
# Python Client — 自动化测试框架

基于 pytest 的自动化测试框架，覆盖 **API 测试**（gRPC + HTTP）和 **UI 测试**（Selenium + Playwright），采用分层架构、数据驱动设计和 Allure 报告。

---

## 目录

- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [运行测试](#运行测试)
- [架构设计](#架构设计)
- [API 测试](#api-测试)
  - [gRPC 测试](#grpc-测试)
  - [HTTP 测试](#http-测试)
  - [如何新增 API 测试](#如何新增-api-测试)
- [UI 测试](#ui-测试)
  - [Selenium POM](#selenium-pom)
  - [Playwright POM](#playwright-pom)
  - [Selenium vs Playwright](#selenium-vs-playwright)
  - [如何新增 UI 测试](#如何新增-ui-测试)
- [测试数据管理](#测试数据管理)
- [配置说明](#配置说明)
- [Allure 报告](#allure-报告)
- [依赖清单](#依赖清单)

---

## 快速开始

### 前置条件

确保 Go 服务已启动（参考根目录 README.md）：

```bash
# gRPC Server → localhost:50051
# HTTP Server  → localhost:8080
```

### 安装

```bash
cd python_client
make setup
```

`make setup` 自动完成：创建 .venv → 升级 pip → 安装 requirements.txt → `playwright install chromium`

### 运行

```bash
make test              # 全部测试
make test-api          # 仅 API（gRPC + HTTP）
make test-selenium     # 仅 Selenium UI
make test-playwright   # 仅 Playwright UI
```

---

## 项目结构

```text
python_client/
├── conftest.py                        # Session 级 fixtures（API 专用）
├── pytest.ini                         # pytest 配置 + markers 注册
├── Makefile                           # setup / test / test-api / test-selenium / test-playwright
├── requirements.txt                   # Python 依赖
│
├── configs/
│   └── config.ini                     # 环境配置（服务地址 + SauceDemo URL）
│
├── functions/
│   └── func_hub.py                    # 引擎层 — gRPC 反射调用 + HTTP 请求
│
├── atom/                              # API Atom 层 — 单个 API 方法封装
│   ├── grpcAtom/
│   │   ├── base_grpc_atom.py          #   gRPC 基类（inspect 自动解析 service + method）
│   │   └── demo_grpc_atom.py
│   └── httpAtom/
│       ├── base_http_atom.py          #   HTTP 基类
│       └── demo_http_atom.py
│
├── service/                           # API Service 层 — 业务编排
│   ├── baseService.py
│   └── demo/
│       └── http_demo_service.py
│
├── pages/                             # UI Page Object 层（按工具隔离）
│   ├── selenium/
│   │   ├── base_page.py               #   WebDriverWait + expected_conditions
│   │   ├── login_page.py              #   SauceDemo 登录页
│   │   ├── products_page.py           #   商品列表页
│   │   ├── cart_page.py               #   购物车页
│   │   ├── checkout_page.py           #   结账信息页
│   │   └── overview_page.py           #   订单确认页 + 完成页
│   └── playwright/
│       ├── base_page.py               #   sync API + 内置 auto-waiting
│       ├── login_page.py
│       ├── products_page.py
│       ├── cart_page.py
│       ├── checkout_page.py
│       └── overview_page.py
│
├── TestCase/                          # 测试用例（按类型隔离）
│   ├── Test_Demo/                     #   API 测试
│   │   ├── test_simple_grpc.py
│   │   └── test_simple_http.py
│   ├── TC_Selenium/                   #   Selenium UI 测试
│   │   ├── conftest.py
│   │   └── test_saucedemo.py
│   └── TC_Playwright/                 #   Playwright UI 测试
│       ├── conftest.py
│       └── test_saucedemo.py
│
├── TestData/                          # 测试数据（YAML 数据驱动）
│   ├── Demo/                          #   API 数据
│   │   ├── simple_grpc.yaml
│   │   └── simple_http.yaml
│   ├── Selenium/                      #   Selenium 数据
│   │   ├── checkout.yaml
│   │   └── login_failure.yaml
│   └── Playwright/                    #   Playwright 数据
│       ├── checkout.yaml
│       └── login_failure.yaml
│
└── utils/
    └── data_reader.py                 # YAML 数据读取器
```

---

## 运行测试

```bash
# 全部
make test

# 按测试类型
make test-api                  # TestCase/Test_Demo
make test-selenium             # TestCase/TC_Selenium
make test-playwright           # TestCase/TC_Playwright

# pytest 原生命令
.venv/bin/python -m pytest TestCase/Test_Demo/test_simple_grpc.py -v
.venv/bin/python -m pytest TestCase/TC_Selenium -m ui_selenium -v
.venv/bin/python -m pytest TestCase/TC_Playwright -m ui_playwright -v

# 指定环境
.venv/bin/python -m pytest --env stage
```

---

## 架构设计

### 整体分层

```
┌──────────────────────────────────────────────────────────┐
│                      TestCase                            │
│   (pytest data-driven, parametrize + markers 隔离)        │
├──────────────┬──────────────────┬────────────────────────┤
│  Test_Demo   │  TC_Selenium     │  TC_Playwright         │
│  (API)       │  (UI - Selenium) │  (UI - Playwright)     │
├──────────────┴──────────────────┴────────────────────────┤
│                                                          │
│  API 路径                     UI 路径                     │
│  TestCase                     TestCase                   │
│    ↓                            ↓                        │
│  Service (编排)               Page Object (pages/)        │
│    ↓                            ↓                        │
│  Atom (单 API 封装)           WebDriver / Playwright      │
│    ↓                                                     │
│  FuncHub (引擎)                                           │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**设计原则：**
- **API 与 UI 完全隔离** — 独立目录、独立 conftest、独立 pytest markers，互不污染
- **工具级隔离** — Selenium 和 Playwright 各自独立包，各自的 conftest 管理驱动生命周期
- **数据与代码分离** — 所有测试数据用 YAML 管理
- **可扩展** — 新增测试类型只需 `pages/{tool}/` + `TestCase/TC_{Tool}/`

---

## API 测试

### gRPC 测试

**核心特性：gRPC 反射** — Python 侧无需 `protoc` 编译 proto 文件，通过 `yagrc` 运行时动态解析服务定义。session 级缓存，整个测试过程只做一次反射查询。

反射流程：

```text
┌──────────┐  1. ServerReflectionInfo    ┌──────────┐
│  Python  │ ──────────────────────────▶ │  Go      │
│  Client  │                             │  Server  │
│          │  2. 动态获取 proto 定义       │          │
│          │ ◀────────────────────────── │          │
│          │  3. 发起实际 RPC 调用         │          │
│          │ ──────────────────────────▶ │          │
└──────────┘                             └──────────┘
```

Go 服务需要开启反射：

```go
import "google.golang.org/grpc/reflection"
reflection.Register(server)
```

#### 自动方法名匹配

Atom 层通过 `inspect` 获取调用栈，自动将 Python 方法名映射为 gRPC 方法名：

```python
# atom/grpcAtom/demo_grpc_atom.py
class DemoServiceGrpcAtom(BaseGrpcAtom):

    @classmethod
    def SayHello(cls, toolkits, json_req):
        return cls.grpc(toolkits, json_req)
        # BaseGrpcAtom.grpc() 通过 inspect 自动解析：
        #   service = "DemoService"  (类名去掉 GrpcAtom 后缀)
        #   method  = "SayHello"     (调用方方法名)
```

#### 配置文件

```ini
# configs/config.ini
[GRPC]
DemoService = localhost:50051
```

#### 测试用例

```python
# TestCase/Test_Demo/test_simple_grpc.py
class TestSimpleGrpc:

    @pytest.mark.parametrize("testdata", yamlDataProvider("TestData/Demo/simple_grpc.yaml"))
    def test_grpc_demo(self, toolkits, testdata):
        res = DemoServiceGrpcAtom.SayHello(toolkits, testdata["request_dict"])
        assert res.get("message") == testdata["expected"]
```

### HTTP 测试

```python
# TestCase/Test_Demo/test_simple_http.py
class TestSimpleHttpAtom:

    @pytest.mark.parametrize("testdata", yamlDataProvider("TestData/Demo/simple_http.yaml"))
    def test_http_request(self, toolkits, testdata):
        demo_service = HttpDemoService(toolkits, testdata)
        res = demo_service.call_demo_api_post()
        assert res.get('error_msg', 0) == 0
```

### 如何新增 API 测试

#### 新增 gRPC 测试

1. **配置服务地址** — `configs/config.ini` 添加：

```ini
[GRPC]
Calculator = localhost:50052
```

2. **创建 Atom 类** — `atom/grpcAtom/calculator.py`：

```python
from atom.grpcAtom.base_grpc_atom import BaseGrpcAtom

class CalculatorGrpcAtom(BaseGrpcAtom):
    # 类名去掉 "GrpcAtom" → service = "Calculator"

    @classmethod
    def Add(cls, toolkits, json_req):
        return cls.grpc(toolkits, json_req)
```

3. **准备 YAML 数据** — `TestData/Demo/calculator.yaml`

4. **写测试用例** — `TestCase/Test_Demo/test_calculator.py`

#### 新增 HTTP 测试

1. `configs/config.ini` 添加域名
2. `atom/httpAtom/` 新建 Atom（继承或直接使用 `BaseHttpAtom`）
3. 可选：`service/` 新建 Service 编排业务逻辑
4. `TestData/Demo/` + `TestCase/Test_Demo/` 写数据 + 用例

---

## UI 测试

两个 UI 框架均采用 **Page Object Model（POM）**，针对 SauceDemo（`https://www.saucedemo.com`）电商网站，覆盖相同测试场景。

### 测试场景

| 用例 | YAML | 描述 |
|------|------|------|
| `test_complete_checkout` | `checkout.yaml` | 登录 → 浏览商品 → 加购 2 件 → 购物车验证 → 结账 → 填写信息 → 确认订单 |
| `test_login_failure` | `login_failure.yaml` | locked_out_user 登录失败，验证错误消息 |

### Selenium POM

**Fixture（session 级 browser）：**

```python
# TestCase/TC_Selenium/conftest.py
@pytest.fixture(scope="session")
def browser(env):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.base_url = env["SAUCEDEMO"]["base_url"]
    yield driver
    driver.quit()
```

**BasePage（显式等待）：**

```python
# pages/selenium/base_page.py
class BasePage:
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def find(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def click(self, by, value):
        self.wait.until(EC.element_to_be_clickable((by, value))).click()

    def fill(self, by, value, text):
        el = self.find(by, value)
        el.clear()
        el.send_keys(text)
```

**Page Object 示例：**

```python
# pages/selenium/login_page.py
class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON   = (By.ID, "login-button")

    def login(self, username, password):
        self.fill(*self.USERNAME_INPUT, username)
        self.fill(*self.PASSWORD_INPUT, password)
        self.click(*self.LOGIN_BUTTON)
        return ProductsPage(self.driver)    # 页面跳转 → 返回新 Page Object
```

**测试用例：**

```python
# TestCase/TC_Selenium/test_saucedemo.py
class TestSauceDemoSelenium:

    @pytest.mark.ui_selenium
    @pytest.mark.parametrize("testdata", yamlDataProvider("TestData/Selenium/checkout.yaml"))
    def test_complete_checkout(self, browser, testdata):
        login_page = LoginPage(browser).open()
        products_page = login_page.login(td["username"], td["password"])
        # ... 完整 E2E 流程
```

### Playwright POM

**Fixture 链（session browser + function page）：**

```python
# TestCase/TC_Playwright/conftest.py
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw

@pytest.fixture(scope="session")
def browser(playwright_instance, env):
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")    # ← function 级，每个测试独立 Context
def page(browser, env):
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.base_url = env["SAUCEDEMO"]["base_url"]
    yield page
    context.close()
```

**BasePage（内置 auto-waiting）：**

```python
# pages/playwright/base_page.py
class BasePage:
    DEFAULT_TIMEOUT = 10_000  # ms

    def __init__(self, page: Page):
        self.page = page

    def click(self, selector: str):
        self.page.locator(selector).click(timeout=self.DEFAULT_TIMEOUT)

    def fill(self, selector: str, text: str):
        self.page.locator(selector).fill(text, timeout=self.DEFAULT_TIMEOUT)
```

**Page Object 示例：**

```python
# pages/playwright/login_page.py
class LoginPage(BasePage):
    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BTN = "#login-button"

    def login(self, username, password):
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
        return ProductsPage(self.page)
```

### Selenium vs Playwright

| 维度 | Selenium | Playwright |
|------|----------|------------|
| **等待机制** | 显式 `WebDriverWait` + `EC` | 内置 auto-waiting，无需手动等待 |
| **元素定位** | `(By.ID, "user-name")` 元组 | `"#user-name"` CSS 选择器 |
| **驱动管理** | 需要 `webdriver-manager` 匹配 ChromeDriver | 内置，`playwright install chromium` |
| **测试隔离** | session 级共享 driver，需手动清理状态 | function 级 BrowserContext，自动隔离 |
| **API 风格** | 传统 WebDriver 协议 | 现代 CDP 协议 |
| **适用场景** | 老旧项目兼容、多浏览器矩阵 | 新项目首选、调试体验更好 |

### 如何新增 UI 测试

按 `pages/{tool}/` + `TestCase/TC_{Tool}/` 模式扩展：

```text
python_client/
├── pages/
│   └── cypress/                  # 例如新增 Cypress
│       ├── base_page.py
│       ├── login_page.py
│       └── ...
└── TestCase/
    └── TC_Cypress/
        ├── conftest.py            # Cypress 专用 fixtures
        └── test_xxx.py
```

步骤：
1. `pages/{tool}/base_page.py` — 封装该工具的通用操作
2. `pages/{tool}/*.py` — 逐个页面写 Page Object
3. `TestCase/TC_{Tool}/conftest.py` — 管理驱动/Fixture
4. `TestCase/TC_{Tool}/test_*.py` — 写用例，注册新的 `@pytest.mark`
5. `pytest.ini` 添加对应 marker

---

## 测试数据管理

测试数据存储在 `TestData/` 下，YAML 格式，通过 `utils/data_reader.py` 的 `yamlDataProvider()` 读取：

```yaml
# 格式
- testCase:
    testId: tc-1                        # 用例 ID
    testName: "场景名称"                 # pytest parametrize 中作为 id
    testOwner: owner1
    testDescription: "描述"
    isAutomated: Y
  testData:
    request_dict:                       # API 用
      name: "yuchen"
    expected: "Hello, yuchen!"

# UI 用
  testData:
    username: standard_user
    password: secret_sauce
    checkout_info:
      first_name: "Test"
      last_name: "User"
      postal_code: "12345"
    expected_products:
      - "Sauce Labs Backpack"
      - "Sauce Labs Bike Light"
    expected_complete_header: "Thank you for your order!"
```

**最佳实践：** 一个 YAML 文件对应一个 test 方法，文件命名清晰（如 `checkout.yaml`、`login_failure.yaml`），避免一个文件混合多个场景。

---

## 配置说明

`configs/config.ini` 按 section 管理环境配置：

```ini
[HTTP]
http_domain = http://localhost:8080

[GRPC]
DemoService = localhost:50051

[SAUCEDEMO]
base_url = https://www.saucedemo.com
```

**多环境示例：**

```ini
[HTTP]
http_domain = http://localhost:8080

[HTTP-stage]
http_domain = https://stage.api.example.com

[GRPC]
DemoService = localhost:50051

[GRPC-stage]
DemoService = stage-server:50051
```

通过 `--env` 切换：

```bash
pytest --env stage
```

---

## Allure 报告

默认配置已开启 Allure，结果输出到 `allure-results/`：

```bash
# 安装 Allure CLI
brew install allure    # macOS

# 运行测试 → 生成报告
pytest --alluredir=allure-results

# 查看报告
allure serve allure-results

# 生成静态 HTML
allure generate allure-results -o allure-report
```

---

## 依赖清单

| 库 | 用途 |
|----|------|
| `grpcio` | gRPC 核心库 |
| `grpcio-reflection` | gRPC 服务端反射支持 |
| `yagrc` | 反射动态加载 proto，无需预编译 |
| `protobuf` | Protocol Buffers 序列化 |
| `requests` | HTTP 请求 |
| `pytest` | 测试框架 |
| `pyyaml` | YAML 解析 |
| `loguru` | 日志 |
| `allure-pytest` | Allure 报告集成 |
| `selenium` | Selenium WebDriver |
| `webdriver-manager` | ChromeDriver 自动管理 |
| `playwright` | Playwright 浏览器自动化 |

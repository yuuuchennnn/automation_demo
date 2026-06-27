# Automation Demo

全栈自动化测试 Demo 项目，覆盖 **API 测试**（gRPC + HTTP）和 **UI 测试**（Selenium + Playwright），采用工业级分层架构。

---

## 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| 被测服务 | **Go** | gRPC Server + HTTP Demo Server |
| 接口契约 | **Protobuf** | 共享 proto 接口定义 |
| API 测试 | **Python + pytest** | gRPC 反射调用 + HTTP API 测试 |
| UI 测试 | **Selenium / Playwright** | Page Object Model 前端自动化 |
| 测试报告 | **Allure** | 可视化测试报告 |
| CI | **GitHub Actions** | 构建 → 测试 → 报告 一条流水线 |

---

## 目录结构

```text
automation_demo/
├── proto/                                # Proto 接口定义
│   └── helloworld/v1/helloworld.proto
│
├── go_services/                          # Go 后端服务
│   ├── grpc_demo/                        #   gRPC Server（反射 + DemoService）
│   │   ├── cmd/server/main.go
│   │   ├── gen/                          #   生成的 proto Go 代码
│   │   ├── Makefile
│   │   └── go.mod
│   └── http_demo/                        #   HTTP Demo Server
│       ├── cmd/server/main.go
│       ├── Makefile
│       └── go.mod
│
├── python_client/                        # Python 自动化测试框架
│   ├── conftest.py                       #   pytest session fixtures（API 专用）
│   ├── pytest.ini                        #   pytest 配置 + markers
│   ├── Makefile                          #   一键命令（setup / test / test-api / test-selenium / test-playwright）
│   ├── requirements.txt                  #   依赖清单
│   ├── configs/config.ini                #   环境配置（服务地址 + SauceDemo URL）
│   │
│   ├── functions/func_hub.py             #   引擎层 — gRPC 反射调用 + HTTP 请求
│   │
│   ├── atom/                             #   API Atom 层 — 单个 API 方法封装
│   │   ├── grpcAtom/
│   │   │   ├── base_grpc_atom.py         #     gRPC 基类（自动解析 service + method）
│   │   │   └── demo_grpc_atom.py
│   │   └── httpAtom/
│   │       ├── base_http_atom.py         #     HTTP 基类
│   │       └── demo_http_atom.py
│   │
│   ├── service/                          #   API Service 层 — 业务编排
│   │   ├── baseService.py
│   │   └── demo/http_demo_service.py
│   │
│   ├── pages/                            #   UI Page Object 层（工具隔离）
│   │   ├── selenium/                     #     Selenium POM（6 个 Page + BasePage）
│   │   │   ├── base_page.py              #       WebDriverWait + expected_conditions
│   │   │   ├── login_page.py
│   │   │   ├── products_page.py
│   │   │   ├── cart_page.py
│   │   │   ├── checkout_page.py
│   │   │   └── overview_page.py
│   │   └── playwright/                   #     Playwright POM（6 个 Page + BasePage）
│   │       ├── base_page.py              #       sync API + 内置 auto-waiting
│   │       ├── login_page.py
│   │       ├── products_page.py
│   │       ├── cart_page.py
│   │       ├── checkout_page.py
│   │       └── overview_page.py
│   │
│   ├── TestCase/                         #   测试用例（按测试类型隔离）
│   │   ├── Test_Demo/                    #     API 测试
│   │   │   ├── test_simple_grpc.py
│   │   │   └── test_simple_http.py
│   │   ├── TC_Selenium/                  #     Selenium UI 测试
│   │   │   ├── conftest.py               #       browser fixture
│   │   │   └── test_saucedemo.py         #       @pytest.mark.ui_selenium
│   │   └── TC_Playwright/                #     Playwright UI 测试
│   │       ├── conftest.py               #       browser + page fixtures
│   │       └── test_saucedemo.py         #       @pytest.mark.ui_playwright
│   │
│   ├── TestData/                         #   测试数据（YAML 数据驱动）
│   │   ├── Demo/                         #     API 数据
│   │   │   ├── simple_grpc.yaml
│   │   │   └── simple_http.yaml
│   │   ├── Selenium/                     #     Selenium 数据
│   │   │   ├── checkout.yaml
│   │   │   └── login_failure.yaml
│   │   └── Playwright/                   #     Playwright 数据
│   │       ├── checkout.yaml
│   │       └── login_failure.yaml
│   │
│   └── utils/data_reader.py             #   YAML 数据读取工具
│
├── .github/workflows/demo-ci.yml         #   CI 流水线
└── README.md
```

---

## 快速开始

### 1. 启动 Go 服务

```bash
# gRPC Server（默认 :50051）
cd go_services/grpc_demo
make
make start-server-bg

# HTTP Server（默认 :8080）
cd go_services/http_demo
make
make start-server-bg
```

### 2. 安装 Python 依赖

```bash
cd python_client
make setup
# 这会自动：创建 venv → 安装 pip 依赖 → 下载 Chromium（Playwright 用）
```

### 3. 运行测试

```bash
cd python_client

make test              # 全部
make test-api          # 仅 API（gRPC + HTTP）
make test-selenium     # 仅 Selenium UI
make test-playwright   # 仅 Playwright UI
```

---

## Proto 接口

```protobuf
// proto/helloworld/v1/helloworld.proto
service DemoService {
  rpc SayHello(SayHelloRequest) returns (SayHelloResponse);
}
```

---

## 测试架构总览

```
                    ┌─────────────────────────────┐
                    │      TestCase               │  pytest data-driven
                    ├──────────────┬──────────────┤
                    │  TC_Selenium │TC_Playwright │  ← UI 测试
                    │  Test_Demo                  │  ← API 测试
                    └─────┬──────┬────────────────┘
                          │      │
            ┌─────────────┘      └─────────────┐
            ▼                                   ▼
   ┌─────────────────┐              ┌───────────────────┐
   │  pages/selenium │              │  pages/playwright │  Page Object 层
   │  BasePage + POM │              │  BasePage + POM   │
   └────────┬────────┘              └──────────┬────────┘
            │                                  │
   ┌────────┴──────────┐              ┌────────┴─────────┐
   │ Selenium WebDriver│              │  Playwright Page │  驱动层
   └───────────────────┘              └──────────────────┘

   ┌──────────────────────────────────────────────────┐
   │          API 测试（四层架构）                       │
   │  TestCase → Service → Atom → FuncHub             │
   │  FuncHub: gRPC 反射调用 + HTTP requests           │
   └──────────────────────────────────────────────────┘
```

### API 测试（四层架构）

| 层 | 文件 | 职责 |
|----|------|------|
| **TestCase** | `test_simple_grpc.py` | pytest 用例，读取 YAML 数据 |
| **Service** | `http_demo_service.py` | 业务编排，组合多个 Atom |
| **Atom** | `demo_grpc_atom.py` | 单个 API 方法封装 |
| **FuncHub** | `func_hub.py` | gRPC 反射调用 + HTTP 请求引擎 |

**核心特性：gRPC 反射** — Python 侧无需 `protoc` 编译，通过 `yagrc` 动态解析服务定义，会话级缓存。

### UI 测试（Page Object Model）

| 层 | 文件 | 职责 |
|----|------|------|
| **TestCase** | `test_saucedemo.py` | pytest 用例，`@pytest.mark.ui_*` 标记 |
| **Page Object** | `pages/{tool}/*.py` | 封装页面元素定位 + 操作 |
| **Fixture** | `conftest.py` | 管理浏览器生命周期 |

**Selenium vs Playwright 对比：**

| | Selenium | Playwright |
|------|----------|------------|
| 等待机制 | 显式 `WebDriverWait` | 内置 auto-waiting |
| 元素定位 | `(By.ID, "user-name")` 元组 | `"#user-name"` CSS |
| 驱动管理 | `webdriver-manager` | 内置 `install chromium` |
| 测试隔离 | session 级共享 driver | function 级 BrowserContext |
| 适用场景 | 老旧项目兼容 / 多浏览器 | 现代项目首选 |

---

## CI（GitHub Actions）

流水线步骤：

1. **Checkout** → **Build Go Services** → **Setup Python**
2. **Start Go Services** → **Run pytest**（API）
3. 失败时打印服务日志
4. **Generate Allure Report** → 上传 Artifact（保留 14 天）

> UI 测试（Selenium/Playwright）因需要浏览器环境，可在后续扩展 CI 步骤中单独 Job 运行。

---

## 扩展指南

### 新增 API 测试（gRPC）

1. `configs/config.ini` 添加服务地址
2. `atom/grpcAtom/` 新建 Atom 类
3. `TestData/Demo/` 新建 YAML 数据
4. `TestCase/Test_Demo/` 写 test 方法

### 新增 UI 测试框架

按 `pages/{tool}/` + `TestCase/TC_{Tool}/` 模式即可：

```text
python_client/
├── pages/
│   └── cypress/            # 例如新增 Cypress
│       ├── base_page.py
│       └── ...
└── TestCase/
    └── TC_Cypress/
        ├── conftest.py
        └── test_xxx.py
```

每个工具独立的 conftest 管理自己的驱动，互不污染。

# Selenium POM Test Demo — Design Spec

**Date:** 2026-06-27
**Status:** Approved

---

## Goal

为 automation_demo 项目新增 Selenium Page Object Model (POM) UI 自动化测试 Demo，覆盖 SauceDemo 完整电商流程。采用与现有 API 测试"同仓分离"的架构，预留 Playwright 扩展点。

---

## Architecture

```
TestCase (TC_Selenium/)     ← pytest data-driven, @pytest.mark.ui_selenium
    ↓
Page Object (pages/selenium/) ← 封装每页元素定位 + 操作
    ↓
Selenium WebDriver           ← conftest.py 提供 browser fixture
```

与 API 测试四层架构概念对等但完全独立，互不污染。

---

## Directory Structure

```
python_client/
├── pages/
│   └── selenium/
│       ├── __init__.py
│       ├── conftest.py              # browser fixture (session-scoped)
│       ├── base_page.py             # BasePage: find/click/fill/get_text/wait
│       ├── login_page.py            # SauceDemo LoginPage
│       ├── products_page.py         # ProductsPage
│       ├── cart_page.py             # CartPage
│       ├── checkout_page.py         # CheckoutPage (checkout-step-one)
│       └── overview_page.py         # OverviewPage (checkout-step-two)
│
├── TestCase/
│   └── TC_Selenium/
│       ├── __init__.py
│       └── test_saucedemo.py        # 完整结账流程 + 登录失败用例
│
├── TestData/
│   └── Selenium/
│       └── saucedemo_checkout.yaml  # 数据驱动测试数据
│
├── configs/config.ini               # + [SAUCEDEMO]
├── requirements.txt                 # + selenium, webdriver-manager
├── pytest.ini                       # + markers: ui_selenium
└── Makefile                         # + test-selenium target
```

### Future Playwright Extension

```
pages/
├── selenium/          ← 本期
└── playwright/        ← 后期新增，独立包
    ├── conftest.py
    ├── base_page.py
    └── ...
TestCase/
├── TC_Selenium/       ← 本期
└── TC_Playwright/     ← 后期新增
TestData/
├── Selenium/          ← 本期
└── Playwright/        ← 后期新增（可复用 selenium 的数据）
```

---

## Page Objects

### BasePage

| Method | Description |
|--------|-------------|
| `find(by, value)` | 等待元素可见后返回 |
| `click(by, value)` | 等待可点击后点击 |
| `fill(by, value, text)` | 清空后输入文本 |
| `get_text(by, value)` | 获取元素文本 |

使用 `WebDriverWait` + `expected_conditions`，默认超时 10s。

### LoginPage (`https://www.saucedemo.com`)

| Element | Locator | Operation |
|---------|---------|-----------|
| username input | `#user-name` | fill |
| password input | `#password` | fill |
| login button | `#login-button` | click |
| error message | `[data-test="error"]` | get_text |

Methods: `login(username, password)`, `get_error_message()`

### ProductsPage (`/inventory.html`)

| Element | Locator | Operation |
|---------|---------|-----------|
| page title | `.title` | get_text |
| product items | `.inventory_item` | list |
| add to cart btn | `button[id^="add-to-cart"]` (per item) | click |
| shopping cart badge | `.shopping_cart_badge` | get_text |
| shopping cart link | `.shopping_cart_link` | click |
| sort dropdown | `.product_sort_container` | select |

Methods: `add_item_to_cart(name)`, `get_cart_count()`, `go_to_cart()`, `get_title()`

### CartPage (`/cart.html`)

| Element | Locator | Operation |
|---------|---------|-----------|
| cart items | `.cart_item` | list |
| remove button | `button[id^="remove"]` | click |
| checkout button | `#checkout` | click |

Methods: `get_items()`, `remove_item(name)`, `checkout()`

### CheckoutPage (`/checkout-step-one.html`)

| Element | Locator | Operation |
|---------|---------|-----------|
| first name | `#first-name` | fill |
| last name | `#last-name` | fill |
| postal code | `#postal-code` | fill |
| continue btn | `#continue` | click |
| error message | `[data-test="error"]` | get_text |

Methods: `fill_checkout_info(first, last, zip)`, `continue_checkout()`

### OverviewPage (`/checkout-step-two.html`)

| Element | Locator | Operation |
|---------|---------|-----------|
| overview items | `.cart_item` | list |
| total label | `.summary_total_label` | get_text |
| finish btn | `#finish` | click |

Methods: `get_items()`, `get_total()`, `finish()`

---

## Test Cases

### 1. 完整结账流程（Happy Path）

`test_complete_checkout`，数据驱动，`@pytest.mark.ui_selenium`

```
1. 打开 SauceDemo → 验证在登录页
2. 用 standard_user 登录
3. 验证进入 ProductsPage（标题 = "Products"）
4. 添加 Sauce Labs Backpack + Sauce Labs Bike Light
5. 购物车 badge 显示 "2"
6. 进入购物车 → 验证 2 件商品
7. 点击 Checkout
8. 填写 shipping 信息 → Continue
9. 验证 Overview 总价存在 + 有 2 件商品
10. 点击 Finish
11. 验证 Complete! 标题和感谢消息
```

### 2. 登录失败用例

`test_login_failure`，验证错误消息显示。

---

## Configuration

```ini
# configs/config.ini
[SAUCEDEMO]
base_url = https://www.saucedemo.com
```

---

## Fixture Design

```python
# pages/selenium/conftest.py
@pytest.fixture(scope="session")
def browser(env):
    """Session-level browser instance"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")        # CI 友好
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
```

- `scope="session"` — 整个测试 session 共享一个浏览器，减少启动开销
- `--headless` — CI 中不需要显示器
- `webdriver-manager` — 自动管理 chromedriver 版本

---

## pytest.ini Changes

```ini
markers =
    ui_selenium: Selenium UI automation tests
```

---

## Makefile Commands

```makefile
test-selenium:
	.venv/bin/python -m pytest TestCase/TC_Selenium -m ui_selenium -v

test-api:
	.venv/bin/python -m pytest TestCase/Test_Demo -v

test-all: test-api test-selenium
```

---

## Error Handling Strategy

- 元素未找到 → WebDriverWait timeout → pytest 自动标记失败
- 网络错误 → Selenium 内建 Exception → conftest 中可通过 pytest_runtest_makereport 添加截图
- Allure 兼容 → 保留现有 allure-pytest，UI 用例失败时自动截图

---

## Self-Review Checklist

- [x] 无 TBD / TODO 占位符
- [x] Page Object 定位器与 SauceDemo 实际 DOM 一致
- [x] 测试数据与代码分离（YAML）
- [x] UI 与 API 完全隔离（独立目录、独立 conftest、独立 marker）
- [x] Playwright 预留扩展路径（pages/playwright/）
- [x] CI 友好（headless 模式 + webdriver-manager）

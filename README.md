## 🚀 自动化测试执行与 Allure 可视化报告交付

本框架采用 Pytest 作为核心测试驱动引擎，联动 Allure 实现了生产级的质量看板交付。为了防范垃圾文件污染 Git，全量测试中间产物（`allure-results/`）已在 `.gitignore` 中执行了硬隔离拦截。

### 1. 环境依赖就绪 (Prerequisites)
在运行测试前，请确保你已激活本地虚拟环境，并完成了第三方核心库与 Playwright 浏览器的静默安装：
```bash
pip install -r requirements.txt
playwright install
```

### 2. 一键触发全量测试 (Execute Automated Tests)
执行以下标准命令，触发用例自动化跑测。框架在执行过程中会自动捕获接口依赖数据，且在 UI 测试翻车时通过 Pytest 钩子自动抓拍缺陷现场，并统一将结构化数据沉淀至 `allure-results` 文件夹中：
```bash
pytest --alluredir=allure-results
```

### 3. 本地一键拉起 HTML 质量看板 (Generate & Serve Allure Report)
由于跑测生成的原始数据均为非直视的 JSON 级联分片，请确保你的本地系统（Windows/Mac）已配置好 Allure 命令行环境，随后在项目根目录下执行以下命令。系统将自动在本地沙盒中编译并拉起一个惊艳的、可交互的可视化 HTML 报告网页：
```bash
allure serve allure-results
```
*(💡 提示：Allure Board 包含用例成功率饼图、严密的 @allure.step 业务执行序列、响应体 JSON 动态审计以及失败时的全量屏幕快照。)*

### 📊 自动化测试交付质量看板 (Allure Visual Dashboard)

> 💡 **提示**：为防范环境文件污染 Git，全量测试中间产物（`allure-results/`）已在 `.gitignore` 中执行了硬隔离。以下为本框架在持续集成（CI）流水线中编译产出的标准 Allure 可视化看板：

![Allure Report Preview](https://ax1x.com)

#### 🛡️ 框架核心高光技术栈实现说明：
1. **服务虚拟化解耦 (`conftest.py`)**：在 `1-API-Automation` 模块中，自研内嵌式 `responses` 轻量级 Mock 网关夹具，在内存中完全接管并模拟第三方网关，彻底斩断外部网络 WAF 阻断对自动化流水线的污染，实现毫秒级快速闭环跑测。
2. **多层级业务故事线装饰器**：用例层深度融入 `@allure.epic`、`@allure.feature`、`@allure.story` 及 `@allure.severity` 等大厂级原语，实现非结构化测试成果向可读性极高、带步骤展开树（Steps）的工业级看板转化。


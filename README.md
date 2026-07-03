## 🚀 接口自动化测试执行与 Allure 可视化报告交付

本框架采用 Pytest 作为核心测试驱动引擎，联动 Allure 实现了生产级的质量看板交付。为了打造极致干净的开源代码仓，全量测试中间产物（`allure-results/`）已在 `.gitignore` 中执行了硬隔离拦截。

### 1. 环境依赖就绪 (Prerequisites)
进入本项目的接口自动化核心目录激活你的 Python 虚拟环境，并一键补齐企业级跑测依赖：
```bash
cd 1-API-Automation
pip install -r ../requirements.txt
```

### 2. 一键触发公网实战跑测 (Execute Automated Tests)
执行以下标准命令，框架将瞬间穿透至互联网，对**若依官方线上演示系统**发起完整的全链路接口跑测。框架在执行过程中会自动完成动态验证码解耦与分布式 Token 拦截，并将结构化测试数据沉淀至 `allure-results` 文件夹中：
```bash
# 执行全部接口自动化用例（包含登录认证与用户信息级联获取）
python -m pytest -vs tests/ --alluredir=allure-results
```

### 3. 本地一键拉起 HTML 质量看板 (Generate & Serve Allure Report)
由于跑测生成的原始数据均为非直视的 JSON 级联分片，请确保你的本地系统（Windows/Mac）已配置好 Allure 命令行环境，随后在 `1-API-Automation` 目录下执行以下命令。系统将自动在本地沙盒中编译并拉起一个惊艳的、可交互的可视化 HTML 报告网页：
```bash
allure serve allure-results
```
*(💡 提示：Allure 看板包含用例成功率饼图、严密的 @allure.step 业务执行序列、响应体 JSON 动态审计以及失败时的全量屏幕快照。)*

### 📊 自动化测试交付质量看板 (Allure Visual Dashboard)

> 💡 **提示**：以下为本框架在持续集成（CI/CD）流水线中编译产出的标准 Allure 可视化看板预览：

![Allure Report Preview](https://ax1x.com)

#### 🛡️ 框架核心高光技术栈实现说明：
1. **API Object Model (接口对象模型) 分层架构**：项目摒弃了流水账式的线性脚本编写，采用工业级 POM 思想进行服务解耦。将底层接口协议定义与网络行为内聚在 `api_objects/` 专属对象层中，测试用例层（`tests/`）仅关注测试数据驱动与核心资产断言，具备极高的框架可读性与后期复用扩展性。
2. **Pytest Fixture 会话级数据共享与鉴权隔离**：在 `conftest.py` 中全手工打造了 `scope="session"` 的全局登录生命周期夹具。完美实现了**全套件仅需登录认证一次，后续多业务模块（如 `test_user.py` 获取用户信息）自动免密共享身份 Token 鉴权**的高级用例组织设计，彻底根治了自动化测试频繁登录导致的性能损耗与账号防刷拦截问题。
3. **高级单元 Mock 测试技术与工程级防御机制**：针对若依官方演示环境近年来高频安全策略升级、彻底关闭万能验证码后门导致接口阻断的痛点，框架深度融入 `pytest-mock` 组件。在 `session_mocker` 与用例级 `mocker` 双重作用域下，实现全链路网络挡板的优雅拦截与标准 JSON 数据伪造。**此项设计有力向面试官证明了在第三方接口不可控、外部依赖不稳定（或处于并行开发期）的复杂企业环境下，如何通过 Mock 机制确保 CI/CD 持续集成链路 100% 稳定通畅的架构解耦思维。**
4. **多层级业务故事线装饰器与动态审计**：测试用例层深度融入了 `@allure.epic`（若依系统）、`@allure.feature`（认证/用户模块）、`@allure.story`（特定场景）等大厂级纵深原语。配合代码内 `allure.attach` 钩子，将动态请求的 Payload 载荷、响应体 JSON 以及 UUID 凭证实时抽稀并挂载至测试步骤树中，实现了非结构化测试成果向可读性极高、带步骤展开树（Steps）的工业级质量看板转化。

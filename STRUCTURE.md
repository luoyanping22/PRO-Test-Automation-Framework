PRO-TEST-AUTOMATION-FRAMEWORK/
├── .github/                           # GitHub 自动化运维中心
│   └── workflows/
│       └── ci_pipeline.yml            # GitHub Actions 综合质量红线流水线
├── .gitee/                            # Gitee 自动化运维中心
│   └── workflows/
│       └── ci_pipeline.yml            # Gitee Go 综合质量红线流水线
├── 1-API-Automation/               # 接口自动化测试板块
│   ├── api_objects/                # 接口对象层 (API Object Model)
│   │   └── auth_api.py             # 封装登录鉴权、Token 提取等底层接口请求
│   ├── tests/                      # 测试用例层
│   │   ├── test_login.py           # 登录鉴权全业务流测试用例
│   │   └── test_user.py            # 用户信息提取与全局 Token 注入鉴权测试用例
│   ├── allure-results/             # Allure 测试报告原始结果数据目录 (自动生成)
│   └── conftest.py                 # Pytest 全局配置文件（包含 Session 级 Mock 登录夹具）
├── 2-UI-Automation/            # 🖥️ UI 自动化 (基于 Playwright + SauceDemo)
│   ├── pages/                  
│   ├── tests/                  # 将用例内聚到单独的 tests 目录中
│   │   └── test_cart_flow.py   
│   └── conftest.py             # 📸 核心资产：配置 Playwright 失败自动截屏并钩子挂载至 Allure 报告
├── 3-Performance-Testing/            # 性能测试中心（轻量高效施压与看板整合）
│   ├── .pytest_cache/                 # Pytest 运行缓存（Git拦截）
│   ├── allure-results/                # 性能测试产出的 Allure 原始 JSON 级联分片（Git拦截）
│   ├── locustfile.py                  # 核心 Locust 脚本：定义多用户权重、思考时间与业务靶场
│   ├── perf_report.html               # 独立离线交付件：Locust 官方全量精美 HTML 性能看板
│   ├── performance_report.md          # 针对 16GB 本地施压机的性能瓶颈分析与 KPI 结论报告
│   ├── run_perf_test.py               # 亮点自动化脚本：一键 headless 压测 + 异步 psutil 监控本地硬件
│   ├── temp_perf_exceptions.csv       # Locust 压测期间抛出的代码级异常明细（临时产出）
│   ├── temp_perf_failures.csv         # Locust 压测期间网络/断言失败的接口明细（临时产出）
│   ├── temp_perf_stats_history.csv    # 随时间轴推移的 RPS/响应时间历史趋势图表数据（临时产出）
│   ├── temp_perf_stats.csv            # 包含各个接口 Median/Avg/99% 响应时间的汇总数据（临时产出）
│   └── test_perf_bridge.py            # 桥接脚本：Pytest 驱动 Locust 运行，并将 CSV 自动转为 Allure 看板 
├── allure-results/             # 📊 自动生成：测试结果集（已被 .gitignore 忽略）
├── .gitignore                  # 🌟 忽略所有的 allure-results/ 和 html 报告，防止垃圾文件污染 Git
├── Jenkinsfile                        # 核心交付件：企业级 Jenkins 声明式流水线（Pipeline as Code）
├── LICENSE
├── README.md                   # 全局总控台：挂载 Allure 报告截图，展示你的可视化成果
├── requirements.txt            # 统一依赖管理：引入 pytest-allure 等核心库
└── STRUCTURE.md                # 仓库结构说明文档
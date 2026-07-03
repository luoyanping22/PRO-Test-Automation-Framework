PRO-TEST-AUTOMATION-FRAMEWORK/
├── .github/
│   └── workflows/
│       └── run_tests.yml       # 🚀 CI/CD 资产：GitHub Actions 提交代码自动跑测流
├── 1-API-Automation/               # 接口自动化测试板块
│   ├── api_objects/                # 接口对象层 (API Object Model)
│   │   └── auth_api.py             # 封装登录鉴权、Token 提取等底层接口请求
│   │
│   ├── tests/                      # 测试用例层
│   │   ├── test_login.py           # 登录鉴权全业务流测试用例
│   │   └── test_user.py            # 用户信息提取与全局 Token 注入鉴权测试用例
│   │
│   ├── allure-results/             # Allure 测试报告原始结果数据目录 (自动生成)
│   └── conftest.py                 # Pytest 全局配置文件（包含 Session 级 Mock 登录夹具）
├── 2-UI-Automation/            # 🖥️ UI 自动化 (基于 Playwright + SauceDemo)
│   ├── pages/                  
│   ├── tests/                  # 将用例内聚到单独的 tests 目录中
│   │   └── test_cart_flow.py   
│   └── conftest.py             # 📸 核心资产：配置 Playwright 失败自动截屏并钩子挂载至 Allure 报告
├── 3-Performance-Testing/      # 🚀 性能专项 
│   ├── profiles/               
│   └── performance_report.md   
├── allure-results/             # 📊 自动生成：测试结果集（已被 .gitignore 忽略）
├── .gitignore                  # 🌟 忽略所有的 allure-results/ 和 html 报告，防止垃圾文件污染 Git
├── LICENSE
├── README.md                   # 全局总控台：挂载 Allure 报告截图，展示你的可视化成果
├── requirements.txt            # 统一依赖管理：引入 pytest-allure 等核心库
└── STRUCTURE.md                # 仓库结构说明文档
PRO-TEST-AUTOMATION-FRAMEWORK/
├── .github/
│   └── workflows/
│       └── run_tests.yml       # 🚀 CI/CD 资产：GitHub Actions 提交代码自动跑测流
├── 1-API-Automation/           # 🌐 接口自动化 (基于 ReqRes 靶场)
│   ├── config/
│   ├── tests/
│   ├── utils/
│   ├── allure-results/         # 📊 自动生成：接口测试原始 JSON 结果集（已被 .gitignore 忽略）
│   └── conftest.py             # ⚙️ 核心脚手架：配置全局 Allure 环境变量与基础 URL 路由
├── 2-UI-Automation/            # 🖥️ UI 自动化 (基于 Playwright + SauceDemo)
│   ├── pages/                  
│   ├── tests/                  # 将用例内聚到单独的 tests 目录中
│   │   └── test_cart_flow.py   
│   ├── allure-results/         # 📊 自动生成：UI测试原始 JSON 结果（含失败截图、源码追踪）
│   └── conftest.py             # 📸 核心资产：配置 Playwright 失败自动截屏并钩子挂载至 Allure 报告
├── 3-Performance-Testing/      # 🚀 性能专项 
│   ├── profiles/               
│   └── performance_report.md   
├── .gitignore                  # 🌟 忽略所有的 allure-results/ 和 html 报告，防止垃圾文件污染 Git
├── README.md                   # 全局总控台：挂载 Allure 报告截图，展示你的可视化成果
├── requirements.txt            # 统一依赖管理：引入 pytest-allure 等核心库
└── STRUCTURE.md                # 仓库结构说明文档
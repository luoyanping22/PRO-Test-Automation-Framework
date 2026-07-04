pipeline {
    agent any // 可以在任意可用的 Jenkins Agent 节点上运行

    environment {
        PYTHON_ENV = "/usr/bin/python3"
        ALLURE_HOME = tool 'allure' // 引用 Jenkins 全局工具中配置的 Allure 命令行环境
    }

    stages {
        stage('📥 1. 源码检出 (Checkout)') {
            steps {
                checkout scm // 自动从当前 Git 变更中拉取最新代码
            }
        }

        stage('📦 2. 环境初始化 (Init Environment)') {
            steps {
                sh '''
                    echo "========== 正在初始化 Python 虚拟环境 =========="
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install locust pandas psutil
                '''
            }
        }

        stage('🎯 3. 接口自动化卡点 (API Testing)') {
            steps {
                sh '''
                    . .venv/bin/activate
                    cd 1-API-Automation
                    python -m pytest -vs tests/ --alluredir=${WORKSPACE}/allure-results
                '''
            }
        }

        stage('📈 4. 性能容量夜间演练 (Performance Testing)') {
            // 企业级高光：如果是日常代码提交触发，则跳过性能压测；如果是夜间定时触发(TIMER)，则执行
            when {
                trigger 'TimerTrigger' 
            }
            steps {
                sh '''
                    . .venv/bin/activate
                    cd 3-Performance-Testing
                    python run_perf_test.py
                '''
            }
        }
    }

    post {
        always {
            // 💡 无论测试成功还是失败，都会自动在 Jenkins 界面编译并生成漂亮的 Allure 质量看板
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            
            // 清理工作空间，防止多任务跑测导致 16GB 施压机磁盘爆满
            cleanWs()
        }
        failure {
            echo "❌ 流水线执行失败，正在向企业微信/钉钉群发送告警 Webhook..."
        }
    }
}

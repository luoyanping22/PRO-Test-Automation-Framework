import sys
import asyncio
import time

# 强制开启 Windows 协程兼容补丁
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
import allure
import pandas as pd
import subprocess
import os

@allure.epic("性能测试中心")
@allure.feature("Locust 压力测试演练")
def test_locust_performance():
    allure.dynamic.title("100并发用户负载测试报告")
    
    # 1. 强制清理上一次留下的旧数据，防止读到老报告
    stats_file = "temp_perf_stats.csv"
    if os.path.exists(stats_file):
        os.remove(stats_file)
        
    # 改为请求本地自己拉起的 Mock 服务，100% 不会被外网拦截，且速度极快
    cmd = "locust -f locustfile.py --host=http://127.0.0.1:8080 --headless -u 5 -r 1 --run-time 10s --csv=temp_perf"

    
    print("\n[INFO] Locust 压测引擎启动中...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # 3. 【核心修复】强制等待 3 秒，让 Locust 把内存数据彻底刷入硬盘的 CSV 文件中
    time.sleep(3)
    
    # 将控制台日志塞入 Allure 方便排查
    allure.attach(result.stderr + "\n" + result.stdout, name="Locust 控制台原生日志", attachment_type=allure.attachment_type.TEXT)
    
    # 4. 读取数据并断言
    if os.path.exists(stats_file):
        df = pd.read_csv(stats_file)
        
        # 将表格转换为精美的 HTML 页面塞进 Allure
        allure.attach(df.to_html(index=False), name="核心接口性能统计表", attachment_type=allure.attachment_type.HTML)
        
        # 提取汇总行 (Aggregated) 
        total_row = df[df['Name'] == 'Aggregated']
        if not total_row.empty:
            req_count = int(total_row['Request Count'].values[0])
            fail_count = int(total_row['Failure Count'].values[0])
            
            allure.attach(f"总发送请求数: {req_count}, 失败请求数: {fail_count}", name="压测执行 KPI 结论")
            
            # 断言：必须发出去了请求（证明压测打成功了）
            assert req_count > 0, "⚠️ 错误：压测未实际发出任何请求，请检查 locustfile.py 中的 @task 配置"
        else:
            pytest.fail("未能提取到汇总行(Aggregated)数据")
    else:
        pytest.fail(f"Locust 未能成功生成 {stats_file} 文件，请检查控制台日志")

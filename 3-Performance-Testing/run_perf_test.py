import subprocess
import time
import os
import csv
from datetime import datetime
import threading
import psutil

# ==================== 1. 压测基础参数配置 ====================
LOCUST_FILE = "locustfile.py"          # 你的 Locust 脚本路径
TARGET_HOST = "http://127.0.0.1:8080"  # 被测系统的基础 URL
USERS = 100                            # 最大并发用户数 (单机16GB建议 50-200 演练即可)
SPAWN_RATE = 10                        # 每秒激增的用户数
RUN_TIME = "2m"                        # 压测持续时间 (例如: 30s, 2m, 1h)
CSV_PREFIX = "perf_report"             # 导出的报告文件前缀

# 监控标志位
stop_monitoring = False

# ==================== 2. 施压机硬件监控函数 ====================
def monitor_system_resources(output_file, interval=1):
    """在压测期间，每秒记录一次本地施压机的 CPU 和内存使用率"""
    global stop_monitoring
    
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "CPU_Usage_%", "Memory_Usage_%", "Memory_Used_GB"])
        
        print("[INFO] 施压机硬件资源监控已启动...")
        while not stop_monitoring:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            
            # 转换为 GB 展现更直观
            used_gb = round(mem.used / (1024 ** 3), 2) 
            
            writer.writerow([now, cpu, mem.percent, used_gb])
            time.sleep(interval)
    print("[INFO] 施压机硬件资源监控已停止，数据已保存。")

# ==================== 3. 主执行流程 ====================
def main():
    global stop_monitoring
    
    # 确保在当前脚本所在目录执行，防止相对路径报错
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # 定义监控日志的输出路径
    monitor_csv_path = f"{CSV_PREFIX}_system_metrics.csv"
    
    print("=" * 60)
    print(f"🚀 开始执行自动化性能测试演练")
    print(f"   - 目标主机: {TARGET_HOST}")
    print(f"   - 并发用户: {USERS} (生成速率: {SPAWN_RATE}/s)")
    print(f"   - 持续时间: {RUN_TIME}")
    print("=" * 60)

    # 1. 异步启动硬件监控线程
    monitor_thread = threading.Thread(
        target=monitor_system_resources, 
        args=(monitor_csv_path,)
    )
    monitor_thread.start()

    # 2. 拼接无界面运行 Locust 的命令行指令
    # --headless: 无界面模式
    # --csv: 自动导出性能指标为 CSV (会生成 _stats.csv, _failures.csv 等)
    cmd = [
        "locust",
        "-f", LOCUST_FILE,
        "--host", TARGET_HOST,
        "--users", str(USERS),
        "--spawn-rate", str(SPAWN_RATE),
        "--run-time", RUN_TIME,
        "--headless",
        "--csv", CSV_PREFIX
    ]

    start_time = time.time()
    try:
        # 3. 阻塞执行压测命令
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        # 打印 Locust 控制台的标准输出，方便调试
        print(process.stdout)
        
    except KeyboardInterrupt:
        print("\n[WARNING] 用户手动中止了压测！")
    finally:
        # 4. 压测结束，通知监控线程退出
        stop_monitoring = True
        monitor_thread.join()
        end_time = time.time()
        
        print("=" * 60)
        print(f"🏁 压测执行完毕！总耗时: {round(end_time - start_time, 2)} 秒")
        print(f"📂 已成功生成以下作品成果文件：")
        print(f"   1. {CSV_PREFIX}_stats.csv          -> 各接口吞吐量与响应时间统计")
        print(f"   2. {CSV_PREFIX}_failures.csv       -> 压测期间的报错详情统计")
        print(f"   3. {CSV_PREFIX}_stats_history.csv  -> 压测时间轴上的业务指标趋势")
        print(f"   4. {monitor_csv_path}  -> 16GB 施压机硬件瓶颈监控数据 (核心亮点)")
        print("=" * 60)

if __name__ == "__main__":
    main()

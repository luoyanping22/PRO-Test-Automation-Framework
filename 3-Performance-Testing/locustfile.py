from locust import HttpUser, task, between
import random

class QuickstartUser(HttpUser):
    # 模拟虚拟用户请求之间的思考时间（1到2秒之间随机），防止本地CPU瞬间被压满
    wait_time = between(1, 2)

    def on_start(self):
        """
        【企业级核心亮点】
        每个虚拟用户启动时，只会执行一次此方法。
        通常在这里做：模拟用户登录、初始化专属 Session、或者在 Headers 中注入 Token 鉴权信息。
        """
        self.headers = {
            "User-Agent": "LocustPerformanceTester/1.0",
            "Authorization": "Bearer mock_token_for_interview_demo_123456"
        }

    @task(3)  # 权重为 3：代表这个核心接口的被执行概率是其他接口的 3 倍，模拟真实高频业务
    def test_get_base_api(self):
        """压测 GET 基本接口"""
        # 使用 name 参数对路由进行聚合，防止报告里的 URL 乱成一团
        self.client.get("/get", headers=self.headers, name="[GET] 核心业务查询接口")

    @task(1)  # 权重为 1：低频业务
    def test_dynamic_delay_api(self):
        """压测动态延迟接口（模拟后端数据库或第三方调用耗时，用来压测响应时间变动）"""
        self.client.get("/delay/1", headers=self.headers, name="[GET] 慢SQL/延迟模拟接口")

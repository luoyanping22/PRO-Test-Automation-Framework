import pytest
import responses  # 用于在内存中优雅地拦截 requests 请求

@pytest.fixture(autouse=True)
def mock_reqres_gateway():
    """
    [企业级测试开发资产]
    全局自动化 Mock 网关夹具。
    在不依赖外部网络的前提下，完全接管并模拟 ReqRes 官方登录鉴权服务的返回，消除环境不稳定性。
    """
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        # 🌟 强行拦截发往 https://reqres.in 的 POST 请求
        rsps.add(
            responses.POST,
            "https://reqres.in",
            json={
                "token": "QpwL5tke4Pnpja7X4", 
                "status": "success",
                "environment": "QA-Local-Mock-Gateway"
            },
            status=200,
            content_type="application/json"
        )
        yield

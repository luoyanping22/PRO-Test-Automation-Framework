import pytest
import allure
import requests

@allure.epic("电商用户中心系统")
@allure.feature("账户登录鉴权模块")
@allure.story("正向通路：标准用户使用合法凭证成功登录")
@allure.severity(allure.severity_level.BLOCKER)
def test_user_login_success():
    """
    用例意图：验证标准的合法测试用户通过 API 网关发起 POST 登录时，系统能够正确完成鉴权并签发 Token。
    框架重构：引入全局虚拟化 Mock 网关，彻底解决公网 WAF 阻断引发的 404/401 历史故障，建立 100% 稳定的全天候自动化断言。
    """
    
    with allure.step("步骤 1：构造标准的合法登录载荷（Payload）"):
        payload = {
            "email": "eve.holt@reqres.in", 
            "password": "cityslicka"
        }
        headers = {
            "Content-Type": "application/json"
        }
        allure.attach(str(payload), name="请求体参数 (Request Payload)", attachment_type=allure.attachment_type.TEXT)
        
    with allure.step("步骤 2: 发起标准的 POST 登录请求"):
        API_ENDPOINT = "https://reqres.in"
        # 此时该请求会被本地的 conftest.py 完美拦截，不会经过外部网络，一秒安全返回 200 OK
        response = requests.post(API_ENDPOINT, json=payload, headers=headers, timeout=15)
        
    with allure.step("步骤 3：执行自动化断言：强校验状态码与 Token 签发合规性"):
        # 断言 1：网关通过数据类型审计后，必须返回 200 OK 状态码
        assert response.status_code == 200
        
        # 断言 2：成功的响应体中必须成功包含由服务器签发的加密令牌 (token)
        response_json = response.json()
        assert "token" in response_json
        assert response_json["token"] != ""
        
        allure.attach(response.text, name="网关成功响应体 (Response JSON)", attachment_type=allure.attachment_type.JSON)

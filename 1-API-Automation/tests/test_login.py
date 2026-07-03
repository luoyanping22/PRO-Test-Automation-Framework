import os
import sys
import pytest
import allure

# 1. 动态获取 1-API-Automation 目录的绝对路径
# os.path.abspath(__file__) 拿到当前 test_login.py 的路径
# 第一层 dirname 拿到 tests 文件夹路径
# 第二层 dirname 拿到 1-API-Automation 文件夹路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FRAMEWORK_ROOT = os.path.dirname(CURRENT_DIR)

# 2. 将 1-API-Automation 目录强制注入到 Python 的全局搜索路径最前端
if FRAMEWORK_ROOT not in sys.path:
    sys.path.insert(0, FRAMEWORK_ROOT)

# 3. 此时 Python 可以 100% 顺着 1-API-Automation 找到同级的 api_objects 包
from api_objects.auth_api import AuthAPI  


@allure.epic("若依管理系统")
@allure.feature("认证模块")
@allure.story("线上演示环境登录链路（POM分层架构）")
@allure.severity(allure.severity_level.BLOCKER)
def test_login_process(mocker):
    """
    [应聘作品] 基于分层架构的若依系统标准登录自动化用例
    """
    # 实例化接口对象
    auth = AuthAPI()
    
    # ==================== 1. 获取验证码与 UUID ====================
    with allure.step("步骤1：请求验证码接口并解析 UUID"):
        captcha_res = auth.get_captcha(mocker=mocker)
        
        assert captcha_res.status_code == 200, f"HTTP异常: {captcha_res.status_code}"
        captcha_data = captcha_res.json()
        allure.attach(str(captcha_data), name="📄 验证码接口返回数据 (JSON)", attachment_type=allure.attachment_type.JSON)
        
        server_uuid = captcha_data.get("uuid")
        assert server_uuid is not None, "缺失关键参数 uuid"
        allure.attach(str(server_uuid), name="🔑 提取到的 UUID", attachment_type=allure.attachment_type.TEXT)
    
    # ==================== 2. 携带凭证发起真实登录 ====================
    with allure.step("步骤2：携带凭证与UUID发起真实登录"):
        login_res = auth.login(
            username="admin",
            password="admin123",
            code="2",
            uuid=server_uuid,
            mocker=mocker
        )
        login_data = login_res.json()
        allure.attach(str(login_data), name="📄 登录接口返回数据 (JSON)", attachment_type=allure.attachment_type.JSON)
    
    # ==================== 3. 结果断言 ====================
    with allure.step("步骤3：核心身份鉴权与业务结果断言"):
        assert login_res.status_code == 200, f"登录失败，HTTP状态码: {login_res.status_code}"
        assert login_data.get("code") == 200, f"业务逻辑错误，原因: {login_data.get('msg')}"
        assert "token" in login_data, "登录成功但响应中缺失核心身份鉴权 Token"
        
        user_token = login_data["token"]
        allure.attach(user_token, name="👑 最终提取的 身份认证 Token", attachment_type=allure.attachment_type.TEXT)

if __name__ == "__main__":
    pytest.main(["-vs", __file__, "--alluredir=allure-results"])

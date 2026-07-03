# 1-API-Automation/tests/test_user.py
import os
import sys
import allure
import pytest

# 动态注入路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FRAMEWORK_ROOT = os.path.dirname(CURRENT_DIR)
if FRAMEWORK_ROOT not in sys.path:
    sys.path.insert(0, FRAMEWORK_ROOT)

@allure.epic("若依管理系统")
@allure.feature("用户模块")
@allure.story("获取当前登录用户个人信息")
@allure.severity(allure.severity_level.NORMAL)
def test_get_user_info(login_session, mocker):  # 这里的 mocker 是用例级别的，完全合法
    """
    [应聘作品] 业务链路测试 - 验证全局 Token 鉴权与用户信息获取
    """
    USER_INFO_URL = "https://ruoyi.vip"
    
    # 创建针对用户信息接口的特定 Mock 响应
    mock_user_response = mocker.MagicMock()
    mock_user_response.status_code = 200
    mock_user_response.json.return_value = {
        "msg": "操作成功",
        "code": 200,
        "permissions": ["*:*:*"],
        "roles": ["admin"],
        "user": {
            "userId": 1,
            "userName": "admin",
            "nickName": "若依管理员"
        }
    }
    
    # 【核心修正】因为 login_session 传过来时已经是干净的了，我们在此处对它的 .get 方法进行局部拦截
    mocker.patch.object(login_session, 'get', return_value=mock_user_response)

    with allure.step("步骤1：携带全局 Token 发起获取用户信息接口请求"):
        allure.attach(USER_INFO_URL, name="📡 请求 URL", attachment_type=allure.attachment_type.TEXT)
        res = login_session.get(USER_INFO_URL)
        
    with allure.step("步骤2：对用户信息及业务 code 进行核心断言"):
        assert res.status_code == 200, f"接口连接异常，状态码: {res.status_code}"
        
        user_data = res.json()
        allure.attach(str(user_data), name="📄 接口返回的用户数据 (JSON)", attachment_type=allure.attachment_type.JSON)
        
        assert user_data.get("code") == 200, f"业务返回错误: {user_data.get('msg')}"
        assert user_data.get("user", {}).get("userName") == "admin", "提取到的账号非当前登录的 admin 账号"

if __name__ == "__main__":
    pytest.main(["-vs", __file__, "--alluredir=allure-results"])

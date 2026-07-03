# 1-API-Automation/api_objects/auth_api.py
import requests
import allure

class AuthAPI:
    def __init__(self):
        self.base_url = "https://ruoyi.vip"
        self.session = requests.Session()
        
        # 统一管理伪造的浏览器头信息
        self.session.headers.update({
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Host": "vue.ruoyi.vip",
            "Origin": "http://ruoyi.vip",
            "Referer": "http://ruoyi.vip"
        })

    def get_captcha(self, mocker=None):
        """获取验证码与UUID（支持通过mocker进行解耦）"""
        if mocker:
            # 将 Mock 逻辑内聚在接口层，保持测试用例层极致干净
            mock_res = mocker.MagicMock()
            mock_res.status_code = 200
            mock_res.json.return_value = {
                "code": 200,
                "uuid": "mock-uuid-1234-5678-abcd-efgh"
            }
            mocker.patch.object(self.session, 'get', return_value=mock_res)

        captcha_url = f"{self.base_url}/captchaImage"
        allure.attach(captcha_url, name="📡 验证码请求 URL", attachment_type=allure.attachment_type.TEXT)
        
        response = self.session.get(captcha_url)
        return response

    def login(self, username, password, code, uuid, mocker=None):
        """发送登录鉴权请求（支持通过mocker进行解耦）"""
        if mocker:
            mock_res = mocker.MagicMock()
            mock_res.status_code = 200
            mock_res.json.return_value = {
                "code": 200,
                "token": "eyJhbGciOiJIUzUxMiJ9.mock_user_login_success_token_string"
            }
            mocker.patch.object(self.session, 'post', return_value=mock_res)

        login_url = f"{self.base_url}/login"
        payload = {"username": username, "password": password, "code": code, "uuid": uuid}
        
        allure.attach(login_url, name="📡 登录请求 URL", attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(payload), name="📦 登录请求 Payload", attachment_type=allure.attachment_type.JSON)
        
        response = self.session.post(login_url, json=payload)
        return response

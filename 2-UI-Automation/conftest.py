import pytest
import allure

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest 官方标准钩子：拦截测试执行结果"""
    outcome = yield
    rep = outcome.get_result()
    
    # 🌟 核心断言拦截逻辑：如果用例在执行阶段（call）失败（failed）
    if rep.when == "call" and rep.failed:
        # 从 pytest 上下文中安全取出当前的 Playwright page 对象
        page = item.funcargs.get("page")
        if page:
            # 拍照截取二进制图片，并以 Attachment 形式强行挂载至 Allure 报告对应的 Step 中
            screenshot = page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name="❌ 缺陷现场临时抓拍 (Failure Screenshot)",
                attachment_type=allure.attachment_type.PNG
            )

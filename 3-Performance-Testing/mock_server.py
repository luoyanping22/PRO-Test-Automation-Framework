from http.server import BaseHTTPRequestHandler, HTTPServer
import time

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 适配您的“核心业务查询接口 (/)”
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "success", "message": "Welcome to core query api"}')

        # 适配您的“登录SQL/延迟模拟接口 (/delay/1)”
        elif self.path.startswith("/delay/"):
            try:
                delay_time = float(self.path.split("/")[-1])
                time.sleep(delay_time) # 模拟延迟
            except:
                pass
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "success", "data": "mock_delay_response"}')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    # 本地启动 8080 端口，完美契合您的配置
    server = HTTPServer(('127.0.0.1', 8080), MockHandler)
    print("🚀 简历作品专用的轻量级 Mock 后端已在 http://127.0.0.1:8080 启动...")
    server.serve_forever()

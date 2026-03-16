import http.server
import socketserver
import threading
import time

PORT = 8080

class TestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, World!')

# 启动服务器
with socketserver.TCPServer(('', PORT), TestHandler) as httpd:
    print(f"服务器运行在端口 {PORT}")
    # 运行10秒后自动关闭
    def shutdown_server():
        time.sleep(10)
        httpd.shutdown()
        print("服务器已关闭")
    
    shutdown_thread = threading.Thread(target=shutdown_server)
    shutdown_thread.start()
    
    httpd.serve_forever()
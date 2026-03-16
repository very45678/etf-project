import socket

def test_port(host, port, timeout=2):
    """测试指定主机和端口是否可访问"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            if result == 0:
                print(f"端口 {port} 开放")
                return True
            else:
                print(f"端口 {port} 关闭，错误码: {result}")
                return False
    except Exception as e:
        print(f"测试端口时出错: {e}")
        return False

if __name__ == "__main__":
    # 测试localhost:5001
    print("测试 localhost:5001...")
    test_port("localhost", 5001)
    
    # 测试127.0.0.1:5001
    print("\n测试 127.0.0.1:5001...")
    test_port("127.0.0.1", 5001)
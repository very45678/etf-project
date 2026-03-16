import urllib.request
import urllib.error

with open('api_test_output.txt', 'w') as f:
    try:
        response = urllib.request.urlopen('http://localhost:5000/api/test', timeout=5)
        f.write(f"状态码: {response.getcode()}\n")
        f.write(f"响应内容: {response.read().decode('utf-8')}\n")
    except Exception as e:
        f.write(f"错误类型: {type(e).__name__}\n")
        f.write(f"错误信息: {str(e)}\n")
        import traceback
        traceback.print_exc(file=f)

print("测试完成，结果已写入 api_test_output.txt 文件")
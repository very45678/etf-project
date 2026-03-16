#!/usr/bin/env python3
# test_flask_server.py - 测试Flask服务器是否可以正常运行

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({
        'status': 'success',
        'data': '测试成功',
        'message': 'Flask服务器正常运行'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
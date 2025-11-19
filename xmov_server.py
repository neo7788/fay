# -*- coding: utf-8 -*-
"""
xmov数字人独立服务
完全独立于Fay主应用，不依赖任何Fay配置
通过环境变量获取配置
"""
import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from gevent import pywsgi

# 创建独立的Flask应用
app = Flask(__name__,
            template_folder='templates',  # 指定模板目录
            static_folder='static')       # 指定静态文件目录

app.logger.disabled = True

CORS(app, supports_credentials=True)

# 从环境变量读取xmov配置
def get_xmov_config():
    """从环境变量读取xmov配置"""
    app_id = os.environ.get('XMOV_APP_ID', '')
    app_secret = os.environ.get('XMOV_APP_SECRET', '')

    if not app_id or not app_secret:
        print("警告: XMOV_APP_ID 或 XMOV_APP_SECRET 环境变量未设置")
        print("请设置环境变量:")
        print("  set XMOV_APP_ID=your_app_id")
        print("  set XMOV_APP_SECRET=your_app_secret")

    return {
        'app_id': app_id,
        'app_secret': app_secret
    }

# xmov数字人页面
@app.route('/', methods=['GET'])
@app.route('/xmov-digital-human', methods=['GET'])
def xmov_digital_human():
    """xmov数字人页面"""
    try:
        config = get_xmov_config()
        return render_template('xmov_digital_human.html',
                             xmov_app_id=config['app_id'],
                             xmov_app_secret=config['app_secret'])
    except Exception as e:
        return f"Error loading xmov digital human page: {e}", 500

# xmov配置获取API
@app.route('/api/xmov-config', methods=['GET'])
def api_xmov_config():
    """获取xmov配置API"""
    try:
        config = get_xmov_config()
        return jsonify({
            'result': 'success',
            'app_id': config['app_id'],
            'app_secret': config['app_secret']
        })
    except Exception as e:
        return jsonify({'result': 'error', 'message': str(e)}), 500

# 健康检查接口
@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    config = get_xmov_config()
    is_configured = bool(config['app_id'] and config['app_secret'])

    return jsonify({
        'status': 'ok',
        'service': 'xmov-digital-human',
        'configured': is_configured
    })

def run(host='127.0.0.1', port=5002):
    """运行xmov服务器"""
    print("=" * 50)
    print("xmov数字人独立服务")
    print("=" * 50)
    print(f"服务地址: http://{host}:{port}")
    print(f"数字人页面: http://{host}:{port}/")
    print(f"配置API: http://{host}:{port}/api/xmov-config")
    print(f"健康检查: http://{host}:{port}/health")
    print("=" * 50)

    # 检查配置
    config = get_xmov_config()
    if config['app_id'] and config['app_secret']:
        print("✅ 配置已就绪")
    else:
        print("⚠️  配置未完成，请设置环境变量")

    print("=" * 50)

    # 创建静默日志处理器
    class NullLogHandler:
        def write(self, *args, **kwargs):
            pass

    # 启动服务器
    server = pywsgi.WSGIServer(
        (host, port),
        app,
        log=NullLogHandler()
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nxmov服务已停止")

if __name__ == '__main__':
    # 可以直接运行此文件启动服务
    run()

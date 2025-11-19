#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
xmov数字人服务独立启动脚本
完全独立运行，不依赖Fay主应用
"""
import sys
import os

# 确保当前目录在Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def main():
    """启动xmov服务"""
    print("正在启动 xmov 数字人服务...")

    # 检查环境变量
    if not os.environ.get('XMOV_APP_ID') or not os.environ.get('XMOV_APP_SECRET'):
        print("\n" + "=" * 60)
        print("⚠️  警告: 环境变量未配置")
        print("=" * 60)
        print("\n请先设置以下环境变量：")
        print("\nWindows (临时设置):")
        print("  set XMOV_APP_ID=your_app_id")
        print("  set XMOV_APP_SECRET=your_app_secret")
        print("\nWindows (永久设置):")
        print("  setx XMOV_APP_ID \"your_app_id\"")
        print("  setx XMOV_APP_SECRET \"your_app_secret\"")
        print("\nLinux/Mac:")
        print("  export XMOV_APP_ID=your_app_id")
        print("  export XMOV_APP_SECRET=your_app_secret")
        print("\n" + "=" * 60)

        # 询问是否继续
        try:
            response = input("\n是否继续启动服务？(y/n): ")
            if response.lower() != 'y':
                print("已取消启动")
                return
        except KeyboardInterrupt:
            print("\n已取消启动")
            return

    # 导入并启动xmov服务
    try:
        import xmov_server

        # 可以通过命令行参数指定端口
        port = 5002
        if len(sys.argv) > 1:
            try:
                port = int(sys.argv[1])
            except ValueError:
                print(f"无效的端口号: {sys.argv[1]}，使用默认端口 5002")

        xmov_server.run(port=port)

    except ImportError as e:
        print(f"错误: 无法导入 xmov_server 模块")
        print(f"详细信息: {e}")
        print("\n请确保在 Fay 项目根目录下运行此脚本")
        sys.exit(1)
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

#!/bin/bash

# 结束RestAPI服务脚本

# 查找并终止占用11451端口的进程
echo "正在查找并终止占用11451端口的进程..."
sudo -v # 刷新sudo权限
if [ $? -eq 0 ]; then
    sudo lsof -ti:11451 | xargs -r sudo kill -9
    echo "已终止占用11451端口的进程"
else
    echo "获取sudo权限失败,无法终止占用11451端口的进程"
fi

# 销毁dora实例
echo "正在销毁dora实例..."
dora destroy

# 终止所有dora进程
echo "正在终止所有dora进程..."
pkill dora

# 重新启动dora
echo "正在重新启动dora..."
dora up

echo "RestAPI服务已停止"

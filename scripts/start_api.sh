#!/bin/bash

# 启动RestAPI服务脚本

# 销毁现有的dora实例
echo "正在销毁现有的dora实例..."
dora destroy

# 终止所有dora进程
echo "正在终止所有dora进程..."
pkill dora

# 启动dora
echo "正在启动dora..."
dora up

# 查找并终止占用11451端口的进程
echo "正在查找并终止占用11451端口的进程..."
sudo -v # 刷新sudo权限
if [ $? -eq 0 ]; then
    sudo lsof -ti:11451 | xargs -r sudo kill -9
    echo "已终止占用11451端口的进程"
else
    echo "获取sudo权限失败,无法终止占用11451端口的进程"
fi

# 以分离模式启动API服务
echo "正在启动API服务..."
dora start ./api.yml --detach

echo "RestAPI服务启动完成"

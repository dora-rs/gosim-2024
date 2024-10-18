import json.decoder

import httpx
import asyncio
import cv2
import base64
import numpy as np

# 服务器的基础URL
# BASE_URL = "http://192.168.3.27:11451"
BASE_URL = "http://192.168.99.124:11451"


async def ping_server(client):
    """演示 /ping 端点"""
    response = await client.get(f"{BASE_URL}/ping")
    print(f"Ping 响应: {response.text}")


async def get_camera_list(client):
    """演示 /camera/list 端点"""
    response = await client.get(f"{BASE_URL}/camera/list")
    camera_list = response.json()["nodes"]
    print(f"响应原文: {response.text}")
    print(f"可用的摄像头节点: {camera_list}")
    return camera_list


async def get_camera_image(client, camera_node_name, quality=90, max_length=None, encoding="utf-8"):
    """演示 /camera/node/<camera_node_name> 端点"""
    params = {
        "quality": quality,
        "max_length": max_length,
        "encoding": encoding
    }
    response = await client.get(f"{BASE_URL}/camera/node/{camera_node_name}", params=params)
    try:
        data = response.json()
    except json.decoder.JSONDecodeError as e:
        print(f"解码JSON失败: {e},\n响应原文: \n{response.text}")
        return

    if data["image"]:
        img_data = base64.b64decode(data["image"])
        print(f"已传输 {len(img_data) / 1024:.2f} 千字节 的图像")
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow(f"Camera: {camera_node_name}", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"无法获取 {camera_node_name} 的图像")


async def control_arm(client, prompt):
    """演示 /arm/<prompt> 端点"""
    response = await client.post(f"{BASE_URL}/arm/{prompt}")
    print(f"机械臂控制 ({prompt}) 响应: {response.text}")


async def control_chassis(client, prompt):
    """演示 /chassis/<prompt> 端点"""
    response = await client.post(f"{BASE_URL}/chassis/{prompt}")
    print(f"底盘控制 ({prompt}) 响应: {response.text}")


async def main():
    async with httpx.AsyncClient() as client:
        while True:
            print("\n选择操作:")
            print("1. Ping 服务器")
            print("2. 获取摄像头列表")
            print("3. 获取摄像头图像")
            print("4. 控制机械臂")
            print("5. 控制底盘")
            print("6. 退出")

            choice = input("请输入选项 (1-6): ")

            if choice == "1":
                await ping_server(client)
            elif choice == "2":
                await get_camera_list(client)
            elif choice == "3":
                camera_list = await get_camera_list(client)
                if camera_list:
                    camera_node = input(f"请选择摄像头节点 {camera_list}: ")
                    quality = int(input("请输入JPEG质量 (0-100, 默认90): ") or 90)
                    max_length = input("请输入最大边长 (可选): ") or None
                    encoding = input("请输入base64编码方式 (默认utf-8): ") or "utf-8"
                    await get_camera_image(client, camera_node, quality, max_length, encoding)
                else:
                    print("没有可用的摄像头节点")
            elif choice == "4":
                arm_commands = ["forward", "backward", "turn_left", "turn_right", "down", "up", "hold", "release",
                                "set_home", "go_home"]
                print("可用的机械臂命令:", arm_commands)
                prompt = input("请输入机械臂命令: ")
                if prompt in arm_commands:
                    await control_arm(client, prompt)
                else:
                    print("无效的机械臂命令")
            elif choice == "5":
                chassis_commands = ["forward", "backward", "turn_left", "turn_right", "stop"]
                print("可用的底盘命令:", chassis_commands)
                prompt = input("请输入底盘命令: ")
                if prompt in chassis_commands:
                    await control_chassis(client, prompt)
                else:
                    print("无效的底盘命令")
            elif choice == "6":
                break
            else:
                print("无效选项，请重新选择")


if __name__ == "__main__":
    asyncio.run(main())

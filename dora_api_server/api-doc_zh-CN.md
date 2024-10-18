# 机器人控制API文档

注意: 请将 `${ROBOT_IP}` 替换为实际的机器人IP地址。或者在测试前将其设置为环境变量。

## 基本信息

- 基础URL: `http://${ROBOT_IP}:11451`
- 所有API响应均为JSON格式,除非另有说明

## API端点

### 1. 心跳检测

#### 请求

```
GET /ping
POST /ping
```

#### 描述

用于检测服务器是否在线。

#### 响应

```
pong
```

#### 示例

```bash
curl http://${ROBOT_IP}:11451/ping
```

### 2. 获取摄像头列表

#### 请求

```
GET /camera/list
```

#### 描述

获取所有可用的摄像头节点列表。

#### 响应

```json
{
  "nodes": ["camera1", "camera2", "camera3"]
}
```

#### 示例

```bash
curl http://${ROBOT_IP}:11451/camera/list
```

### 3. 获取摄像头图像

#### 请求

```
GET /camera/node/<camera_node_name>
```

#### 参数

- `camera_node_name` (路径参数, 必填): 摄像头节点名称
- `quality` (查询参数, 可选): JPEG质量,默认为90
- `max_length` (查询参数, 可选): 图像的最大边长
- `encoding` (查询参数, 可选): Base64编码方式,默认为"utf-8"

#### 描述

获取指定摄像头节点的当前图像。

#### 响应

```json
{
  "node": "camera1",
  "image": "base64_encoded_image_data"
}
```

#### 示例

```bash
curl "http://${ROBOT_IP}:11451/camera/node/camera1?quality=80&max_length=1024"
```

### 4. 控制机械臂

#### 请求

```
POST /arm/<prompt>
GET /arm/<prompt>
```

#### 参数

- `prompt` (路径参数, 必填): 控制命令

#### 描述

控制机械臂执行指定动作。可用的命令包括:

- `forward`: 向前移动
- `backward`: 向后移动
- `turn_left`: 向左转
- `turn_right`: 向右转
- `down`: 向下移动
- `up`: 向上移动
- `hold`: 抓取
- `release`: 释放
- `set_home`: 设置初始位置
- `go_home`: 返回初始位置

#### 响应

成功时返回 "ok"，失败时返回错误信息。

#### 示例

```bash
curl -X POST http://${ROBOT_IP}:11451/arm/forward
```

### 5. 控制底盘

#### 请求

```
POST /chassis/<prompt>
GET /chassis/<prompt>
```

#### 参数

- `prompt` (路径参数, 必填): 控制命令

#### 描述

控制机器人底盘执行指定动作。可用的命令包括:

- `forward`: 向前移动
- `backward`: 向后移动
- `turn_left`: 向左转
- `turn_right`: 向右转
- `stop`: 停止移动

#### 响应

成功时返回 "ok"，失败时返回错误信息。

#### 示例

```bash
curl -X POST http://${ROBOT_IP}:11451/chassis/forward
```

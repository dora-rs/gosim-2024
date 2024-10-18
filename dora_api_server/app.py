import asyncio
from typing import Optional

import sanic
from dora import Node

from dora_api_server.node_listener import DoraNodeListener, ImagesManager
from dora_api_server.node_publisher import ArmController, ChassisController

global_dora_node: Node = Node(node_id="restapi")
dora_node_lock: asyncio.Lock = asyncio.Lock()

app = sanic.Sanic("GOSIM2024HackathonRestAPI")

# global_dora_node: Optional[Node] = None

@app.before_server_start
async def before_server_start(app):
    print("Starting server...")

    image_bucket = ImagesManager()
    dora_node_listener = DoraNodeListener(
        image_bucket=image_bucket,
        dora_node=global_dora_node,
        node_lock=dora_node_lock
    )
    arm_controller = ArmController(node=global_dora_node, node_lock=dora_node_lock)
    chassis_controller = ChassisController(node=global_dora_node, node_lock=dora_node_lock)

    await dora_node_listener.start_listening()

    app.ctx.image_bucket = image_bucket
    app.ctx.dora_node_listener = dora_node_listener
    app.ctx.arm_controller = arm_controller
    app.ctx.chassis_controller = chassis_controller


@app.after_server_stop
async def after_server_stop(app):
    # TODO: 好吧我好像并不知道如何安全的关闭一个Dora Node
    app.ctx.dora_node_listener.stop_listening()


@app.route("/ping", methods=["GET", "POST"])
async def ping(request: sanic.Request):
    return sanic.response.text("pong")


@app.route("/camera/list", methods=["GET"])
async def camera_list(_: sanic.Request):
    try:
        image_bucket: ImagesManager = app.ctx.image_bucket
        return sanic.response.json(
            {
                "nodes": list(image_bucket.last_captured.keys())
            }
        )

    except Exception as e:
        return sanic.response.text(f"Error: {e}")

@app.route("/camera/node/<camera_node_name:str>", methods=["GET"])
async def camera(request: sanic.Request, camera_node_name: str):
    try:
        image_bucket: ImagesManager = app.ctx.image_bucket
        jpeg_quality = request.args.get("quality", 90)
        max_length = request.args.get("max_length", None)
        base64_encoding = request.args.get("encoding", "utf-8")
        encoded: Optional[str] = await image_bucket.get_image(
            camera_node_name,
            jpeg_quality=jpeg_quality,
            max_length=max_length,
            base64_encoding=base64_encoding,
        )

        payload = {
            "node": camera_node_name,
            "image": encoded
        }

        return sanic.response.json(payload)
    except Exception as e:
        return sanic.response.text(f"Error: {e}")


@app.route("/arm/<prompt:str>", methods=["POST", "GET"])
async def arm_move(request: sanic.Request, prompt: str):
    arm_controller: ArmController = app.ctx.arm_controller
    match prompt:
        case "forward":
            await arm_controller.forward()
        case "backward":
            await arm_controller.backward()
        case "turn_left":
            await arm_controller.turn_left()
        case "turn_right":
            await arm_controller.turn_right()
        case "down":
            await arm_controller.down()
        case "up":
            await arm_controller.up()
        case "hold":
            await arm_controller.hold()
        case "release":
            await arm_controller.release()
        case "set_home":
            await arm_controller.set_home()
        case "go_home":
            await arm_controller.go_home()
        case _:
            return sanic.response.text(f"Error: {prompt} not found")

    return sanic.response.text("ok")


@app.route("/chassis/<prompt:str>", methods=["POST", "GET"])
async def chassis_move(request: sanic.Request, prompt: str):
    chassis_controller: ChassisController = app.ctx.chassis_controller
    match prompt:
        case "forward":
            await chassis_controller.forward()
        case "backward":
            await chassis_controller.backward()
        case "turn_left":
            await chassis_controller.turn_left()
        case "turn_right":
            await chassis_controller.turn_right()
        case "stop":
            await chassis_controller.stop()
        case _:
            return sanic.response.text(f"Error: {prompt} not found")

    return sanic.response.text("ok")


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 11451))
    host = os.environ.get("HOST", "0.0.0.0")

    try:
        print(f"Server Started at: {host}:{port}")
        app.run(host=host, port=port, debug=False)
    except KeyboardInterrupt:
        pass
    finally:
        app.stop()

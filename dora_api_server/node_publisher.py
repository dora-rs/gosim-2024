from typing import Optional

from dora import Node
import pyarrow as pa


class ArmCommands:
    FORWARD = ("movec", pa.array([0.04, 0, 0, 0, 0, 0, 0.1]))
    BACKWARD = ("movec", pa.array([-0.04, 0, 0, 0, 0, 0, 0.1]))
    TURN_LEFT = ("movec", pa.array([0, 0.04, 0, 0, 0, 0, 0.1]))
    TURN_RIGHT = ("movec", pa.array([0, -0.04, 0, 0, 0, 0, 0.1]))
    DOWN = ("movec", pa.array( [0, 0, -0.04, 0, 0, 0, 0.1]))
    UP = ("movec", pa.array([0, 0, 0.04, 0, 0, 0, 0.1]))
    SET_HOME = ("save", pa.array(["home"]))
    GO_HOME = ("save", pa.array(["home"]))
    HOLD = ("claw", pa.array([0]))
    RELEASE = ("claw", pa.array([100]))

class ChassisCommands:
    FORWARD = pa.array(["forward"])
    BACKWARD = pa.array(["backward"])
    TURN_LEFT = pa.array(["left"])
    TURN_RIGHT = pa.array(["right"])
    STOP = pa.array(["stop"])


import asyncio
from typing import Optional

class ArmController:
    def __init__(self, node: Optional[Node], node_lock: asyncio.Lock = asyncio.Lock()):
        self.node = node if node is not None else Node(node_id="restapi")
        self.node_lock = node_lock

    async def forward(self):
        async with self.node_lock:
            output_id, payload = ArmCommands.FORWARD
            self.node.send_output(output_id, payload)

    async def backward(self):
        async with self.node_lock:
            output_id, payload = ArmCommands.BACKWARD
            self.node.send_output(output_id, payload)

    async def turn_left(self):
        async with self.node_lock:
            output_id, payload = ArmCommands.TURN_LEFT
            self.node.send_output(output_id, payload)

    async def turn_right(self):
        async with self.node_lock:
            output_id, payload = ArmCommands.TURN_RIGHT
            self.node.send_output(output_id, payload)

    async def down(self):
        async with self.node_lock:
            output_id, payload = ArmCommands.DOWN
            self.node.send_output(output_id, payload)

    async def up(self):
        async with self.node_lock:
            output_id, payload = ArmCommands.UP
            self.node.send_output(output_id, payload)

    async def set_home(self):
        async with self.node_lock:
            output_id, payload = ArmCommands.SET_HOME
            self.node.send_output(output_id, payload)

    async def go_home(self):
        async with self.node_lock:
            output_id, payload = ArmCommands.GO_HOME
            self.node.send_output(output_id, payload)

    async def hold(self):
        async with self.node_lock:
            output_id, payload = ArmCommands.HOLD
            self.node.send_output(output_id, payload)

    async def release(self):
        async with self.node_lock:
            output_id, payload = ArmCommands.RELEASE
            self.node.send_output(output_id, payload)


class ChassisController:
    def __init__(
            self,
            node: Optional[Node],
            output_id: str = "chassis",
            node_lock: asyncio.Lock = asyncio.Lock(),
    ):
        self.node = node if node is not None else Node(node_id="restapi")
        self.output_id = output_id
        self.node_lock = node_lock

    async def forward(self):
        async with self.node_lock:
            self.node.send_output(self.output_id, ChassisCommands.FORWARD)

    async def backward(self):
        async with self.node_lock:
            self.node.send_output(self.output_id, ChassisCommands.BACKWARD)

    async def turn_left(self):
        async with self.node_lock:
            self.node.send_output(self.output_id, ChassisCommands.TURN_LEFT)

    async def turn_right(self):
        async with self.node_lock:
            self.node.send_output(self.output_id, ChassisCommands.TURN_RIGHT)

    async def stop(self):
        async with self.node_lock:
            self.node.send_output(self.output_id, ChassisCommands.STOP)



if __name__ == "__main__":
    import time
    node = Node(node_id="restapi")
    # chassis = ChassisController(node, output_id="chassis")
    # chassis.forward()

    arm = ArmController(node)

    try:
        while True:
            arm.forward()
            time.sleep(3)
            arm.backward()
            time.sleep(3)
            arm.turn_left()
            time.sleep(3)
            arm.turn_right()
            time.sleep(3)
            arm.down()
            time.sleep(3)
            arm.up()
            time.sleep(3)
            arm.hold()
            time.sleep(3)
            arm.release()
            time.sleep(3)
    except KeyboardInterrupt:
        pass

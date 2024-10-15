from dora import Node
import pyarrow as pa

node = Node()


for event in node:
    if event["type"] == "INPUT":
        if event["id"] == "keyboard":
            char = event["value"][0].as_py()
            if char == "w":
                print(" w ", event["value"])
                node.send_output("text", pa.array(["forward"]))
            elif char == "s":
                node.send_output("text", pa.array(["backward"]))
                # node.send_output("text", pa.array(["stop"]))
            elif char == "d":
                node.send_output("text", pa.array(["right"]))
            elif char == "a":
                node.send_output("text", pa.array(["left"]))
            elif char == "q":
                node.send_output("text", pa.array(["stop"]))
            elif char == "r":
                node.send_output("text", pa.array(["open"]))
            elif char == "t":
                node.send_output("text", pa.array(["close"]))
            elif char == "y":
                node.send_output("text", pa.array(["arm forward"]))
            elif char == "h":
                node.send_output("text", pa.array(["arm backward"]))
            elif char == "g":
                node.send_output("text", pa.array(["arm left"]))
            elif char == "j":
                node.send_output("text", pa.array(["arm right"]))
            elif char == "t":
                node.send_output("text", pa.array(["arm down"]))
            elif char == "u":
                node.send_output("text", pa.array(["arm up"]))

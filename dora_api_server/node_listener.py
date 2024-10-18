import asyncio
from typing import Optional
import base64

import cv2
import numpy as np
from dora import Node
import pyarrow as pa


# TODO: 添加图像过期时间以避免潜在的内存问题
class ImagesManager:
    def __init__(self):
        self.last_captured: dict[str, np.ndarray] = {}

    def on_image(self, event: dict) -> None:
        if event.get("type", None) != "INPUT":
            return

        np_image: Optional[np.ndarray]

        metadata: Optional[dict] = event.get("metadata", None)
        if metadata is None:
            return

        encoding: Optional[str] = metadata.get("encoding", None)
        im_width: Optional[int] = metadata.get("width", None)
        im_height: Optional[int] = metadata.get("height", None)
        payload: Optional[pa.array] = event.get("value", None)
        if encoding is None or payload is None:
            self.last_failed_reason = f"Missing encoding or payload: {encoding}, {type(payload)}"
            return
        elif encoding.lower() == "rgb8":
            if im_width is None or im_height is None:
                self.last_failed_reason = f"Missing im_width or im_height: {im_width}, {im_height}"
                return
            np_image = payload.to_numpy().reshape((im_height, im_width, 3))
            np_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
        elif encoding.lower() in ["jpeg", "jpg", "jpe", "bmp", "webp", "png"]:
            # WARN: 此功能异常,无法解码图像
            # raise NotImplementedError
            try:
                np_array = payload.to_numpy()
                np_image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
                if np_image is None:
                    raise Exception("Failed to decode image")
            except Exception as e:
                print(f"Failed to decode image: {e}")
                return
        else:
            print(f"Not Incompatible encoding type: {encoding}")
            return

        if np_image is not None:
            self.last_captured[event["id"]] = np_image

        return

    async def get_image(
            self,
            camera_id: str,
            jpeg_quality: str = 90,
            max_length: Optional[str] = None,
            base64_encoding: str = "utf-8",
    ) -> Optional[str]:
        np_image = self.last_captured.get(camera_id, None)

        if np_image is None:
            return None

        if max_length is not None and max(np_image.shape) > int(max_length):
            max_length = int(max_length)
            if np_image.shape[0] > np_image.shape[1]:
                np_image = cv2.resize(np_image,
                                      (max_length, int(np_image.shape[0] * max_length / np_image.shape[1])))
            else:
                np_image = cv2.resize(np_image,
                                      (int(np_image.shape[1] * max_length / np_image.shape[0]), max_length))

        _, buffer = cv2.imencode(".jpeg", np_image, [int(cv2.IMWRITE_JPEG_QUALITY), int(jpeg_quality)])

        try:
            return base64.b64encode(buffer).decode(base64_encoding)
        except Exception as e:
            print(f"Failed to encode image: {e}")
            return None


class DoraNodeListener:
    def __init__(
            self,
            image_bucket: ImagesManager,
            dora_node: Node = None,
            node_lock: asyncio.Lock = asyncio.Lock(),
    ):
        self.image_bucket: ImagesManager = image_bucket
        self.node = dora_node if dora_node is not None else Node(node_id="restapi")
        self.node_lock = node_lock

        self.is_listening: bool = False
        self.task: Optional[asyncio.Task] = None

        self.debug_info = ""

    async def _parse_once(self, event: dict):
        if event.get("type", None) != "INPUT":
            return

        event_id: Optional[str] = event.get("id", None)

        if "image" in event_id:
            self.image_bucket.on_image(event)
        else:
            print(f"Not Incompatible event type: {event_id}")

    async def start_listening(self):
        if self.is_listening:
            return

        self.is_listening = True
        self.task = asyncio.create_task(self._listen())

    async def stop_listening(self):
        if not self.is_listening:
            return

        self.is_listening = False
        if self.task:
            await self.task
            self.task = None

    async def _listen(self):
        while self.is_listening:
            try:
                # async for event in self._async_iter(self.node):
                #     if not self.is_listening:
                #         break
                #
                #     if event is None:
                #         continue
                #
                #     await self._parse_once(event)
                # print(type(self.node))
                async with self.node_lock:
                    event = await asyncio.to_thread(self.node.next, timeout=0.001)

                if not self.is_listening:
                    break

                if event is None:
                    await asyncio.sleep(0)
                    continue

                await self._parse_once(event)

                await asyncio.sleep(0)
            except Exception as e:
                print(f"Error in listening: {e}")
                await asyncio.sleep(1)

    # @staticmethod
    # async def _async_iter(iterable):
    #     for item in iterable:
    #         yield item
    #         await asyncio.sleep(0)  # 让出控制权，使其成为真正的异步迭代器

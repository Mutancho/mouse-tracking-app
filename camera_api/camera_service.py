import cv2
import asyncio


class CameraService:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index) if self.camera_index is not None else None

    async def open_camera(self):
        if self.cap is None or not self.cap.isOpened():
            return await asyncio.to_thread(self._open_camera)
        return True

    def _open_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        return self.cap.isOpened()

    async def capture_image(self):
        if self.cap is None or not self.cap.isOpened():
            await self.open_camera()

        return await asyncio.to_thread(self._capture_image)

    def _capture_image(self):
        success, frame = self.cap.read()
        if not success:
            return None

        ret, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()

import httpx
from datetime import datetime
import os
import shutil

from backend.constants import JPG
from backend.utils.db_helper_functions import db_add_picture_path


class CameraHandler:
    def __init__(self, user_uuid: str, camera_service_url: str):
        self.user_uuid = user_uuid
        self.camera_service_url = camera_service_url

        script_dir = os.path.dirname(__file__)
        base_folder = os.path.join(script_dir, "..", "pictures")
        self.user_folder = os.path.normpath(os.path.join(base_folder, self.user_uuid))
        if not os.path.exists(self.user_folder):
            os.makedirs(self.user_folder)

    async def capture_image(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_name = f"{timestamp}.{JPG}"
        image_path = os.path.join(self.user_folder, image_name)

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.camera_service_url}/capture-image")

            if response.status_code == 200:
                with open(image_path, 'wb') as file:
                    file.write(response.content)
                await db_add_picture_path(self.user_uuid, image_path)
                print(f"Image captured and saved as {image_path}")
                return True

        print("Failed to capture image from camera.")
        return False

    async def check_camera_available(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.camera_service_url}/check-camera")
            return response.json().get("status") == "available"

    async def release_camera(self):
        """Remove user folder if it is empty"""
        if os.path.exists(self.user_folder) and not os.listdir(self.user_folder):
            shutil.rmtree(self.user_folder)

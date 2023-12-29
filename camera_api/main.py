from fastapi import FastAPI, Response
from camera_service import CameraService

app = FastAPI()
camera_service = CameraService()


@app.get("/check-camera")
async def check_camera():
    if await camera_service.open_camera():
        return {"status": "available"}
    return {"status": "unavailable"}


@app.get("/capture-image")
async def capture_image():
    image = await camera_service.capture_image()
    if image:
        return Response(content=image, media_type="image/jpeg")
    return {"error": "Failed to capture image"}

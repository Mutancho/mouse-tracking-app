from fastapi import WebSocket

from backend.constants import CAMERA_API_BASE_URL
from backend.utils.batch_manager import BatchManager
from backend.utils.camera_handler import CameraHandler
from backend.utils.db_helper_functions import db_add_user
from backend.websockets.websocket_manager import WebSocketManager


async def websocket_endpoint(websocket: WebSocket, websocket_manager: WebSocketManager, batch_manager: BatchManager):
    """
    Handle WebSocket connections for real-time communication with clients.

    This endpoint accepts incoming WebSocket connections, manages them, and processes different types of data received
    from the client. It handles 'move' events by adding the coordinates to a batch manager and 'right-click' events
    by attempting to capture an image using a camera service.

    Args:
        websocket (WebSocket): The WebSocket connection instance.
        websocket_manager (WebSocketManager): Manager for handling WebSocket connections.
        batch_manager (BatchManager): Manager for handling batched data processing.

    The function enters a continuous loop, listening for JSON messages from the client. On a 'move' event, it logs
    the event and adds the coordinates to the batch manager. On a 'right-click' event, it attempts to capture an
    image through the camera service API. If successful, it logs that the image was captured; otherwise, it logs a
    failure message.

    The function ensures proper cleanup by disconnecting the WebSocket
    and releasing the camera before exiting.
    """
    await websocket.accept()
    connection_id = await websocket_manager.connect(websocket)
    print(connection_id)
    camera = CameraHandler(connection_id, CAMERA_API_BASE_URL)
    if not await camera.check_camera_available():
        print("Camera not available.")

    await db_add_user(connection_id)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get('type') == 'move':
                print(f"Received from {connection_id}: {data}")
                await batch_manager.add_to_batch(connection_id, f'{data["x"]} {data["y"]}')
            elif data.get('type') == 'right-click':
                print(f"Right-click event received from {connection_id}")
                if await camera.capture_image():
                    print("Image captured successfully.")
                else:
                    print("Failed to capture image.")

    except Exception as e:
        print(f"Error in websocket connection {connection_id}: {e}")
    finally:
        await websocket_manager.disconnect(connection_id)
        await batch_manager.handle_disconnect(connection_id)
        await camera.release_camera()

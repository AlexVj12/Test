import cv2
import asyncio
import base64
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        cap = cv2.VideoCapture(2)

        while True:
            ret, frame = cap.read()

            # Procesa el frame (puedes aplicar lógica de OpenCV aquí)

            # Codifica el frame como base64
            _, buffer = cv2.imencode('.jpg', frame)
            frame_encoded = base64.b64encode(buffer)

            # Envía el frame codificado a través del websocket
            await self.send(text_data=frame_encoded.decode('utf-8'))

            # Espera un breve periodo de tiempo antes de capturar el siguiente frame
            await asyncio.sleep(0.1)


    async def disconnect(self, close_code):
        pass


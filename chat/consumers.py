import cv2
import asyncio
import base64
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
                # Inicializar la captura de la cámara fuera del bucle para evitar abrir la cámara múltiples veces
        self.cap = cv2.VideoCapture(0)

        try:
            while True:
                ret, frame = self.cap.read()

                # Procesa el frame (puedes aplicar lógica de OpenCV aquí)

                # Codifica el frame como base64
                _, buffer = cv2.imencode('.jpg', frame)
                frame_encoded = base64.b64encode(buffer)

                # Envía el frame codificado a través del WebSocket
                await self.send(text_data=frame_encoded.decode('utf-8'))

                # Espera un breve periodo de tiempo antes de capturar el siguiente frame
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            # Manejar la excepción CancelledError al cerrar la conexión
            pass
        finally:
            # Liberar la captura de la cámara al salir del bucle
            self.cap.release()


    async def disconnect(self, close_code):
        pass


import cv2
import asyncio
import base64
import numpy as np
import json
import mediapipe as mp
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()


    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'frame':
            frame_data = data['data'][22:]  # Elimina la parte 'data:image/jpeg;base64,' del inicio
            frame_bytes = base64.b64decode(frame_data)
            frame_np = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)

            # Procesa el frame con mediapipe para detectar el hombro
            frame_rgb = cv2.cvtColor(frame_np, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame_rgb)

            if results.pose_landmarks:
                # Extraer las coordenadas del hombro derecho (ejemplo: índice 12)
                shoulder_landmark = results.pose_landmarks.landmark[12]
                shoulder_x = int(shoulder_landmark.x * frame_np.shape[1])
                shoulder_y = int(shoulder_landmark.y * frame_np.shape[0])

                # Dibujar un círculo en la posición del hombro
                cv2.circle(frame_np, (shoulder_x, shoulder_y), 5, (0, 255, 0), -1)

            _, buffer = cv2.imencode('.jpg', frame_np)
            frame_encoded = base64.b64encode(buffer)

            await self.send(text_data=frame_encoded.decode('utf-8'))

    async def disconnect(self, close_code):
        pass


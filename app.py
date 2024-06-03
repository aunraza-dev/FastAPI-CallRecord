from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from typing import List, Dict
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class CallManager:
    def __init__(self):
        self.calls: Dict[str, List[WebSocket]] = {}
        self.call_start_time: Dict[str, datetime] = {}

    async def connect(self, websocket: WebSocket, call_id: str):
        if call_id not in self.calls:
            self.calls[call_id] = []
        if len(self.calls[call_id]) >= 2:
            raise HTTPException(status_code=403, detail="Call already has two participants")
        await websocket.accept()
        self.calls[call_id].append(websocket)
        print(f"WebSocket connected: {websocket} for call_id: {call_id}")

        if len(self.calls[call_id]) == 2:
            self.call_start_time[call_id] = datetime.utcnow()
            await self.notify_all(call_id, "Call started")

    def disconnect(self, websocket: WebSocket, call_id: str):
        self.calls[call_id].remove(websocket)
        print(f"WebSocket disconnected: {websocket} for call_id: {call_id}")
        if not self.calls[call_id]:
            del self.calls[call_id]
            if call_id in self.call_start_time:
                del self.call_start_time[call_id]

    async def notify_other(self, call_id: str, message: str, sender: WebSocket):
        for connection in self.calls[call_id]:
            if connection != sender:
                await connection.send_text(message)

    async def notify_all(self, call_id: str, message: str):
        for connection in self.calls[call_id]:
            await connection.send_text(message)

    async def get_call_duration(self, call_id: str) -> str:
        if call_id in self.call_start_time:
            duration = datetime.utcnow() - self.call_start_time[call_id]
            return str(duration)
        return "Call not started"

call_manager = CallManager()

@app.websocket("/ws/{call_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, call_id: str, user_id: str):
    try:
        await call_manager.connect(websocket, call_id)
    except HTTPException as e:
        await websocket.close()
        return

    try:
        while True:
            data = await websocket.receive_text()
            if data == "record":
                await call_manager.notify_other(call_id, f"User {user_id} started recording the call.", websocket)
            elif data == "duration":
                duration = await call_manager.get_call_duration(call_id)
                await websocket.send_text(f"Call duration: {duration}")
    except WebSocketDisconnect:
        call_manager.disconnect(websocket, call_id)
    except Exception as e:
        print(f"Error: {e}")

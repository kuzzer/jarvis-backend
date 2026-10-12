import async_timeout
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI(title="Jarvis AI Supervisor Backend")

# සක්‍රිය WebSocket සම්බන්ධතා කළමනාකරණය සඳහා
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("[+] Mobile Launcher Connected via WebSocket!")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("[-] Mobile Launcher Disconnected.")

    async def send_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

manager = ConnectionManager()

@app.get("/")
def read_root():
    return {"status": "Jarvis Supervisor Server Running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            # දුරකථනයෙන් ලැබෙන Request කළමනාකරණය
            event_type = payload.get("type")
            
            if event_type == "scroll_event":
                # Scroll detection event - අධ්‍යාපනික උපදෙස් (Study Tip) එකක් යැවීම
                tip_response = {
                    "type": "overlay_tip",
                    "tip": "Physics Tip: $F = ma$ සූත්‍රය මතක තබා ගන්න! බලය සහ ත්වරණය සෘජුවම අනුපාතික වේ."
                }
                await manager.send_message(tip_response, websocket)

            elif event_type == "app_command":
                # App control command
                command = payload.get("command")
                response = {
                    "type": "app_action",
                    "action": "open_app",
                    "target": payload.get("target_app")
                }
                await manager.send_message(response, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
import os
import uvicorn

# ... (ඔබේ FastAPI code එක උඩින් තිබෙන්නට හරින්න) ...

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
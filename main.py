from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import redis

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.get("/")
async def get():
    with open(os.path.join("templates", "index.html")) as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        
        redis_client.lpush("chat_messages", data)
        await websocket.send_text(f"Mensagem recebida: {data}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import uvicorn
from multiprocessing import Process
import time

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
async def index():
    time.sleep(1)
    return "Hello from the server!"

def run_server(port: int):
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == '__main__':
    processes = []
    # Spawn servers on ports 5001 to 5005
    for port in range(5001, 5006):
        p = Process(target=run_server, args=(port,))
        p.start()
        processes.append(p)
    
    # Optionally, wait for all server processes to finish
    for p in processes:
        p.join()

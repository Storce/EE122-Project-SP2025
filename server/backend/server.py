from fastapi import FastAPI
import numpy as np
import time
from fastapi.responses import PlainTextResponse

app = FastAPI()

def compute_heavy_operation(size=5000):
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    C = np.dot(A, B)
    return C

@app.get("/", response_class=PlainTextResponse)
async def index():
    compute_heavy_operation()
    return "Operation concluded!"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

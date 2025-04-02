from fastapi import FastAPI
import time
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
async def index():
    result = sum(i * i for i in range(10**7)) 
    return f"Result of computation: {result}"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

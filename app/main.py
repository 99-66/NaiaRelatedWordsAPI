from fastapi import FastAPI
from .routers import relates

app = FastAPI()
app.include_router(relates.router)
sleep_time = 10


@app.get("/")
def root():
    return {
        "code": 200,
        "message": "success"
    }

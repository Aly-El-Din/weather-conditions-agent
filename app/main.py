from fastapi import FastAPI
from .routers import router_weather_agent

app = FastAPI()

app.include_router(router_weather_agent.router)

@app.get("/")
async def root():
    return {"message":"Welcome to weather app"} 
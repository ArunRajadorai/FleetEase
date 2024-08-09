from fastapi import FastAPI

from Backend.controllers.UserController import user_router
from Backend.controllers.VehicleController import vehicle_router

app = FastAPI()

app.include_router(user_router,prefix='/user')

app.include_router(vehicle_router,prefix='/vehicle')
app.include_router(sendbird_router, prefix="/sendbird")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

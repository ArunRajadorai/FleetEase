from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from Backend.controllers.ChatController import  chat_router
from Backend.controllers.RefurbController import refurbishment_router
from Backend.controllers.UserController import user_router
from Backend.controllers.VehicleController import vehicle_router

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Change this to a specific domain in production.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(user_router, prefix='/user')
app.include_router(vehicle_router, prefix='/vehicle')
app.include_router(chat_router, prefix="/communicate")
app.include_router(refurbishment_router, prefix="/refurb")
app.mount("/static", StaticFiles(directory="Backend/static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

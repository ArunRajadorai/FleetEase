from fastapi import APIRouter, HTTPException, Depends
from ..services.chatservice import ChatService

sendbird_router = APIRouter()
chat_service = ChatService()


@sendbird_router.post("/create-channel")
def create_channel(name: str, user_ids: list):
    try:
        channel = chat_service.create_channel(name, user_ids)
        return {"success": True, "channel": channel}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@sendbird_router.post("/send-message")
def send_message(channel_url: str, message: str):
    try:
        response = chat_service.send_message(channel_url, message)
        return {"success": True, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@sendbird_router.get("/list-channels")
def list_channels():
    try:
        channels = chat_service.list_channels()
        return {"success": True, "channels": channels}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

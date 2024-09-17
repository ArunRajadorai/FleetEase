import json
from typing import List, Dict

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import null
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.websockets import WebSocket, WebSocketDisconnect

from ..database.config import get_db
from ..models.chat import Chat, Message
from ..schemas.filterschema import EnquiryCreate
from ..services import chatservice
from ..utils.responseHandler import ApiResponse

chat_router = APIRouter()

# Dictionary to map client IDs to WebSocket connections
client_connections: Dict[int, WebSocket] = {}


@chat_router.websocket("/chat-api")
async def chat_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    # Accept the WebSocket connection
    await websocket.accept()
    global_user_id = None

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            target_user_id = message_data['targetUserId']
            user_id = message_data['from']
            global_user_id = user_id
            client_connections[user_id] = websocket

            # Find or create the chat between the buyer and seller
            chat = chatservice.get_chat(db, buyer_id=user_id, seller_id=target_user_id)
            if not chat:
                chat = chatservice.create_chat(db, buyer_id=user_id, seller_id=target_user_id,
                                               message=message_data['message'])

            # Save the message to the database
            chatservice.create_message(db, chat_id=chat.id, sender_id=user_id, receiver_id=target_user_id,
                                       message=message_data['message'])

            # Send the message to the target user if connected
            target_websocket = client_connections.get(target_user_id)
            if target_websocket:
                await target_websocket.send_text(data)
            else:
                print(f"Target user {target_user_id} is not connected.")

    except WebSocketDisconnect:
        # Remove the client from the dictionary on disconnect
        client_connections.pop(global_user_id, None)
        print(f"Client {global_user_id} disconnected.")
    except Exception as e:
        print(f"WebSocket error: {e}")


@chat_router.get("/chats/{buyer_id}")
def get_chats_for_user(buyer_id: int, db: Session = Depends(get_db)):
    chats = chatservice.get_chats_for_user(db, user_id=buyer_id)
    return chats


@chat_router.get("/chats/{chat_id}/messages")
def get_messages_for_chat(chat_id: int, db: Session = Depends(get_db)):
    messages = chatservice.get_messages_for_chat(db, chat_id=chat_id)
    return messages


@chat_router.post("/enquiry")
def create_enquiry(enquiry: EnquiryCreate, db: Session = Depends(get_db)):
    try:
        new_enquiry = chatservice.create_enquiry(db, enquiry)
        if new_enquiry:
            return ApiResponse(message="Enquiry submitted successfully", success=True)
        else:
            return ApiResponse(message="Not Submitted, Please Try again", success=False)
    except Exception as e:
        return ApiResponse(data=[], message=str(e), success=False)
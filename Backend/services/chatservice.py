from sqlalchemy import or_
from sqlalchemy.orm import Session
from ..models.chat import Chat, Message, Enquiry
from datetime import datetime

from ..schemas.filterschema import EnquiryCreate


def get_chat(db: Session, buyer_id: int, seller_id: int):
    return db.query(Chat).filter(
        or_(
            (Chat.buyer_id == buyer_id and Chat.seller_id == seller_id),
            (Chat.buyer_id == seller_id and Chat.seller_id == buyer_id)
        )
    ).first()


def create_chat(db: Session, buyer_id: int, seller_id: int, message: str):
    db_chat = Chat(buyer_id=buyer_id, seller_id=seller_id, last_message=message)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def create_message(db: Session, chat_id: int, sender_id: int, receiver_id: int, message: str):
    db_message = Message(chat_id=chat_id, sender_id=sender_id, receiver_id=receiver_id, message=message)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_chats_for_user(db: Session, user_id: int):
    return db.query(Chat).filter(
        (Chat.buyer_id == user_id) | (Chat.seller_id == user_id)).all()


def get_messages_for_chat(db: Session, chat_id: int):
    return db.query(Message).filter(Message.chat_id == chat_id).all()


def create_enquiry(db: Session, enquiry: EnquiryCreate):
    new_enquiry = Enquiry(
        username=enquiry.username,
        email=enquiry.email,
        message=enquiry.message,
        seller_id=enquiry.sellerId,
        buyer_id=enquiry.buyerId,
        vehicle_name=enquiry.vehicle_name,
    )
    db.add(new_enquiry)
    db.commit()
    db.refresh(new_enquiry)
    return new_enquiry

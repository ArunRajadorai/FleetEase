from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, index=True)
    seller_id = Column(Integer, index=True)
    last_message = Column(Text)
    last_message_time = Column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    message = Column(Text)
    sent_time = Column(DateTime, default=datetime.utcnow)


class Enquiry(Base):
    __tablename__ = 'enquiries'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    seller_id = Column(Integer, nullable=False)
    buyer_id = Column(Integer, nullable=False)
    vehicle_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
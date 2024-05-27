from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base  # Absolute import

class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(String, index=True, unique=True)

    # Define the relationship with the Message model
    messages = relationship("Message", back_populates="thread")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    status = Column(String, index=True)
    priority = Column(String, index=True)
    assignee = Column(String, index=True, nullable=True)
    thread_id = Column(Integer, ForeignKey('threads.id'))

    # Define the relationship with the Message model
    messages = relationship("Message", back_populates="ticket")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    thread_id = Column(Integer, ForeignKey('threads.id'))
    ticket_id = Column(Integer, ForeignKey('tickets.id'))

    # Define the relationship with the Ticket model
    ticket = relationship("Ticket", back_populates="messages")
    
    # Define the relationship with the Thread model
    thread = relationship("Thread", back_populates="messages")

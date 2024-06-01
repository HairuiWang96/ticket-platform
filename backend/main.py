from fastapi import FastAPI, HTTPException, Depends, Request, Query
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.models import Ticket, Message
from backend.database import engine, SessionLocal
from backend.nylas_integration import nylas
import backend.schemas as schemas
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from backend.nylas_client import nylas
import os


app = FastAPI()

Ticket.metadata.create_all(bind=engine)

class EmailResponse(BaseModel):
    ticket_id: int
    content: str

# Set all CORS enabled origins
origins = [
    "http://localhost:5173",  # Add the frontend origin here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables
Ticket.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

# Route to fetch messages using Nylas SDK
@app.get("/messages/")
async def get_messages():
    try:
        messages = nylas.messages.all()
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to list all new tickets with filtering
@app.get("/tickets/", response_model=List[schemas.Ticket])
async def list_tickets(done: bool = Query(False), db: Session = Depends(get_db)):
    try:
        if done:
            # Filter out done tickets
            tickets = db.query(Ticket).filter(Ticket.status != "Closed").all()
        else:
            # Retrieve all tickets
            tickets = db.query(Ticket).all()
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to get a single ticket by ID
@app.get("/tickets/{ticket_id}/", response_model=schemas.Ticket)
async def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

# Route to update a ticket
@app.put("/tickets/{ticket_id}/", response_model=schemas.Ticket)
async def update_ticket(ticket_id: int, ticket: schemas.TicketUpdate, db: Session = Depends(get_db)):
    logger.info(f"Received update for ticket ID {ticket_id} with data: {ticket}")
    try:
        logging.info(f"Received request to update ticket with ID {ticket_id}")
        logging.info(f"Request data: {ticket.dict()}")

        ticket_found = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket_found:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        # Log information about the ticket being updated
        logging.info(f"Updating ticket with ID: {ticket_id}. New details: {ticket}")

        # Update ticket details
        update_data = ticket.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(ticket_found, key, value)

        return ticket_found
    except Exception as e:
        logging.error(f"Error updating ticket with ID {ticket_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Route to list messages for a given ticket
@app.get("/tickets/{ticket_id}/messages/", response_model=List[schemas.Message])
async def list_messages_for_ticket(ticket_id: int, db: Session = Depends(get_db)):
    try:
        ticket_found = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket_found:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        # Use Nylas SDK to fetch messages for the ticket
        messages = nylas.messages.where(thread_id=ticket_found.thread_id)
        
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to connect email
@app.post("/connect_email/")
async def connect_email(user_id: int, email: str, password: str):
    try:
        nylas.accounts.first(login=email, password=password).save()
        # Store access token in database for future use
        return {"message": "Email connected successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tickets/{ticket_id}/respond")
def respond_to_email(ticket_id: int, response: schemas.EmailResponse, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    thread_id = ticket.thread_id
    try:
        body = {
            "subject": "Re: Your Subject",
            "body": response.content,
            "reply_to": [{"name": "Name", "email": os.environ.get("EMAIL")}],  # Replace with actual reply-to
            "to": [{"name": "Recipient Name", "email": "recipient@example.com"}],  # Replace with actual recipient
            "thread_id": thread_id
        }

        message = nylas.messages.send(request_body=body).data

        # Optionally log the response in your messages table
        new_message = Message(ticket_id=ticket_id, content=response.content)
        db.add(new_message)
        db.commit()
        return {"status": "sent", "message": message}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session
from backend.models import Ticket, Message
from backend.database import engine, SessionLocal
from backend.nylas_integration import nylas
import backend.schemas as schemas

app = FastAPI()

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

# Route to fetch messages using Nylas SDK
@app.get("/messages/")
async def get_messages():
    try:
        messages = nylas.messages.all()
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to list all new tickets
@app.get("/tickets/", response_model=List[schemas.Ticket])
async def list_tickets(db: Session = Depends(get_db)):
    try:
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
    try:
        ticket_found = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket_found:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Update ticket details
        ticket_found.status = ticket.status
        ticket_found.assignee = ticket.assignee
        ticket_found.priority = ticket.priority
        db.commit()
        db.refresh(ticket_found)

        return ticket_found
    except Exception as e:
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

if __name__ == "__main__":
    from temporal.workerfactory import WorkerFactory
    from temporal.workerfactory import WorkerFactoryOptions
    from temporal.activity_method import ActivityOptions

    # Create a worker factory
    factory = WorkerFactory("platform", WorkerFactoryOptions())

    # Register the activity function
    factory.register_activity(run_email_collection_workflow, "run_email_collection_workflow", ActivityOptions())

    # Start the Temporal worker to execute activities
    factory.start()

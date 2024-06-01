from temporalio import workflow
from backend.models import Ticket, Message
from backend.database import SessionLocal
import os
from backend.nylas_client import nylas

@workflow.defn
class EmailFetchWorkflow:
    @workflow.run
    async def run(self):
        while True:
            # Fetch new emails using Nylas API
            messages = nylas.messages.where({'in': 'inbox', 'limit': 10}).all()  # Example limit
            for message in messages:
                thread_id = message['thread_id']
                # Add logic to create/update tickets in the database
                db = SessionLocal()
                ticket = db.query(Ticket).filter(Ticket.thread_id == thread_id).first()
                if ticket:
                    # Update existing ticket
                    new_message = Message(ticket_id=ticket.id, content=message['body'])
                    db.add(new_message)
                else:
                    # Create a new ticket
                    new_ticket = Ticket(
                        status="new",
                        assignee="unassigned",
                        priority="normal",
                        thread_id=thread_id
                    )
                    db.add(new_ticket)
                    db.commit()
                    new_message = Message(ticket_id=new_ticket.id, content=message['body'])
                    db.add(new_message)
                db.commit()
            await workflow.sleep(3600)  # Wait for an hour before fetching again

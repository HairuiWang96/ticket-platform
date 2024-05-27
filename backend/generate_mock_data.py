import sys
import os
import random
from sqlalchemy.orm import Session

# Adjust the module path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Adjust PYTHONPATH to include the backend directory
backend_dir = os.path.join(current_dir, 'backend')
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from database import engine
from models import Thread, Ticket, Message

def create_mock_data():
    # Define some sample data
    subjects = ["Issue with login", "Payment not processed", "Bug in the app", "Feature request", "General inquiry"]
    statuses = ["Open", "In Progress", "Closed"]
    priorities = ["Low", "Medium", "High"]
    assignees = ["john.doe@example.com", "jane.doe@example.com", "support@example.com"]

    # Start a new database session
    with Session(engine) as session:
        for _ in range(10):  # Create 10 threads
            thread = Thread(thread_id=f"thread-{random.randint(1000, 9999)}")
            session.add(thread)
            session.commit()

            # Create a ticket linked to this thread
            ticket = Ticket(
                subject=random.choice(subjects),
                status=random.choice(statuses),
                priority=random.choice(priorities),
                assignee=random.choice(assignees),
                thread_id=thread.id
            )
            session.add(ticket)
            session.commit()

            # Create some messages linked to this thread and ticket
            for _ in range(random.randint(1, 5)):  # Create between 1 to 5 messages per thread
                message = Message(
                    content="This is a mock message for testing.",
                    thread_id=thread.id,
                    ticket_id=ticket.id
                )
                session.add(message)

        session.commit()

if __name__ == "__main__":
    create_mock_data()

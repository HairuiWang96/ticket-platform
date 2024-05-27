import sys
import os
from sqlalchemy.orm import Session
from database import engine
from models import Thread, Ticket, Message

# Adjust the module path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Adjust PYTHONPATH to include the backend directory
backend_dir = os.path.join(current_dir, 'backend')
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

def check_data():
    with Session(engine) as session:
        threads = session.query(Thread).all()
        tickets = session.query(Ticket).all()
        messages = session.query(Message).all()

        print(f"Threads: {threads}")
        print(f"Tickets: {tickets}")
        print(f"Messages: {messages}")

if __name__ == "__main__":
    check_data()

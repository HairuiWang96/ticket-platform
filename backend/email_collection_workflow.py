# from temporal import workflow_method
# from backend.nylas_integration import nylas
# from backend.models import Message
# from backend.database import SessionLocal

# @workflow_method
# class EmailCollectionWorkflow:
#     @classmethod
#     async def execute(cls):
#         # Fetch new messages or threads using Nylas SDK
#         new_messages = nylas.messages.where(unread=True)
        
#         # Ingest new messages into the system
#         with SessionLocal() as db:
#             for message_data in new_messages:
#                 # Check if message already exists in the database to ensure idempotency
#                 existing_message = db.query(Message).filter(Message.id == message_data.id).first()
#                 if not existing_message:
#                     # Create a new message object and add it to the database
#                     new_message = Message(id=message_data.id, content=message_data.content, thread_id=message_data.thread_id)
#                     db.add(new_message)
        
#         return "Email collection completed successfully"

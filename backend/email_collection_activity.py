# from temporalio import activity_method
# from temporalio import WorkflowClient
# from backend.email_collection_workflow import EmailCollectionWorkflow

# @activity_method
# def run_email_collection_workflow():
#     # Create a WorkflowClient to interact with Temporal
#     client = WorkflowClient.new_client()

#     # Create a workflow stub for the EmailCollectionWorkflow
#     workflow_stub = client.new_workflow_stub(EmailCollectionWorkflow)

#     # Execute the workflow
#     return workflow_stub.execute()

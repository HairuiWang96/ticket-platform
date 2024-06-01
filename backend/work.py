from temporalio.client import Client
from temporalio.worker import Worker
from workflows import EmailFetchWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="email-fetch-task-queue",
        workflows=[EmailFetchWorkflow],
    )
    await worker.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

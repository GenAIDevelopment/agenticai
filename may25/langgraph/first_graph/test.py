import asyncio

async def task1():
    print("Task 1 started")
    await asyncio.sleep(6)
    print("Task 1 finished")

async def task2():
    print("Task 2 started")
    await asyncio.sleep(3)
    print("Task 2 finished")

async def task3():
    print("Task 3 started")
    await asyncio.sleep(1)
    print("Task 3 finished")

async def main():
    await asyncio.gather(task1(), task2(), task3())  # Runs both tasks together

asyncio.run(main())
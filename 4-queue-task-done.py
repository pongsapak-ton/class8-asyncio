from random import random
import asyncio
import time

# coroutine to generate work 
async def producer(queue): 
    print(f'{time.ctime()} Producer: Running') 
    # generate work 
    for i in range(10): 
        # generate a value 
        value = random() 
        # block to simulate work 
        await asyncio.sleep(value) 
        # add to the queue 
        await queue.put(value) 
        #print(f'{time.ctime()} Producer: put {value}')
    # send an all done signal 
    await queue.put(None) 
    print(f'{time.ctime()} Producer: Done')


    # coonsumer work
async def consumer(queue):
    print(f'{time.ctime()} Consumer: Running') 
    # consume work 
    while True: 
        # get a unit of work  
        item = await queue.get()
         #report 
        print(f'{time.ctime()} >got {item}') 
        # block while processing 
        if item:
            await asyncio.sleep(item)
    # mask the task as done 
    queue.task_done()

# entry point coroutine
async def main():
    # create the shared queue 
    queue = asyncio.Queue()
    # start the consumer
    _ = asyncio.create_task(consumer(queue))
    # start the producer and wait for it to finish
    await asyncio.create_task(producer(queue)) 
    # wait for all items to be proocessed
    await queue.join()

# start the asyncio program 
asyncio.run(main())

# we will create a producer coroutine that will generate ten random numbers 
# and put them on the queue. We will also create a consumer coroutine 
# that will get numbers from the queue and report their values.

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

async def consumer(queue):
    print(f'{time.ctime()} Consumer: Running') # consume work 
    while True: 
        # get a unit of work 
        item = await queue.get() 
        # check for stop signal 
        if item is None:
            break
         #report 
        print(f'{time.ctime()} >got {item}') 
    # all done 
    print(f'{time.ctime()} Consumer: Done') 

# entry point coroutine
async def main():
    # create the shared queue 
    queue = asyncio.Queue() 
    # run the producer and consumers 
    await asyncio.gather(producer(queue), consumer(queue))

# start the asyncio program 
asyncio.run(main())
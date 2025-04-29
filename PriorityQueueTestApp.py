from structure.queue.PriorityInsertQueue import PriorityInsertQueue


queue = PriorityInsertQueue()

queue.enqueue(1, 1)
queue.enqueue(2, 2)
queue.enqueue(3, 3)
queue.enqueue(4, 4)
queue.enqueue(100, 100)
queue.enqueue(50, 50)
queue.enqueue(3, 12)
queue.enqueue(3, 13)
queue.enqueue(3, 14)
queue.enqueue(3, 15)

print(queue)

while not queue.is_empty:
    print(queue.dequeue())

# python3 PriorityQueueTestApp.py

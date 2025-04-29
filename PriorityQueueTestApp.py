from structure.queue.PriorityInsertQueue import PriorityInsertQueue
from structure.PriorityInsertStack import PriorityInsertStack


queue = PriorityInsertQueue()
stack = PriorityInsertStack()

stack.put(1, 1)
stack.put(2, 2)
stack.put(3, 3)
stack.put(4, 4)
stack.put(100, 100)
stack.put(50, 50)
stack.put(3, 12)
stack.put(3, 13)
stack.put(3, 14)
stack.put(3, 15)

print(stack)

while not stack.is_empty:
    print(stack.pop())

# python3 PriorityQueueTestApp.py

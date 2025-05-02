from structure.queue.PriorityInsertQueue import PriorityInsertQueue
from structure.PriorityInsertStack import PriorityInsertStack
from structure.matrix.ListMatrix import ListMatrix
from utility_algorithms.StableMarriage import StableMarriage
from utility_algorithms.AssignmentProblem import AssignmentProblem


# queue = PriorityInsertQueue()
# stack = PriorityInsertStack()

# stack.put(1, 1)
# stack.put(2, 2)
# stack.put(3, 3)
# stack.put(4, 4)
# stack.put(100, 100)
# stack.put(50, 50)
# stack.put(3, 12)
# stack.put(3, 13)
# stack.put(3, 14)
# stack.put(3, 15)

# stack.replace_item(100, 3, 100)
# stack.replace_item(4, 50, 4)

# print(stack)

# while not stack.is_empty:
#     print(stack.pop())

# mx = ListMatrix(2, 2)

# Trouble with:
# mx._setAll([
#     [2, 5],
#     [3, 6]
# ])

mx = ListMatrix(3, 3)

# mx._setAll([
#     [2, 6, 9],
#     [6, 103, 100],
#     [200, 1, 2]
# ])
# mx._setAll([
#     [1, 2, 9],
#     [4, 3, 100],
#     [2, 1, 5]
# ])
# Trouble with:
mx._setAll([
    [3, 3, 4],
    [4, 4, 5],
    [4, 4, 3]
])

# i.e. <row index>, <col index>, <value chosen>
# result_list = StableMarriage.GaleShapley(mx, comparizon_function=lambda a, b: b - a)
# result_list = AssignmentProblem.HungarianAlgorithmV0(mx)
result_list = AssignmentProblem.HungarianAlgorithm(mx)

print(result_list)

sum = 0
for i in range(0, len(result_list), 1):
    sum += result_list[i][2]

print(result_list, '->', sum)


# python3 PriorityQueueTestApp.py

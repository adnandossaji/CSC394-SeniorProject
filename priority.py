import heapq
from node import *
from collections import deque

class Priority:
    def __init__(self, f): # f is the function that orders queue
        self.queue = []
        self.count = 0     # hash: needed to differentiate nodes that have the same cost 
        self.lookup = {}   # use dictionary to see if value is in queue
        self.f = f         # function for prioritizing queue 
        self.space = 0     # value for determing size of queue 

    #push node onto heap (hashed using function f and count in case function values are the same for two nodes)
    def push(self, node):
        c = self.f(node)
        heapq.heappush(self.queue, (c, self.count, node)) 
        self.lookup[node] = [c, self.count, node]
        self.count += 1
        self.space += 1

    # pop off node
    def pop(self): 
        self.space -= 1
        return heapq.heappop(self.queue)[2]

    def get(self, node):
        print(self)
        index = self.queue.index(node)
        return queue[index]

    def remove(self, node):
        index = self.queue.index 
        queue.remove(index)
        heapq.heapify(queue)
        
# overrided function for making  priorityqueue iterable and comparable, use contains for lookup in dict and len for getting length of queue
    def __iter__(self):
        return iter(self.queue)

# if new cost is the same current cost, prioritize the node added first, otherwise prioritize based on f(cost)
    def __lt__(self, new):
        return (self.f(self), self.count) < (new.f(new), new.count)
        
    def __contains__(self, node):
        return node in self.lookup

    def __len__(self):
        return self.space

class fdeque:
    def __init__(self):
        self.queue = deque()
        self.lookup = {}
        self.space = 0 # size of queue for calculating space

    # ovverride deque functions while also using dictionary to keep track of visited states and space to keep track of size
    def appendleft(self, node): 
        self.queue.appendleft(node)
        self.lookup[node] = node
        self.space += 1

    def append(self, node):
        self.queue.append(node)
        self.lookup[node] = node
        self.space += 1

    def pop(self):
        deleted = self.queue.pop()
        self.lookup.pop(deleted)
        self.space -= 1
        return deleted

    def __contains__(self, node):
        return node in self.lookup 

    def __len__(self):
        return self.space

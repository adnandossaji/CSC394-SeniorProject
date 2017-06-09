import heapq
from app.node import *
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
        cost = self.f(node)
        heapq.heappush(self.queue, (cost, self.count, node)) 
        self.lookup[tuple(node.taken_overall)] = (cost, self.count, node)
        self.count += 1
        self.space += 1

    # pop off node
    def pop(self): 
        self.space -= 1
        popped = heapq.heappop(self.queue)
        del self.lookup[tuple(popped[2].taken_overall)]
        return popped[2]

    def remove(self, entry):
        #print(node.taken_overall)
        #index = self.queue.index(tuple(node.taken_overall))
        self.queue.remove(entry)
        heapq.heapify(self.queue)

        del self.lookup[tuple(entry[2].taken_overall)] 

    def replace(self, node):
        return
        try:
            (cost, c, compare) = self.lookup[tuple(node.taken_overall)]
            if (cost <= self.f(node)):
                # if what's on queue is already lowest, do nothing; return
                return 
            else:
                # if not, remove it from queue and add lower cost onto queue
                self.remove((cost, c, compare))
                self.push(node)

        except KeyError:
            print("WARNING: tried to replace node that was not already on priority queue")
            print("="*10)
            print("="*10)
            print("="*10)
            pass
        
    def __iter__(self):
        return iter(self.queue)

    # if new cost is the same current cost, prioritize the node added first, otherwise prioritize based on f(cost)
    def __lt__(self, new):
        return (self.f(self)) < (new.f(new))
        
    def __contains__(self, node):
        return tuple(node.taken_overall) in self.lookup

    def __len__(self):
        return self.space

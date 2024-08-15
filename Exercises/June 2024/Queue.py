from collections import deque
import time
import threading

class Queue:
    
    def __init__(self):
        self.buffer = deque()
    
    def enqueue(self, val):
        self.buffer.appendleft(val)
        
    def dequeue(self):
        return self.buffer.pop()
    
    def is_empty(self):
        return len(self.buffer)==0
    
    def size(self):
        return len(self.buffer)
    
food_queue = Queue()

def place_order(order):
    food_queue.enqueue(order)
    time.sleep(0.5)

def serve_order():
    print(food_queue.dequeue())

binary_queue = Queue()

for i in range(1, 11):
    binary_queue.enqueue(bin(i).split('b')[1])
    print(binary_queue.dequeue())
    
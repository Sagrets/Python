def fib(n):
        if n == 1 or n == 0:
            return n
    
        return fib(n - 1) + fib(n - 2)

class fib_object():
    def __init__(self):
        self.current = 0
        self.nxt = 1

    def __iter__(self):
         return self
    
    def __next__(self):
         self.nxt = self.nxt + self.current
         self.current = self.nxt - self.current

         return self.nxt
fib_test = fib_object()
fib_itr = iter(fib_test)

print(fib_test.current)
print(fib_test.nxt)
print(next(fib_itr))
print(next(fib_itr))
print(next(fib_itr))
print(next(fib_itr))

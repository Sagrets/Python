# Define a function named list_sum that takes a list of numbers as input
def list_sum(num_List):
    # Check if the length of the input list is 1
    if len(num_List) == 1:
        # If the list has only one element, return that element
        return num_List[0]
    else:
        # If the list has more than one element, return the sum of the first element
        # and the result of recursively calling the list_sum function on the rest of the list
        return num_List[0] + list_sum(num_List[1:])

# Print the result of calling the list_sum function with the input [2, 4, 5, 6, 7]
#print(list_sum([2, 4, 5, 6, 7]))

def nest_list_sum(array, total=0):
    for item in array:
        if isinstance(item, list):
            total += nest_list_sum(item)
        else:
            total += item
    return total

"""
elements = [1, 2, [3, 4], [5, 6]]

print(nest_list_sum(elements))
"""

def factorial(n):
    if n == 1:
        return n
        
    return n * factorial(n - 1)
    
#print(factorial(3))

def fib(n):
    if n == 1 or n == 0:
        return n
    
    return fib(n - 1) + fib(n - 2)

print(fib(9))

def int_sum(n):
    if len(str(n)) == 1:
        return n
    
    return int(str(n)[0]) + int_sum(int(str(n)[1:]))

#print(int_sum(45))

def sum_series(n, x=0):
    x += 2
    while n - x > 0:
        return sum_series(n - x) + sum_series(n - (x + 2))
    
    return n

#print(sum_series(6))

def geo_sum(b, r, n, sequence=[]):
    if n == 0:
        return  b
    else:
        sequence.append(b)
        geo_sum(b * r, r, n - 1)
        
        return sum(sequence)

#print(geo_sum(2, 3, 10))

def power(b, e):
    if e == 1:
        return b
    
    return b * power(b, e - 1)

#print(power(3,4))


    

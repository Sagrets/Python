import random
import math

num_list = []

for i in range(1, 11):
    num_list.append(random.randint(1, 9))

answer = num_list[random.randint(0, 9)]
num_list.sort()

while num_list:
    mid_val = num_list[math.floor(len(num_list) / 2)]
    
    print(answer)
    print(num_list)
    print(mid_val)

    if answer == mid_val:
        print(answer)
        break
    elif answer > mid_val:
        num_list = num_list[math.floor(len(num_list) / 2):]
        mid_val = num_list[math.floor(len(num_list) / 2)]
    else:
        num_list = num_list[0: math.floor(len(num_list) / 2)]
        mid_val = num_list[math.floor(len(num_list) / 2)]
import math

def insertion_sort(elements):
    for i in range(1, len(elements)):
        anchor = elements[i]
        j = i - 1
        while j>=0 and anchor < elements[j]:
            elements[j+1] = elements[j]
            j = j - 1
        elements[j+1] = anchor

list = [2, 1, 5, 7, 2, 0, 5]

def get_median(list):
    if len(list) == 1:
        return list[0]

    if len(list) % 2 == 0:
        median = (list[math.floor((len(list) / 2) - 1)] + list[math.floor(len(list) / 2)]) / 2
        if median % 2 == 0:
            return(math.floor(median))
        else: 
            return median
    else:
        return list[math.floor((len(list) - 1) / 2)]

for n in list:
    current = list[:list.index(n) + 1]
    insertion_sort(current)

    print(get_median(current))
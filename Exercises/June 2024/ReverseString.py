from collections import deque

input_string = input("Please enter a phrase or sentence: ")
string_arr = deque()
output_string = ''

for char in input_string:
    string_arr.append(char)

while string_arr:
    output_string += string_arr.pop()

print(output_string)
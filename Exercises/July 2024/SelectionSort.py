def find_dict_index(arr, target):
    for index, dict in enumerate(arr):
        if dict == target:
            return index
    return None

def selection_sort(arr, key1, key2):
    n = 0
    while n < len(arr):
        tmp_arr = arr[n]
        tmp_k1 = arr[n][key1]
        tmp_k2 = arr[n][key2]
        reassign_count = 0

        for i in range(n, len(arr)):
            if arr[i][key1] == tmp_k1:
                if arr[i][key2] < tmp_k2:
                    reassign_count += 1
                    tmp_k1 = arr[i][key1]
                    tmp_k2 = arr[i][key2]
                    tmp_arr = arr[i]

            if arr[i][key1] < tmp_k1:
                reassign_count += 1
                tmp_k1 = arr[i][key1]
                tmp_k2 = arr[i][key2]
                tmp_arr = arr[i]

        if reassign_count == 0:
            n += 1
            continue
        
        if tmp_k1 < arr[n][key1]:
            arr[arr.index(tmp_arr)] = arr[n]
            arr[n] = tmp_arr
            
        if tmp_k2 < arr[n][key2]:
            arr[arr.index(tmp_arr)] = arr[n]
            arr[n] = tmp_arr
            
        n += 1
        
elements = [
    {'First Name': 'Raj', 'Last Name': 'Nayyar'},
    {'First Name': 'Suraj', 'Last Name': 'Sharma'},
    {'First Name': 'Karan', 'Last Name': 'Kumar'},
    {'First Name': 'Jade', 'Last Name': 'Canary'},
    {'First Name': 'Raj', 'Last Name': 'Thakur'},
    {'First Name': 'Raj', 'Last Name': 'Sharma'},
    {'First Name': 'Kiran', 'Last Name': 'Kamla'},
    {'First Name': 'Armaan', 'Last Name': 'Kumar'},
    {'First Name': 'Jaya', 'Last Name': 'Sharma'},
    {'First Name': 'Ingrid', 'Last Name': 'Galore'},
    {'First Name': 'Jaya', 'Last Name': 'Seth'},
    {'First Name': 'Armaan', 'Last Name': 'Dadra'},
    {'First Name': 'Ingrid', 'Last Name': 'Maverick'},
    {'First Name': 'Aahana', 'Last Name': 'Arora'}
]
selection_sort(elements, 'First Name', 'Last Name')
for i in elements:
    print(i)
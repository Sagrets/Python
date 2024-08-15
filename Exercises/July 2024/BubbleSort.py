def bubble_sort(elements, key='transaction_amount'):
    size = len(elements)

    for i in range(size - 1):
        if elements[i][key] > elements[i + 1][key]:
            tmp = elements[i][key]
            elements[i][key] = elements[i + 1][key]
            elements[i + 1][key] = tmp
            bubble_sort(elements, key)

    return elements
    
if __name__ == '__main__':
    elements = [
        { 'name': 'mona',   'transaction_amount': 1000, 'device': 'iphone-10'},
        { 'name': 'dhaval', 'transaction_amount': 400,  'device': 'google pixel'},
        { 'name': 'kathy',  'transaction_amount': 200,  'device': 'vivo'},
        { 'name': 'aamir',  'transaction_amount': 800,  'device': 'iphone-8'},
    ]


    bubble_sort(elements, 'device')
    
    for i in range(len(elements)):
        print(elements[i])
  
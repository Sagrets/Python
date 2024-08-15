def square():
    n = 1
    while True:
        yield n * n
        n += 1

for i in square():
    if i > 100:
        break

    print(i)
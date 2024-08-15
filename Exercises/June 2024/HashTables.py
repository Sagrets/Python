class HashTable:
    def __init__(self):
        self.max = 100
        self.arr = [[] for i in range(self.max)]

    def get_hash(self, key):
        h = 0
        for char in key:
            h += ord(char)
            return h % self.max
    
    def __setitem__(self, key, val):
        h = self.get_hash(key)

        found = False        
        for index, element in enumerate(self.arr[h]):
            if element[0] == key:
                self.arr[h][index] = (key, val)
                found = True
                break
        if not found:
            self.arr.append((key, val))


    def __getitem__(self, key):
        h = self.get_hash(key)
        
        for index, element in enumerate(self.arr[h]):
            if element[0] == key:
                return element[1]
    
    def __delitem__(self, key):
        h = self.get_hash(key)

        for index, element in enumerate(self.arr[h]):
            if element[0] == key:
                del self.arr[h][index]
                return

t = HashTable()
t['March 6'] = 150
print(t.arr)
del t['March 6']
print(t.arr)

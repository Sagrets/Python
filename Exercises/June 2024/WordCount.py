with open('poems.txt') as file:
    poems_contents = file.read()

whitespace_removed = poems_contents.split()

word_dict = {}

for word in whitespace_removed:
    if word in word_dict:
        word_dict[word] += 1
    else:
        word_dict[word] = 1

print(word_dict)
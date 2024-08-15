import datasets

def gen():
    yield {'Dragon': 'Caraxes', 'color': 'red'}
    yield {'Dragon': 'Vhagar', 'color': 'grey'}

ds = datasets.Dataset.from_generator(gen)

print(ds[0])
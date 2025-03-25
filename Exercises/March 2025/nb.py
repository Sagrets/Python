import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB

wine = load_wine()
wine_df = pd.DataFrame(wine.data, columns=wine.feature_names)

x_train, x_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.2)

model = GaussianNB()
model.fit(x_train, y_train)

model2 = MultinomialNB()
model2.fit(x_train, y_train)

print(model.score(x_test, y_test))
print(model2.score(x_test, y_test))
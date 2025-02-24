from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

flowers = load_iris()

x_train, x_test, y_train, y_test = train_test_split(flowers.data, flowers.target, test_size=0.2)

model = LogisticRegression()

model.fit(x_train, y_train)

print(model.predict(x_test))
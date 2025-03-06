import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

iris = load_iris()

df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
df['flower_name'] = df.target.apply(lambda x: iris.target_names[x])

inputs = df.drop(['target', 'flower_name'], axis=1)
target = df.target

x_train, x_test, y_train, y_test = train_test_split(inputs, target, test_size=0.2)


model=SVC(C=1.2, gamma='auto')

model.fit(x_train, y_train)

print(model.score(x_train, y_train))
print(model.score(x_test, y_test))
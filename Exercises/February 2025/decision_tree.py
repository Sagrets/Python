import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import tree

df = pd.read_csv('titanic.csv')

inputs = df.drop(['PassengerId', 'Survived', 'Name', 'SibSp', 'Parch', 'Ticket', 'Cabin', 'Embarked'], axis=1)

le_Sex = LabelEncoder()

inputs['Sex_n'] = le_Sex.fit_transform(inputs['Sex'])

inputs_n = inputs.drop('Sex', axis=1)
target = df['Survived']
inputs_n_train, inputs_n_test, target_train, target_test = train_test_split(inputs_n, target, test_size=0.2)

model = tree.DecisionTreeClassifier()
model.fit(inputs_n_train, target_train)

print('Accuracy score: ' + str(model.score(inputs_n_test, target_test)))
print(model.predict(pd.DataFrame([[3, 0, 30, 54.43]], columns=inputs_n.columns)))
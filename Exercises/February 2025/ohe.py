import pandas as pd
from sklearn.linear_model import LinearRegression
model = LinearRegression()

pd.set_option('display.width', 8000)
pd.set_option('display.max_columns', None)

df = pd.read_csv('carprices.csv')

df = pd.concat([df, pd.get_dummies(df['Car Model']).astype(int)], axis=1)
df = df.fillna(0)
df = df.drop(['Car Model', 'Mercedez Benz C class'], axis=1)

model.fit(df.drop(['Sell Price($)'], axis=1), df['Sell Price($)'])

input1 = pd.DataFrame([[45000, 4, 0, 0]], columns=df.drop(['Sell Price($)'], axis=1).columns)
input2 = pd.DataFrame([[86000, 7, 0, 1]], columns=df.drop(['Sell Price($)'], axis=1 ).columns)

print(model.predict(input1))
print(model.predict(input2))
print(model.score(df.drop(['Sell Price($)'], axis=1), df['Sell Price($)']))
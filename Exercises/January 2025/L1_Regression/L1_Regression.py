import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

df = pd.read_csv('canada_per_capita_income.csv')

reg = linear_model.LinearRegression()
reg.fit(df[['year']].values, df[['per capita income (US$)']])

new_rows=[]

for i in range(0, 4):
    year=2017+i
    income = reg.predict([[year]])[0][0]
    new_rows.append({'year': year, 'per capita income (US$)': income})
    
new_rows = pd.DataFrame(new_rows)
df = pd.concat([df, new_rows], ignore_index=True)

plt.xlabel('Year')
plt.ylabel('Per Capita Income (US$)')
plt.scatter(df[['year']], df[['per capita income (US$)']], color='red', marker='+')
plt.plot(df[['year']], reg.predict(df[['year']]), color='blue')
plt.xticks(df['year'], rotation=45)
plt.show()
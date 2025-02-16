import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from word2number import w2n

df = pd.read_csv('hiring.csv')
df.loc[pd.isna(df['experience']), 'experience'] = 'six'
df['experience'] = df['experience'].apply(w2n.word_to_num)
df.loc[pd.isna(df['test_score(out of 10)']), 'test_score(out of 10)'] = 8.5

reg = linear_model.LinearRegression()
reg.fit(df[['experience', 'test_score(out of 10)', 'interview_score(out of 10)']], df['salary($)'])

two_yr_exp = reg.predict([[2, 9, 6]])
twelve_yr_exp = reg.predict([[12, 10, 10]])

print('2 yr experience, 9 test score, 6 interview score: ' + str(two_yr_exp))
print('12 yr experience, 10 test score, 10 interview score: ' + str(twelve_yr_exp))

import kagglehub
import glob
import os
import pandas as pd
from matplotlib import pyplot
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

data_path = kagglehub.dataset_download("giripujar/hr-analytics")

csv_path = glob.glob(os.path.join(data_path, "*.csv"))[0]

df = pd.read_csv(csv_path)

left_employees_by_salary = df[df['left'] == 1][['salary', 'left']]
salary_counts = left_employees_by_salary['salary'].value_counts().reset_index()

left_employees_by_dept = df[df['left'] == 1][['Department', 'left']]
dept_counts = left_employees_by_dept['Department'].value_counts().reset_index()

fig, (ax, ax2) = pyplot.subplots(ncols=2)

salary_categories = ['high', 'medium', 'low']
ax_counts = salary_counts['count'].values
bar_colors = ['tab:red', 'tab:green', 'tab:blue']

departments = dept_counts['Department'].values
ax2_counts = dept_counts['count'].values

"""
ax.bar(salary_categories, ax_counts, label=salary_categories, color=bar_colors)
ax2.bar(departments, ax2_counts, label=departments)

ax.set_ylabel('salary category counts')
ax.set_title('salary category counts for left employees')

ax2.set_ylabel('department counts')
ax2.set_title('left employee count by departments')
ax2.set_xticklabels(departments, rotation=45)

pyplot.show()
"""
x = pd.get_dummies(df[['Department', 'salary']], drop_first=True).astype(int)
satisfaction_levels = df['satisfaction_level']
x = pd.concat([satisfaction_levels, x], axis=1)
y = df['left']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

model = LogisticRegression()
model.fit(x_train, y_train)

print(model.predict(x_test))
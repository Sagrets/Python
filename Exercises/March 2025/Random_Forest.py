from sklearn.datasets import load_digits
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

digits = load_digits()

df = pd.DataFrame(digits.data, columns=digits.feature_names)
df['target'] = digits.target

x = df.drop(['target'], axis=1)
y = df.target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=25)

model.fit(x_train, y_train)

print(model.score(x_test, y_test))
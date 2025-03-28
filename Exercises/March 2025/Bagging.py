import pandas as pd
from scipy.stats import zscore
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('heart.csv')

z_scores = df.select_dtypes(include=['number']).apply(zscore)
df = df[(z_scores.abs() <= 3).all(axis=1)]

encoder = LabelEncoder()
for column in df.select_dtypes(include=['object']).columns:
    df[column] = encoder.fit_transform(df[column])

scaler = StandardScaler()

X = df.drop('HeartDisease', axis=1)
y = df['HeartDisease']
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

svm = SVC(kernel='rbf', random_state=42)
svm.fit(X_train, y_train)

print("Accuracy with SVM:", svm.score(X_test, y_test))

bagging_svm = BaggingClassifier(estimator=SVC(kernel='rbf', random_state=42), 
                                 n_estimators=11, random_state=42)
bagging_svm.fit(X_train, y_train)

print("Accuracy with Bagging (SVM):", bagging_svm.score(X_test, y_test))

decision_tree = DecisionTreeClassifier(random_state=42)
decision_tree.fit(X_train, y_train)

print("Accuracy with Decision Tree:", decision_tree.score(X_test, y_test))

bagging_tree = BaggingClassifier(estimator=DecisionTreeClassifier(random_state=42), 
                                 n_estimators=11, random_state=42)
bagging_tree.fit(X_train, y_train)

print("Accuracy with Bagging (Decision Tree):", bagging_tree.score(X_test, y_test))
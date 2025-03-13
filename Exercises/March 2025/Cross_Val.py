from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score

iris = load_iris()

log_reg = LogisticRegression(max_iter=200)
svc = SVC()
rf_clf = RandomForestClassifier()

log_reg_scores = cross_val_score(log_reg, iris.data, iris.target, cv=5)
svc_scores = cross_val_score(svc, iris.data, iris.target, cv=5)
rf_clf_scores = cross_val_score(rf_clf, iris.data, iris.target, cv=5)

print(f"Logistic Regression average score: {log_reg_scores.mean()}")
print(f"SVC average score: {svc_scores.mean()}")
print(f"Random Forest average score: {rf_clf_scores.mean()}")
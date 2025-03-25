from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits
from sklearn.model_selection import GridSearchCV
import pandas as pd

digits = load_digits()
x_train, x_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.2)

model_parameters = {
    "svm": {
        "model": svm.SVC(),
        "parameters": {
            "C": [0.1, 1, 10],
            "kernel": ["linear", "rbf", "poly"],
            "gamma": ["scale", "auto"]
        }
    },
    "random_forest": {
        "model": RandomForestClassifier(),
        "parameters": {
            "n_estimators": [10, 50, 100],
            "max_depth": [None, 10, 20],
            "min_samples_split": [2, 5, 10]
        }
    },
    "logistic_regression": {
        "model": LogisticRegression(),
        "parameters": {
            "C": [0.1, 1, 10],
            "solver": ["liblinear", "lbfgs"],
            "penalty": ["l2"]
        }
    },
    "gaussian_nb": {
        "model": GaussianNB(),
        "parameters": {
            "var_smoothing": [1e-9, 1e-8, 1e-7]
        }
    },
    "multinomial_nb": {
        "model": MultinomialNB(),
        "parameters": {
            "alpha": [0.1, 1, 10],
            "fit_prior": [True, False]
        }
    },
    "decision_tree": {
        "model": DecisionTreeClassifier(),
        "parameters": {
            "criterion": ["gini", "entropy"],
            "max_depth": [None, 10, 20],
            "min_samples_split": [2, 5, 10]
        }
    }
}
scores = []

for model_name, mp in model_parameters.items():
    grid = GridSearchCV(mp["model"], mp["parameters"], cv=5, return_train_score=False)
    grid.fit(x_train, y_train)
    scores.append({
        "model": model_name,
        "best_score": grid.best_score_,
        "best_params": grid.best_params_
    })

scores_df = pd.DataFrame(scores)
print(scores_df)

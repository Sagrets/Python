import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
import math

def gradient_descent(x,y):
    m_curr = b_curr = 0
    iterations = 1000000
    n = len(x)
    learning_rate = 0.0002
    prev_cost = float('inf')
    
    for i in range(iterations):
        y_predicted = m_curr * x + b_curr
        cost = mean_squared_error(y, y_predicted)
        
        if math.isclose(cost, prev_cost, rel_tol=1e-20):
            print(f"Convergance acheived \nm {m_curr}, b {b_curr}, cost {cost}, iteration {i}")
            break
        
        prev_cost = cost
        
        md = -(2/n)*sum(x*(y-y_predicted))
        bd = -(2/n)*sum(y-y_predicted)
        m_curr = m_curr - learning_rate * md
        b_curr = b_curr - learning_rate * bd
        
        print ("m {}, b {}, cost {} iteration {}".format(m_curr,b_curr,cost, i))
        
df = pd.read_csv('test_scores.csv')

x = df['math'].to_numpy()
y = df['cs'].to_numpy()

gradient_descent(x, y)
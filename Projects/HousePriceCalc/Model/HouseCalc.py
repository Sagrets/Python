import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Lasso
from sklearn.tree import DecisionTreeRegressor


df = pd.read_csv('./bengaluru_house_prices.csv')
df = df.drop(['area_type', 'society', 'balcony', 'availability'], axis=1)
df = df.dropna()

df['bhk'] = df['size'].apply(lambda x: int(x.split(' ')[0]))

def is_float(x):
    try:
        float(x)
    except ValueError:
        return False
    return True

def conver_sqft_to_num(x):
    tokens = x.split('-')
    if len(tokens) == 2:
        return (float(tokens[0]) + float(tokens[1])) / 2
    try:
        return float(x)
    except ValueError:
        return None
    
df['total_sqft'] = df['total_sqft'].apply(conver_sqft_to_num)
df = df[df.total_sqft.notnull()]
df['price_per_sqft'] = df['price'] * 100000 / df['total_sqft']

df.location = df.location.apply(lambda x: x.strip())
location_stats = df.location.value_counts(ascending=False)
df.location = df.location.apply(lambda x: 'other' if location_stats[x] <= 10 else x)

df = df[~(df.total_sqft/df.bhk < 300)]

def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for key, subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df = subdf[(subdf.price_per_sqft>(m-st)) & (subdf.price_per_sqft<=(m+st))]
        df_out = pd.concat([df_out,reduced_df],ignore_index=True)
    return df_out

df = remove_pps_outliers(df)

def plot_scatter_chart(df, location):
    bhk2 = df[(df.location == location) & (df.bhk == 2)]
    bhk3 = df[(df.location == location) & (df.bhk == 3)]

    plt.figure(figsize=(10, 7))
    plt.scatter(bhk2.total_sqft, bhk2.price, color='blue', label='2 BHK', s=50)
    plt.scatter(bhk3.total_sqft, bhk3.price, color='green', label='3 BHK', s=50)
    plt.xlabel("Total Square Feet Area")
    plt.ylabel("Price (in Lakhs)")
    plt.title(f"2 BHK vs 3 BHK Prices in {location}")
    plt.legend()
    plt.show()
    
#plot_scatter_chart(df, "Rajaji Nagar")
    
def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('bhk'):
            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }
            
        for bhk, bhk_df in location_df.groupby('bhk'):
            stats = bhk_stats.get(bhk-1)
            if stats and stats['count']>5:
                exclude_indices = np.append(exclude_indices, bhk_df[bhk_df.price_per_sqft<(stats['mean'])].index.values)
    return df.drop(exclude_indices,axis='index')

df = remove_bhk_outliers(df)

df = df[df.bhk + 2 > df.bath]

df = df.drop(['size', 'price_per_sqft'], axis='columns')

def apply_one_hot_encoding(df):
    dummies = pd.get_dummies(df['location'], prefix='location')
    df = pd.concat([df, dummies], axis=1)
    df = df.drop('location', axis=1)
    return df

df = apply_one_hot_encoding(df)
df = df.drop(['location_other'], axis=1)

y= df.price
x = df.drop(['price'], axis=1)

for col in x.columns:
    if col.startswith('location_'):
        x = x.rename(columns={col: col.replace('location_', '')})

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train, y_train)

def find_best_model_using_gridsearchcv(X,y):
    algos = {
        'linear_regression' : {
            'model': LinearRegression(),
            'params': {
                'fit_intercept': [True, False],
            }
        },
        'lasso': {
            'model': Lasso(),
            'params': {
                'alpha': [1,2],
                'selection': ['random', 'cyclic']
            }
        },
        'decision_tree': {
            'model': DecisionTreeRegressor(),
            'params': {
                'criterion' : ['mse','friedman_mse'],
                'splitter': ['best','random']
            }
        }
    }
    scores = []
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
    for algo_name, config in algos.items():
        gs =  GridSearchCV(config['model'], config['params'], cv=cv, return_train_score=False)
        gs.fit(X,y)
        scores.append({
            'model': algo_name,
            'best_score': gs.best_score_,
            'best_params': gs.best_params_
        })

    return pd.DataFrame(scores,columns=['model','best_score','best_params'])

def predict_price(location, sqft, bhk, bath):
    loc_index = np.where(x.columns==location)[0]

    d = np.zeros(len(x.columns))
    d[0] = sqft
    d[1] = bath
    d[2] = bhk
    if len(loc_index) > 0:
        if loc_index >= 0:
            d[loc_index] = 1
    
    d_df = pd.DataFrame([d], columns=x.columns)
        
    return model.predict(d_df)[0]
      
import pickle
with open('model.pickle', 'wb') as f:
    pickle.dump(model, f)
    
import json
columns = {
    'data_columns': [col.lower() for col in x.columns]
}
with open('columns.json', 'w') as f:
    f.write(json.dumps(columns))    

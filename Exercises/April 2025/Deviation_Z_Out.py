import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.stats import zscore
import matplotlib.pyplot as plt


df = pd.read_csv('bhp.csv')

upper_bound = df['price_per_sqft'].quantile(0.99)
lower_bound = df['price_per_sqft'].quantile(0.001)

df2 = df[(df['price_per_sqft'] >= lower_bound) & (df['price_per_sqft'] <= upper_bound)].copy()
df3 = df2[(df2['price_per_sqft'] <= df2['price_per_sqft'].mean() + 4 * df2['price_per_sqft'].std()) |
          (df2['price_per_sqft'] >= df2['price_per_sqft'].mean() - 4 * df2['price_per_sqft'].std())]

plt.hist(df3['price_per_sqft'], bins=30, density=True, alpha=0.6, color='g')

mean = df3['price_per_sqft'].mean()
std = df3['price_per_sqft'].std()
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mean, std)
plt.plot(x, p, 'k', linewidth=2)

plt.title('Histogram and Bell Curve of price_per_sqft')
plt.xlabel('Price per Sqft')
plt.ylabel('Density')
plt.show()

df2['zscore'] = zscore(df2['price_per_sqft'])
df4 = df2[df2['zscore'].abs() <= 4]

print('Outliers removed after z-score filtering: ' + str(df2.shape[0] - df4.shape[0]))
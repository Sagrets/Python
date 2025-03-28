import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.stats import zscore
import matplotlib.pyplot as plt


df = pd.read_csv('bhp.csv')

lower_bound = df['price_per_sqft'].quantile(0.001)
upper_bound = df['price_per_sqft'].quantile(0.99)

df2 = df[(df['price_per_sqft'] >= lower_bound) & (df['price_per_sqft'] <= upper_bound)]

print('Outliers removed after quantile filtering: ' + str(df.shape[0] - df2.shape[0]))

mean = df2['price_per_sqft'].mean()
std_dev = df2['price_per_sqft'].std()

df3 = df2[(df2['price_per_sqft'] >= mean - 4 * std_dev) & (df2['price_per_sqft'] <= mean + 4 * std_dev)]

print('Outliers removed after standard deviation filtering: ' + str(df2.shape[0] - df3.shape[0]))

plt.hist(df3['price_per_sqft'], bins=30, density=True, alpha=0.6, color='blue', label='Histogram')

x = np.linspace(df3['price_per_sqft'].min(), df3['price_per_sqft'].max(), 1000)
bell_curve = norm.pdf(x, mean, std_dev)

plt.plot(x, bell_curve, color='red', label='Bell Curve')

plt.xlabel('Price per Sqft')
plt.ylabel('Density')
plt.title('Histogram and Bell Curve of Price per Sqft')
plt.legend()

plt.show()

df3['zscore'] = zscore(df3['price_per_sqft'])
df4 = df3[(df3['zscore'] >= -4) & (df3['zscore'] <= 4)].drop(columns=['zscore'])

print('Outliers removed after z-score filtering: ' + str(df3.shape[0] - df4.shape[0]))
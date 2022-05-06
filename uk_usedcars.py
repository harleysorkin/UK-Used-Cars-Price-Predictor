# -*- coding: utf-8 -*-
"""UK_usedCars.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FyZdiz8gwWPQKLE00GEXpF8clzUdfQ3T
"""

from google.colab import files
files.upload()

import pandas as pd
import seaborn as sns
import numpy as np
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor

df = pd.read_csv('./cars_dataset.csv')

# Create two new columns for average price and average mpg for each model
df['avgPriceModel'] = df.groupby('model')['price'].transform('mean').round(2)
df['avgMpgModel'] = df.groupby('model')['mpg'].transform('mean').round(1)
df

# # pairplot of the dataframe, colored by Make
# sns.pairplot(df, hue = 'Make')

# # barplot representing Make vs price
# sns.barplot(x = 'Make', y = 'price', data = df)

# # lmplot of year vs price, separated by Make and colored by transmission type
# sns.lmplot(x = 'year', y = 'price', data = df, col = 'Make', hue = 'transmission', truncate = False, height = 5, col_wrap = 2)

# # Flatter regression lines indicate more stable resale value of the car the older it is, whereas steeper slopes indicate higher loss in value the older the car.

# # lmplot of mileage vs price, separated by Make
# sns.lmplot(x = 'mileage', y = 'price', data = df, col = 'Make', hue = 'Make', truncate = False, col_wrap = 2, height = 5, aspect = 0.75)

# # The flatter the regression line, the more value a car will hold despite higher mileage.

# # lmplot of avgPrice (of each model) vs avgMpg (of each model)
# sns.lmplot(data = df, x = 'avgPriceModel', y = 'avgMpgModel', hue = 'Make', truncate = False)

# # Negative regression shows average mpg goes down as the average price goes up.

# # Data distribution plot of price
# sns.displot(data = df, x = 'price')

# Drop unhelpful columns
df = df.drop(['tax'], axis = 1)

# Add 3 more aggregate columns
df['avgPriceMake'] = df.groupby('Make')['price'].transform('mean').round(2)
df['maxPriceModel'] = df.groupby('model')['price'].transform('max').round(2)
df['maxPriceMake'] = df.groupby('Make')['price'].transform('max').round(2)

df

le = preprocessing.LabelEncoder()

# LabelEncode transmission, fuelType, Make, and model columns using SKLearn's preprocessing.LabelEncoder
df['transmission'] = le.fit_transform(df['transmission'])
df['fuelType'] = le.fit_transform(df['fuelType'])
df['Make'] = le.fit_transform(df['Make'])
df['model'] = le.fit_transform(df['model'])

# # OneHotEncode model and Make columns using pd.get_dummies
# ''' X = pd.get_dummies(df, columns = ['model'])
# X = X.drop(['year', 'price', 'transmission', 'mileage', 'fuelType', 'mpg', 'engineSize', 'avgPriceModel', 'avgMpgModel'], axis = 1)
# df = pd.concat([df, X], axis = 1)
# df = df.drop(['model'], axis = 1)

# Y = pd.get_dummies(df, columns = ['Make'])
# Y = Y.drop(['year', 'price', 'transmission', 'mileage', 'fuelType', 'mpg', 'engineSize', 'avgPriceModel', 'avgMpgModel'], axis = 1)
# df = pd.concat([df, Y], axis = 1)
# df = df.drop(['Make'], axis = 1) '''

# Scale data using sklearn.preprocessing.StandarScaler
scaler = StandardScaler()
scaler.fit(df)
scaler.transform(df)

# Randomly sample rows from df for train and the remaining rows are left for test
train = df.sample(frac = 0.1, replace = False)
test = df.sample(frac = 0.9, replace = False)

# Create list of column names
a = list(df.columns)
a.remove('price')

# Training set
x = train[a]
y = train['price']

# Testing set
xt = test[a]
yt = test['price']

# Score with sklearn.linear_model.LinearRegression
reg = linear_model.LinearRegression()

reg.fit(x, y)
regscore = reg.score(xt, yt)

# Score with sklearn.linear_model.SGDRegressor
sgd = linear_model.SGDRegressor()

sgd.fit(x, y)
sgdscore = sgd.score(xt, yt)

print("Linear regression score:", regscore, "\nSGD regression score:", sgdscore)
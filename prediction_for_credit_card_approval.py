# -*- coding: utf-8 -*-
"""Prediction for Credit Card Approval.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QpR9pL5fRZMNwDmW37iUtQT3COJRaXZM

# **Problem Statement**
The primary objective of this project is to predict the approval or rejection of credit card applications.
The challenge lies in understanding the key factors influencing credit card approval decisions and
building a predictive model to assist in the decision-making process.

*1. Exploratory Data Analysis (EDA):*
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#load the datasets
train = pd.read_csv('/content/train_data.csv')
test = pd.read_csv('/content/test_data.csv')

#display the first few rows
train.head()

test.head()

#number of rows and columns
train.shape

test.shape

#bascis info about the training dataset
train.info()

#describing the train dataset
train.describe()

#univariate analysis
train.hist(figsize=(10,10))
plt.show()

#bivariate analysis
sns.pairplot(train, hue='Is high risk')
plt.show()

"""*2.Feature Engineering*"""

#creating 'Total Phones' feature by combining features
train['Total Phones'] = train['Has a mobile phone'] + train['Has a work phone'] + train['Has a phone']
test['Total Phones'] = test['Has a mobile phone'] + test['Has a work phone'] + test['Has a phone']

train.head()

"""*3. Data Preprocessing*"""

#checking for null values
train.isnull().sum()

test.isnull().sum()

#handling missing values
train['Job title'].fillna('Unknown', inplace=True)
test['Job title'].fillna('Unknown', inplace = True)

train['Age'] = (train['Age'].abs()/365).astype(int)
test['Age'] = (test['Age'].abs()/365).astype(int)

train['Employment length'] = (train['Employment length'].abs()/365).astype(int)
test['Employment length'] = (test['Employment length'].abs()/365).astype(int)

train['Account age'] = train['Account age'].abs()
test['Account age'] = test['Account age'].abs()

# Encoding the categorical variables
from sklearn.preprocessing import LabelEncoder

#list of variables to be encoded
variables = ['Gender','Has a car', 'Has a property',
             'Employment status',
             'Education level', 'Marital status',
             'Dwelling','Job title']

for var in variables:
  le = LabelEncoder()
  train[var] = le.fit_transform(train[var])
  test[var] = le.fit_transform(test[var])

train.head()

"""*4.Machine Learning Model Development*"""

#importing the models
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

x_train = train.drop(['ID','Is high risk'], axis=1)
y_train = train['Is high risk']
x_train, x_val, y_train, y_val = train_test_split(x_train,y_train,test_size=0.2)

#training the models
#Logistic Regression
lr = LogisticRegression()
lr.fit(x_train, y_train)

#Decision Tree
dt = DecisionTreeClassifier()
dt.fit(x_train, y_train)

#Random Forest
rf = RandomForestClassifier()
rf.fit(x_train, y_train)

#Gradient Boosting
gb = GradientBoostingClassifier()
gb.fit(x_train, y_train)

"""*5.Model Evaluation*"""

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score,roc_auc_score,confusion_matrix

def evaluate(model,x_val,y_val):
  preds = model.predict(x_val)
  accuracy = accuracy_score(y_val,preds)
  precision = precision_score(y_val,preds)
  recall = recall_score(y_val,preds)
  f1 = f1_score(y_val,preds)
  roc = roc_auc_score(y_val,preds)
  conf = confusion_matrix(y_val,preds)
  print("Accuracy: ",accuracy )
  print("Precision: ",precision)
  print("Recall: ",recall)
  print("F1 score: ",f1)
  print("ROC AUC: ",roc)
  print("Confusion Matrix: ",conf,"\n")

print("Logistic Regression")
evaluate(lr,x_val,y_val)

print("Decision Tree")
evaluate(dt,x_val,y_val)

print("Random Forest")
evaluate(rf,x_val,y_val)

print("Gradient Boosting")
evaluate(gb,x_val,y_val)

"""*6.Predicting Credit Card Approval*"""

#best performance model is Decision Tree
modified = test.drop(['ID','Is high risk'], axis=1)
test_preds = dt.predict(modified)
np.unique(test_preds)

sample_data = {
    'ID':[5827192],
    'Gender': ['Male'],
    'Has a car': [1],
    'Has a property': [0],
    'Children count': [2],
    'Income': [50000],
    'Employment status': ['Employed'],
    'Education level': ['Bachelor'],
    'Marital status': ['Married'],
    'Dwelling': ['House'],
    'Age': [35],
    'Employment length': [5],
    'Has a mobile phone': [1],
    'Has a work phone': [0],
    'Has a phone': [1],
    'Has an email': [1],
    'Job title': ['Manager'],
    'Family member count': [4],
    'Account age': [10],
    'Is high risk':[0],
    'Total Phones':[2]
}

sample_df = pd.DataFrame(sample_data)

sample_df = sample_df.drop(['ID','Is high risk'] ,axis=1)

#list of variables to be encoded
variables = ['Gender','Has a car', 'Has a property','Employment status','Education level', 'Marital status', 'Dwelling','Job title']

for var in variables:
  le = LabelEncoder()
  sample_df[var] = le.fit_transform(sample_df[var])

#making predictions
prediction = dt.predict(sample_df)

if prediction == 0:
  print("Credit Card Approved")
else:
  print("Credit Card Denied")


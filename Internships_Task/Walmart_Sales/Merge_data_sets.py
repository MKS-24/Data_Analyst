import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


features = pd.read_csv('D:/Data Analyst/Internship_Data/Walmart Sales Forecast/features.csv')
stores = pd.read_csv('D:/Data Analyst/Internship_Data/Walmart Sales Forecast/stores.csv')
merge_data = pd.merge(features,stores , on='Store' , how='left')
train=pd.read_csv('D:/Data Analyst/Internship_Data/Walmart Sales Forecast/train.csv')
df = pd.merge(merge_data,train , on=['Store','Date','IsHoliday'] , how='left')
print(df)

df.to_csv('Data_Set.csv' , index=False)

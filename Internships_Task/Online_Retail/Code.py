import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import numpy as np

df = pd.read_csv('D:/Data Analyst/Internship_Data/online+retail/Online_Retail.csv')


                                                 # 1. Data Understanding   
                                                
# Dulpiate Data
print('Duplicate Data',df.duplicated().sum()) # Duplicate Data 5268
df.drop_duplicates(inplace=True)
print('Duplicate Data',df.duplicated().sum()) # Duplicate Data 0

# - Check columns like InvoiceNo, StockCode, CustomerID, InvoiceDate, Quantity, UnitPrice
print(df.columns)

# - Inspect data size, data types, and missing values**
df.info()

# Missing values in each column
print(df.isnull().sum()) 



                                                 # 2. Data Cleaning 
# Drop records with missing CustomerID 
df.dropna(subset=['CustomerID'],inplace=True)
# Remove rows with negative or zero values in Quantity or UnitPrice (you can handle returns separately)  
return_df = df[(df['Quantity'] <= 0) & (df['UnitPrice'] <= 0)] # only include cancle or returned order
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
# Convert InvoiceDate to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'],errors = 'coerce')  
# print(df['InvoiceDate'])



                                                 # 3. RFM Metrics Calculate karna 🧮  
#   Set the **reference date** (e.g., one day after the last **InvoiceDate**) 
reference_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
print(reference_date)

# RFM Metrics
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (reference_date - x.max()).days,  # Recency
    'InvoiceNo': 'nunique',                                    # Frequency
    'TotalPrice': 'sum'                                        # Monetary
}).sort_values(by='InvoiceNo',ascending=False)

print(rfm)
rfm = rfm.reset_index()
rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
# print(rfm.columns)
# print(df.columns)
# print(len(df))
# df = pd.merge(df,rfm , on='CustomerID' , how='outer')
# print(df.columns)
# print(len(df))


# print(rfm['Recency'])
# 4. RFM Scoring & Binning   

#  Score Recency, Frequency, and Monetary on a 1–5 scale using quantiles
  
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])
# print(rfm)

#  Create a combined RFM score (e.g., R\_score × 100 + F\_score × 10 + M\_score)
rfm['Combine_score'] =   rfm['R_Score'].astype(int) * 100 + rfm['F_Score'].astype(int) * 10 + rfm['M_Score'].astype(int)
print(rfm)


# 5. Customer Segmentation (Labeling) 🏷️  
#    - Classic labels:  
#      • Champions  
#      • Loyal Customers  
#      • Potential Loyalists  
#      • At Risk  
#      • Lost Customers  
#    - Customize label names based on business needs 
def assign_segment(row):
    if row['R_Score'] >= 4 and row['F_Score'] >= 4:
        return 'Champions'
    elif row['F_Score'] >= 4:
        return 'Loyal Customers'
    elif row['R_Score'] >= 4 and row['F_Score'] >= 2:
        return 'Potential Loyalists'
    elif row['R_Score'] <= 2 and row['F_Score'] <= 2:
        return 'At Risk'
    elif row['R_Score'] == 1:
        return 'Lost'
    else:
        return 'Others'

rfm['Segment'] = rfm.apply(assign_segment, axis=1)


# 6. Visualization & Insights 📊  
fig,ax = plt.subplots(2,2,figsize = (17, 10) ,facecolor="#E9E9E9" ) 
sns.set_context('talk')
plt.suptitle('Online_Retail_Analysis',fontweight = 700 , fontfamily = 'cursive')


#    - Scatter plot (Recency vs Monetary) with segment colors  
ax[0][0].set_title('Recency vs Monetary Based On Segment',fontsize = 13 , fontweight = 600 , fontfamily = 'cursive')
sns.scatterplot(data=rfm , x = 'Recency' , y = 'Monetary', hue='Segment',ax=ax[0][0],s=40)
font_props = fm.FontProperties(family='cursive', size=10)
ax[0][0].legend(title='Segment', prop=font_props, title_fontsize=12)

#    Show revenue contribution using a pie or Pareto chart  
df['revenue'] = abs(df['Quantity'])*df['UnitPrice']
country_revenue = df.groupby('Country')['revenue'].sum().sort_values(ascending=False).head(5)
print(country_revenue)
print(country_revenue.index)
ax[0][1].set_title('Revenue contribution',fontsize = 13 , fontweight = 600 , fontfamily = 'cursive')
ax[0][1].pie(country_revenue.values,labels=country_revenue.index,explode=[0.6,0.5,0.4,0.3,0.2],textprops={'fontsize' : 8.5 , 'fontweight' : 400 ,'fontfamily' : 'cursive', 'color' : "#000000"},colors=['green','orange',"#2463d1","#21bebe","#29B888"],radius = 1 ,shadow=True,counterclock=True , autopct='%.2f%%')

#    - Line plot of Revenue trend over time
df['MonthYearStr'] = df['InvoiceDate'].dt.strftime('%b-%Y')
trends = df.groupby('MonthYearStr')['revenue'].sum()
print(trends)
trends = trends.reindex(['Dec-2010','Jan-2011','Feb-2011','Mar-2011','Apr-2011','May-2011','Jun-2011','Jul-2011','Aug-2011','Sep-2011','Oct-2011','Nov-2011','Dec-2011'] )
print(trends)
ax[1][0].set_title('Revenue Over Time',fontsize = 13 , fontweight = 600 , fontfamily = 'cursive')
ax[1][0].set_xlabel('Time',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")
ax[1][0].set_ylabel('Revenue',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")
ax[1][0].set_xticklabels(trends.index, fontfamily='cursive',rotation = 15,fontsize = 8.5)
ax[1][0].set_yticklabels(trends.values, fontfamily='cursive')
ax[1][0].grid(linestyle = ":" , linewidth = 0.5 , color = 'black' , alpha = 0.5)
ax[1][0].fill_between(trends.index,trends.values , alpha = 0.1 , color = '#FFA500')
ax[1][0].plot(trends.index,trends.values,color='green')

#    - Heatmap/bar chart of average R, F, M per segment  
segment_avg = rfm.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean().round(2)
print(segment_avg.corr())
ax[1][1].set_title('R, F, M Relation per segment',fontsize = 13 , fontweight = 600 , fontfamily = 'cursive')
sns.heatmap(data = segment_avg.corr() ,linewidths=1,edgecolor='black',annot=True, cmap='BuGn' ,vmax=1,vmin=-1)

sns.despine()
plt.tight_layout()
plt.savefig('Online_Retail.png',dpi=500)
plt.show()


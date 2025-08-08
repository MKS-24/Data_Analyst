import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import seaborn as sns


df = pd.read_csv('D:/Data Analyst/Internship_Data/Walmart Sales/Data_Set.csv')

# df.info()

#  Firstly, i want to change the date type of date colume from object to date.
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
print(df['Date'].dtype)  # now casting is done 
# df.info()

# Check duplicate if exist then drop same data for better results
print('Dupliacted data rows : ',df.duplicated().sum())

# Check Null values in data in order to deal with that rows
print(df.isnull().sum())

# Drop that data rowin which dept colume have null value , because i donot give any random value to dept
# print(df[df['Dept'].isnull()].index)
df.dropna(subset=['Dept'] , inplace=True)
print(df.isnull().sum())
df['Dept'] = df['Dept'].astype(int)

# Now, we have only null values present in markdown table so we can deal with later

# Convert Weekly Sales → Monthly Sales
df['Monthly_Date'] = df['Date'].dt.to_period('M')
print(df['Monthly_Date'].dtype)
store_monthly_trends = df.groupby(['Store','Monthly_Date'])['Weekly_Sales'].sum().sort_index()
store_monthly_trends=store_monthly_trends.reset_index()
store_monthly_trends.columns = ['Stores','Date','Monthly_Sales']
print(store_monthly_trends)

# store_monthly_trends['Stores']=store_monthly_trends['Stores'].astype(str)
store_monthly_trends['Date'] = store_monthly_trends['Date'].dt.strftime('%b-%Y')
store_monthly_trends['Date'] = store_monthly_trends['Date'].astype(str)



#                                                                    Visualization

plt.figure(figsize=(17, 10), facecolor="#E9E9E9")
sns.set_context('notebook')
plt.suptitle('Walmart Sales',fontsize = 25,fontweight = 700 , fontfamily = 'cursive')

ax = plt.subplot(2, 2, (1, 2))  
ax.set_facecolor("#E9E9E9")  
plt.ticklabel_format(style='plain', axis='y')
plt.title('Each Store Monthly Sales',fontsize = 13 , fontweight = 600 , fontfamily = 'cursive')
plt.xlabel('Dates',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")
plt.ylabel('Monthly Sales',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")

palette = sns.cubehelix_palette(45, start=0.5, rot=-.75, dark=0.2, light=0.8)
sns.lineplot(data=store_monthly_trends , x = 'Date' , y='Monthly_Sales' , hue='Stores' , palette=palette)

plt.legend(ncol=2, bbox_to_anchor=(1.000005, 1.1), loc='upper left', title='Stores' , fontsize = 6.5)
plt.xticks(rotation = 45,fontfamily='cursive',fontsize = 8.5)
plt.yticks(rotation = -15,fontfamily='cursive',fontsize = 8.5)
plt.grid(linestyle = ":" , linewidth = 0.4 , color = 'black' , alpha = 0.3)
sns.despine()





# Resample the data on a monthly basis using the Date column.
monthly_sales = df.resample('ME', on='Date')['Weekly_Sales'].sum()
monthly_sales = monthly_sales.reset_index()
monthly_sales.columns = ['Date','Monthly_Sales']
monthly_sales['Date'] = monthly_sales['Date'].dt.strftime('%b-%Y')

#                                                                    Visualization
ax = plt.subplot(2, 2, (3,4))  
ax.set_facecolor("#E9E9E9") 
plt.ticklabel_format(style='plain', axis='y')
plt.title('Overall Monthly Sales ',fontsize = 13 , fontweight = 600 , fontfamily = 'cursive')
plt.xlabel('Date',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")
plt.ylabel('Monthly Sales',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")

plt.plot(monthly_sales['Date'],monthly_sales['Monthly_Sales'],color="#013A30FF")

plt.ylim(143704000,300000000)
plt.xticks(rotation = 45,fontfamily='cursive',fontsize = 8.5)
plt.yticks(rotation = -15,fontfamily='cursive',fontsize = 8.5)
plt.grid(linestyle = ":" , linewidth = 0.4 , color = 'black' , alpha = 0.3)
plt.fill_between(monthly_sales['Date'],monthly_sales['Monthly_Sales'] , alpha = 0.1 , color = '#013A30FF')
ax.set_facecolor("#E9E9E9")  
sns.despine(top=True, right=True, left=True, bottom=True, trim=False)
plt.tight_layout()
plt.savefig('1_Walmart Sales.png',dpi=500)



# Moving Averages
# Apply 3-month and 6-month moving averages.
# 3 Months Rolling Average...
monthly_sales['3_Months_AVG'] = monthly_sales['Monthly_Sales'].rolling(window=3).mean()
monthly_sales['3_Months_AVG'] = monthly_sales['3_Months_AVG'].fillna(monthly_sales['Monthly_Sales'])

# 6 Months Rolling Average...
monthly_sales['6_Months_AVG'] = monthly_sales['Monthly_Sales'].rolling(window=6).mean()
monthly_sales['6_Months_AVG'] = monthly_sales['6_Months_AVG'].fillna(monthly_sales['Monthly_Sales'])

#Plot both of them together for trend smoothing.
plt.figure(figsize=(17, 10), facecolor="#E9E9E9")
sns.set_context('notebook')
plt.suptitle('Walmart Sales',fontsize = 25,fontweight = 700 , fontfamily = 'cursive')

ax = plt.subplot(2, 2, (1,2))  # ax object le lo taake uska bg set kar sako
ax.set_facecolor("#E9E9E9")  # plot area ka background color
plt.ticklabel_format(style='plain', axis='y')
plt.title('3 & 6 Months Rolling Average',fontsize = 13 , fontweight = 600 , fontfamily = 'cursive')
plt.xlabel('Date',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")
plt.ylabel('Rolling Average',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")

plt.plot(monthly_sales['Date'],monthly_sales['3_Months_AVG'],color="#069278FF",label=['3-Months'])
plt.plot(monthly_sales['Date'],monthly_sales['6_Months_AVG'],color="#045C4CFF",label=['6-Months'])
font_props = fm.FontProperties(family='cursive', size=10)
plt.legend(title='Segment', prop=font_props, title_fontsize=12 , facecolor = "#E9E9E9")


plt.ylim(143704000,300000000)
plt.xticks(rotation = 45,fontfamily='cursive',fontsize = 8.5)
plt.yticks(rotation = -15,fontfamily='cursive',fontsize = 8.5)
plt.grid(linestyle = ":" , linewidth = 0.4 , color = 'black' , alpha = 0.3)
plt.fill_between(monthly_sales['Date'],monthly_sales['Monthly_Sales'] , alpha = 0.1 , color = "#013A2FA7")
ax.set_facecolor("#E9E9E9")  # plot area ka background color
plt.text('Apr-2011',278000000,'Monthly Sales',fontsize = 10,fontfamily = 'cursive',bbox = {
    'facecolor' : 'white', 'edgecolor' : '#2f4b7c','alpha' : 0.7,'linewidth' : 0.8,'boxstyle': 'round,pad=0.2,rounding_size=0.3','facecolor':'#E9E9E9'
})
plt.annotate('' ,xy=('Dec-2010',260000000) , xytext=('Feb-2011',260000000) ,arrowprops={   
    'facecolor' : "#013A2FA7", 'shrink' : 0 , 'edgecolor' : 'grey', 'edgecolor' : 'grey','linewidth' : 0.1 , 'headwidth': 10,'headlength': 10,'width': 1})
plt.annotate('' ,xy=('Feb-2011',260000000) , xytext=('Feb-2011',280000000) ,arrowprops={   
    'facecolor' : "#013A2FA7", 'shrink' : 0 , 'edgecolor' : 'grey', 'edgecolor' : 'grey','linewidth' : 0.1 , 'headwidth': 0.1,'headlength': 0.1,'width': 1})
plt.annotate('' ,xy=('Feb-2011',280000000) , xytext=('Apr-2011',280000000) ,arrowprops={   
    'facecolor' : "#013A2FA7", 'shrink' : 0 , 'edgecolor' : 'grey', 'edgecolor' : 'grey','linewidth' : 0.1 , 'headwidth': 0.1,'headlength': 0.1,'width': 1})





sns.despine(top=True, right=True, left=True, bottom=True, trim=False)


plt.tight_layout()
plt.savefig('2_Walmart Sales.png',dpi=500)


#Seasonality
# Calculate the average sales for each month across multiple years.
monthly_avg_data = df.groupby('Monthly_Date')['Weekly_Sales'].mean()
monthly_sales.insert(2,'Monthly_AVG' , monthly_avg_data.values)
print(monthly_sales['Monthly_AVG'].sort_values(ascending=False))

# Create a bar plot of the average weekly sales for each month.
ax = plt.subplot(2, 2, 3) 
ax.set_facecolor("#E9E9E9")  
plt.title('Monthly Average Sales',fontsize = 13 , fontweight = 600 , fontfamily = 'cursive')
plt.xlabel('Date',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")
plt.ylabel('Monthly Average',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")
plt.ylim(12000,20500)
plt.bar(monthly_sales['Date'] , monthly_sales['Monthly_AVG'],width = 0.7,alpha=0.7, hatch='oo',color=["#E69F00", "#56B4E9", "#009E73", "#F0E442","#0072B2",  "#D55E00", "#CC79A7" ],edgecolor = 'black',linewidth = 0.5,linestyle = ':')
plt.xticks(rotation = 45,fontfamily='cursive',fontsize = 7)
plt.yticks(rotation = -15,fontfamily='cursive',fontsize = 8.5)

plt.grid(linestyle = ":" , linewidth = 0.5 , color = 'black' , alpha = 0.5)
plt.fill_between(monthly_sales['Date'] , monthly_sales['Monthly_AVG'] , alpha = 0.05 , color = "#013A2FA7")
plt.text('Feb-2011',18000,'Highest AVG Sales',fontsize = 10,fontfamily = 'cursive',bbox = {
    'facecolor' : 'white', 'edgecolor' : '#2f4b7c','alpha' : 0.7,'linewidth' : 0.8,'boxstyle': 'round,pad=0.2,rounding_size=0.3','facecolor':'#E9E9E9'
})
plt.annotate('' ,xy=('Dec-2010',19570) , xytext=('Dec-2010',20000) ,arrowprops={   
    'facecolor' : "#013A2FA7", 'shrink' : 0 , 'edgecolor' : 'grey', 'edgecolor' : 'grey','linewidth' : 0.1 , 'headwidth': 5,'headlength': 5,'width': 1})
plt.annotate('' ,xy=('Dec-2010',20000) , xytext=('May-2011',20000) ,arrowprops={   
    'facecolor' : "#013A2FA7", 'shrink' : 0 , 'edgecolor' : 'grey', 'edgecolor' : 'grey','linewidth' : 0.1 , 'headwidth': 0.1,'headlength': 0.1,'width': 1})
plt.annotate('' ,xy=('May-2011',20000) , xytext=('May-2011',18410) ,arrowprops={   
    'facecolor' : "#013A2FA7", 'shrink' : 0 , 'edgecolor' : 'grey', 'edgecolor' : 'grey','linewidth' : 0.1 , 'headwidth': 0.1,'headlength': 0.1,'width': 1})
sns.despine(top=True, right=True, left=True, bottom=True, trim=False)
plt.tight_layout()



# Breakdown by Product and Region
top_depts = df.groupby("Dept")["Weekly_Sales"].sum().nlargest(5)
print(top_depts)
ax = plt.subplot(2, 2, 4)  
ax.set_facecolor("#E9E9E9")  
plt.ticklabel_format(style='plain', axis='y')
plt.title('Top 5 Departments - Total Sales',fontsize = 13 , fontweight = 600 , fontfamily = 'cursive')
plt.xlabel('Department',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")
plt.ylabel('Sales',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")
plt.ylim(100000000,600000000)
plt.bar(top_depts.index , top_depts.values,width=1.7,color=["#E69F00", "#56B4E9", "#009E73", "#F0E442","#0072B2",  "#D55E00", "#CC79A7" ] ,alpha=0.7, hatch='oo',edgecolor = 'black',linewidth = 0.5,linestyle = ':')
plt.xticks(rotation = 45,fontfamily='cursive',fontsize = 8.5)
plt.yticks(rotation = -15,fontfamily='cursive',fontsize = 8.5)

plt.grid(linestyle = ":" , linewidth = 0.5 , color = 'black' , alpha = 0.5)
plt.text(50,400000000,'Highest Sales (Dept = 92)',fontsize = 10,fontfamily = 'cursive',bbox = {
    'facecolor' : 'white', 'edgecolor' : '#2f4b7c','alpha' : 0.7,'linewidth' : 0.8,'boxstyle': 'round,pad=0.2,rounding_size=0.3','facecolor':'#E9E9E9'
})
plt.annotate('' ,xy=(92,483943300) , xytext=(92,520000000) ,arrowprops={   
    'facecolor' : "#013A2FA7", 'shrink' : 0 , 'edgecolor' : 'grey', 'edgecolor' : 'grey','linewidth' : 0.1 , 'headwidth': 5,'headlength': 5,'width': 1})
plt.annotate('' ,xy=(92,520000000) , xytext=(58.5,520000000) ,arrowprops={   
    'facecolor' : "#013A2FA7", 'shrink' : 0 , 'edgecolor' : 'grey', 'edgecolor' : 'grey','linewidth' : 0.1 , 'headwidth': 0.1,'headlength': 0.1,'width': 1})
plt.annotate('' ,xy=(58.5,520000000) , xytext=(58.5,426000000) ,arrowprops={   
    'facecolor' : "#013A2FA7", 'shrink' : 0 , 'edgecolor' : 'grey', 'edgecolor' : 'grey','linewidth' : 0.1 , 'headwidth': 0.1,'headlength': 0.1,'width': 1})
sns.despine(top=True, right=True, left=True, bottom=True, trim=True)
plt.tight_layout()
plt.savefig('3_Walmart Sales.png',dpi=500)
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

                                    # Merging Data 
                                    
# d1 = pd.read_csv('D:/Data Analyst/Internship_Data/titanic/train.csv')
# d2 = pd.read_csv('D:/Data Analyst/Internship_Data/titanic/test.csv')
# d3 = pd.read_csv('D:/Data Analyst/Internship_Data/titanic/gender_submission.csv')
# concate_data = pd.merge(d2,d3 , on='PassengerId' , how='outer')
# df = pd.concat([d1,concate_data], axis=0)
# df.to_csv('titanic.csv', index=False)


df = pd.read_csv('D:/Data Analyst/Internship_Data/titanic/titanic.csv')

df.drop_duplicates(inplace=True)

# Which columns (features) are there in the dataset?
print(df.columns)

                                    
# Which columns have missing values?
null_columns = df.isnull().sum()
print(null_columns[null_columns.values != 0].index)

# Handle the missing values?
df['Age'] = df['Age'].fillna(df['Age'].mean())
df.drop(['Cabin'],axis=1,inplace=True)
df['Fare'] = df['Fare'].fillna(df['Fare'].mean())
df.dropna(subset='Embarked',inplace=True)
print('Now Data becomes clean')
print(df.isnull().sum())

# Which column needs a data type change and why?
# Because Age is non decimal numebr
df['Age'] = df['Age'].astype(int)
print(df.dtypes)



# How many total passengers are there in the dataset?
total_passenger = df['PassengerId'].count()
print('Total Number of Passengers on ship are :',total_passenger)
# What is the ratio of survived to not survived passengers?
s_vs_ns = df['Survived'].value_counts()
not_survived = s_vs_ns[0] / total_passenger * 100
survived = s_vs_ns[1] / total_passenger * 100
print('Survived ratio is',int(round(survived,0)))
print('Not Survived ratio is',int(round(not_survived,0)))

fig,ax = plt.subplots(2,2,figsize = (17, 10) ,facecolor="#E9E9E9" ) 
sns.set_context('talk')
plt.suptitle('Titanic Data Analysis',fontweight = 700 , fontfamily = 'cursive')

ax[0][0].set_title('Survived Vs Not Survived',fontsize = 13 , fontweight = 600 , fontfamily = 'cursive')
ax[0][0].pie([not_survived,survived],textprops={'fontsize' : 12 , 'fontweight' : 500 ,'fontfamily' : 'cursive', 'color' : "#000000"},radius = 1.1,startangle = 90 ,counterclock=True,labels=['Not_Survived' , 'Survived'] ,shadow=True , colors=['orange','green'], explode=[0.1,0] , autopct='%.2f%%')




# What was the survival rate based on gender?
print('Gender Wise Survival Rate ')
# print(df.groupby(['Sex','Survived'])['Survived'].count())  non_efficient step for this question
survival_rate = df.groupby('Sex')['Survived'].sum()
print(survival_rate) # my smart step for this question
ax[0][1].set_title('Gender-Wise Survival Rate',fontsize = 13 , fontweight = 600 , fontfamily = 'cursive')
ax[0][1].set_xlabel('Gender',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")
ax[0][1].set_ylabel('Survived Count',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")
ax[0][1].set_ylim(0,600)
bars = ax[0][1].bar(survival_rate.index , survival_rate.values,width = 0.2,alpha=0.7, hatch='oo',color =['orange','green'],edgecolor = 'black',linewidth = 0.5,linestyle = ':')
for bar in bars:
    yval = bar.get_height()
    ax[0][1].text(bar.get_x() + bar.get_width()/2, yval + 9 , yval, ha='center',fontsize = 10,fontfamily = 'cursive')
ax[0][1].set_xticklabels(survival_rate.index, fontfamily='cursive')
ax[0][1].grid(linestyle = ":" , linewidth = 0.5 , color = 'black' , alpha = 0.5)
ax[0][1].fill_between(survival_rate.index,survival_rate.values , alpha = 0.05 , color = 'black')


# What was the survival rate based on passenger class (Pclass)?
print('Passenger class Survival Rate')
p_survival = df.groupby('Pclass')['Survived'].sum()
print(p_survival)

ax[1][0].set_title('Passenger Class Survival Rate',fontsize = 13 , fontweight = 600 , fontfamily = 'cursive')
ax[1][0].set_xlabel('Passenger Class',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")
ax[1][0].set_ylabel('Survived Count',fontsize = 12 , fontweight = 500 ,fontfamily = 'cursive', color = "#000000")
ax[1][0].set_ylim(65,200)
ax[1][0].bar(p_survival.index , p_survival.values,width = 0.2,alpha=0.7, hatch='oo',color =['orange','green','#008080'],edgecolor = 'black',linewidth = 0.5,linestyle = ':')
ax[1][0].grid(linestyle = ":" , linewidth = 0.5 , color = 'black' , alpha = 0.5)
ax[1][0].fill_between(p_survival.index,p_survival.values , alpha = 0.05 , color = 'black')
ax[1][0].text(2.75,191,'191',fontsize = 10,bbox = {
    'facecolor' : 'white', 'edgecolor' : '#2f4b7c','alpha' : 0.7,'linewidth' : 0.8,'boxstyle': 'round,pad=0.2,rounding_size=0.3'
})
ax[1][0].annotate('' ,xy=(2.9,193) , xytext=(3,193) ,arrowprops={   
    'facecolor' : '#2f4b7c', 'shrink' : 0 , 'edgecolor' : 'grey','linewidth' : 0.1 , 'headwidth': 4,'headlength': 6,'width': 0.7})


ax[1][0].text(1.13,184,'184',fontsize = 10,bbox = {
    'facecolor' : 'white', 'edgecolor' : '#2f4b7c','alpha' : 0.7,'linewidth' : 0.8,'boxstyle': 'round,pad=0.2,rounding_size=0.3'
})
ax[1][0].annotate('' ,xy=(1.11,186) , xytext=(1,186) ,arrowprops={   
    'facecolor' : '#2f4b7c', 'shrink' : 0 , 'edgecolor' : 'grey','linewidth' : 0.1 , 'headwidth': 4,'headlength': 6,'width': 0.7})

ax[1][0].text(1.935,148.7,'150',fontsize = 10,bbox = {
    'facecolor' : 'white', 'edgecolor' : '#2f4b7c','alpha' : 0.7,'linewidth' : 0.8,'boxstyle': 'round,pad=0.2,rounding_size=0.3'
})
ax[1][0].annotate('' ,xy=(2.001,144.6) , xytext=(2.001,119.6) ,arrowprops={   
    'facecolor' : '#2f4b7c', 'shrink' : 0 , 'edgecolor' : 'grey','linewidth' : 0.1 , 'headwidth': 4,'headlength': 6,'width': 0.7})


# What was the effect of age on survival?
print(df[['Age','Survived']].corr())
print("Negative Correlation indicate that if age less then survival chances are very high as compared to high age person")
ax[1][1].set_title('Age Effect On Survival',fontsize = 13 , fontweight = 600 , fontfamily = 'cursive')
sns.heatmap(data = df[['Age','Survived']].corr() ,annot=True, cmap='BuGn' ,vmax=1,vmin=-1)



sns.despine()
plt.tight_layout()
plt.savefig('Titanic_EDA.png',dpi=500)
plt.show()


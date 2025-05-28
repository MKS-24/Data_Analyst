import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('D:/Data Analyst/4_Prac/netflix_titles.csv')

# Check Data Set Loaded Successfully!
# print(df.head())

# Understand The Data Set
# df.info()



# Figure Size and Subplots Row and Colume
fig,ax = plt.subplots(2,2,figsize = (10,10))
plt.suptitle("Netfix Data 1925 - 2021",fontweight = 800,fontsize = 20,family='monospace',alpha = 0.7)

# 1. Netflix par har saal (release\_year) kitne shows aur movies release hue?**
#    Bar chart banao jo har saal ke total releases dikhaye.

count_by_release_year = df.pivot_table(index='release_year' , columns='type' , values='show_id' , aggfunc='count')
# print(count_by_release_year)
movies = []  # Hold Count of all Movies each year 
for i in range(len(count_by_release_year)):
    movies.append(count_by_release_year.values[i][0])
shows = []  # Hold Count of all Shows each year 
for i in range(len(count_by_release_year)):
    shows.append(count_by_release_year.values[i][1])
width = 0.2
ax[0,0].set_title("Movies & Shows By Years")
ax[0,0].set_xlabel("Years",color = 'blue',alpha = 0.7)
ax[0,0].set_ylabel("Content Count",color = 'blue',alpha = 0.7)
ax[0,0].bar(count_by_release_year.index , movies , width = width , label = 'Movies')
ax[0,0].bar(count_by_release_year.index + width , shows , width = width ,  label = 'Shows')
ax[0,0].grid(linestyle = ':' , linewidth = 0.5 , color = 'grey')
ax[0][0].legend(loc=2)


# 2. **Movie aur TV Show ka mukabla karo**
#    Pie chart banao jo dikhaye ke kitne percent content Movies hain aur kitne TV Shows.
ax[0,1].set_title("Movie vs Shows")
count_Movie_Shows = df['type'].value_counts().sort_values(ascending=False)
ax[0][1].pie(count_Movie_Shows.values ,labels = count_Movie_Shows.index,startangle = 15, textprops={'fontsize': 8}, explode = [0.2,0] ,shadow = True, autopct = '%.2f%%' , colors = ['orange','skyblue'] )



# 3. **Top 10 countries jin se sabse zyada content aaya hai?**
#    Bar chart banao jo sabse zyada producing countries ko dikhaye (country column ka use karo).

# print(df[['show_id' , 'release_year']].isnull().sum()) # first check for null data
TTCountry = df['country'].value_counts().sort_values(ascending=False).head(10)
ax[1,0].set_title("Top 10 Countries For Producing Content")
ax[1,0].set_xlabel("Years",color = 'blue',alpha = 0.7)
ax[1,0].set_ylabel("Content Count",color = 'blue',alpha = 0.7)
ax[1,0].bar(TTCountry.index , TTCountry.values , width = width , label = 'Countries',hatch = 'oo' ,color = 'orange',alpha = 0.5)
ax[1,0].grid(linestyle = ':' , linewidth = 0.5 , color = 'grey')
ax[1][0].legend(loc=2)
ax[1,0].set_xticklabels(TTCountry.index, rotation=22,fontsize = 7)            # labels set karo aur rotate karo




# 4. **Top 5 genres (listed\_in column) ka analysis karo**
#    Bar chart banao jo sabse zyada popular genres ko dikhaye.

# print(df['listed_in'].isnull().sum()) # first check for null data

genres_data = df['listed_in'].str.split(',').apply(lambda x: [i.strip() for i in x]).explode().value_counts().sort_values(ascending=False).head(5)
ax[1,1].set_title("Top 5 Genres")
ax[1,1].set_xlabel("Genres",color = 'blue',alpha = 0.7)
ax[1,1].set_ylabel("Genres Count",color = 'blue',alpha = 0.7)
ax[1,1].bar(genres_data.index , genres_data.values , width = width , label = 'Genres',hatch = 'oo' ,color = 'orange',alpha = 0.5)
ax[1,1].grid(linestyle = ':' , linewidth = 0.5 , color = 'grey')
ax[1][1].legend(loc=1)
ax[1][1].set_xticklabels(genres_data.index , rotation = 6,fontsize = 7)

# plt.tight_layout()
# plt.savefig("Graph_1.png",dpi = 300)


fig,ax = plt.subplots(2,2,figsize = (15,10))
plt.suptitle("Netfix Data 1925 - 2021",fontweight = 800,fontsize = 20,family='monospace',alpha = 0.7)



# 5. **Har rating (G, PG, TV-MA, etc.) ke kitne shows/movies hain?**
#    Horizontal bar chart banao jo rating-wise distribution show kare.

# print(df['rating'].isnull().sum()) # found_Null Data so remove first
rating_df = df.copy()
drop_index =  rating_df[(rating_df['rating'] == '74 min') | (rating_df['rating'] == '84 min') | (rating_df['rating'] == '66 min')].index
rating_df.drop(drop_index , axis = 0 ,inplace=True)
main_rating_data = rating_df.pivot_table(index='rating' , columns='type' , values='show_id' , aggfunc='count')

movies = []
for i in range(len(main_rating_data)):
    movies.append(main_rating_data.values[i][0])
shows = []
for i in range(len(main_rating_data)):
    shows.append(main_rating_data.values[i][1])

width = 0.2
lengthSpace = np.arange(len(main_rating_data.index))
# print(lengthSpace)
ax[0,0].set_title("Rating of Movies and Shows")
ax[0,0].set_xlabel("Content Count",color = 'blue',alpha = 0.7)
ax[0,0].set_ylabel("Ratings",color = 'blue',alpha = 0.7)
ax[0,0].barh(lengthSpace , movies , width ,hatch = 'oo',label = 'Movie',alpha = 0.7, color = 'blue')
ax[0,0].barh(lengthSpace + width , movies , width ,hatch = 'oo' , label = 'Show' , alpha = 0.5 , color = 'orange')
ax[0,0].set_yticks(lengthSpace + width/2 , main_rating_data.index )
ax[0,0].set_yticklabels(main_rating_data.index,rotation = 25)
ax[0,0].grid(linestyle = ':' , linewidth = 0.5 , color = 'grey')
ax[0][0].legend(loc=1)



# 6. **Director-wise content distribution**
#    Top 10 directors jin ke naam sabse zyada baar aaye hain unka bar chart banao.
# directors = df['director'].isnull().sum() # Check Null Values of Directors not nescessay for this particular Question
directors = df['director'].value_counts().sort_values(ascending=False).head(10)
ax[0,1].set_title("Top 10 Directors For Producing Content")
ax[0,1].set_xlabel("Director",color = 'blue',alpha = 0.7)
ax[0,1].set_ylabel("Director Content",color = 'blue',alpha = 0.7)
ax[0,1].bar(directors.index , directors.values , width = width , label = 'Director',hatch = 'oo' ,color = 'orange',alpha = 0.5)
ax[0,1].grid(linestyle = ':' , linewidth = 0.5 , color = 'grey')
ax[0,1].legend(loc=1)
ax[0,1].set_xticks(range(len(directors.index)))
ax[0,1].set_xticklabels(directors.index,rotation = 18,fontsize = 7)


# 7. **Har country ke TV Shows count karo (sirf TV Shows ke liye)**
#    Country-wise bar chart banao lekin sirf type == "TV Show" filter kar ke.
data = df.dropna(subset='country').copy() # Not Compulsary tu clean data
data['country'] = data['country'].str.split(',').apply(lambda x: [i.strip() for i  in x])
data = data.explode('country')
data = data[data['country'] != '']
country_shows = data[data['type'] == 'TV Show'].groupby('country')['show_id'].count().sort_values(ascending=False).head(10)
ax[1,0].set_title("Top 10 Countries For Producing TV Shows")
ax[1,0].set_xlabel("Countries",color = 'blue',alpha = 0.7)
ax[1,0].set_ylabel("TV Shows Count",color = 'blue',alpha = 0.7)
ax[1,0].bar(country_shows.index , country_shows.values , width = width , label = 'Director',hatch = 'oo' ,color = 'orange',alpha = 0.5)
ax[1,0].grid(linestyle = ':' , linewidth = 0.5 , color = 'grey')
ax[1,0].legend(loc=1)
ax[1,0].set_xticks(range(len(country_shows.index)))
ax[1,0].set_xticklabels(country_shows.index,rotation = 15,fontsize = 7)


# 8. **Year-wise content trends of only Documentaries**
#    Har saal kitne Documentaries release hue? (listed\_in column mein “Documentaries” ho)

documentries_data = df[df['listed_in'] == 'Documentaries'].groupby('release_year')['listed_in'].count()
ax[1,1].set_title("Year_Wise Trends Of Documentaries")
ax[1,1].set_xlabel("Years",color = 'blue',alpha = 0.7)
ax[1,1].set_ylabel("Documentaries_count",color = 'blue',alpha = 0.7)
ax[1,1].plot(documentries_data.index , documentries_data.values , label = 'Documentaries',color = 'b',linewidth = 2)
ax[1,1].grid(linestyle = ':' , linewidth = 0.5 , color = 'grey')
ax[1,1].legend(loc=2)
ax[1,1].fill_between(documentries_data.index , documentries_data.values,color = 'orange' , alpha = 0.8)

# plt.tight_layout()
# plt.savefig("Graph_2.png",dpi = 300)



fig , ax = plt.subplots(2,1 , sharey = True)
plt.suptitle("Netfix Data 1925 - 2021",fontweight = 800,fontsize = 20,family='monospace',alpha = 0.7)



# 9. **Duration ke basis par Movies ka analysis karo**
#     Sirf movies ke liye duration column ka numeric part lo (minutes), aur histogram banao jo unki duration distribution dikhaye.

# print(df[df['duration'].isnull()].index) Null Value index in df['duration]
# print(df.loc[df[df['duration'].isnull()].index,['type' , 'duration']])

data = df[df['type'] == 'Movie'].copy()
# print(len(data['type']))
data['duration'] = data[data['duration'].str.contains('min' , na=False)]['duration']
data.dropna(subset='duration',inplace=True)
data['duration'] = data['duration'].str.replace('min','').astype(int)
ax[0].set_title("Analysis Movies Over Duration")
ax[0].set_xlabel("Duration",color = 'blue',alpha = 0.7)
ax[0].set_ylabel("Duration Count",color = 'blue',alpha = 0.7)
ax[0].hist(data['duration'],bins = [i for i in range(0,401,10)],alpha=0.5,linewidth = 2,edgecolor = 'blue',color = 'orange',hatch = 'x' ,label='Duration')
ax[0].legend()
ax[0].grid(linestyle = ':' , linewidth = 0.5 , color = 'grey')



# 10. **Monthly release trend**
#    Kis month mein sabse zyada content add hua? (`date_added` column ka month extract karo, phir bar chart banao)

# print(df['date_added'].isnull().sum())  
date_df = df.copy()  # Copy data
# print(date_df[date_df['date_added'].isnull()]['date_added']) # Get index of Null data in date_added colume
date_df.dropna(subset='date_added',inplace=True) # Remove All Null Values
date_df['date_added'] = pd.to_datetime(date_df['date_added'], errors='coerce')  #Convert Date into int date formate from str date format
date_df['date_added'] = date_df['date_added'].dt.month_name()  # now converted number to month name
month_trend = date_df.groupby('date_added')['show_id'].count() # count no. of conent with respect to months
# print(month_trend)
month_order = ['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December']
month_trend = month_trend.reindex(month_order)
# print(month_trend)
ax[1].set_title("Month_Wise Trends Of Content")
ax[1].set_xlabel("Months",color = 'blue',alpha = 0.7)
ax[1].set_ylabel("Content",color = 'blue',alpha = 0.7)
ax[1].plot(month_trend.index , month_trend.values , label = 'Months',color = 'b',linewidth = 2)
ax[1].grid(linestyle = ':' , linewidth = 1.5 , color = 'grey')
ax[1].legend(loc=1)
ax[1].fill_between(month_trend.index , month_trend.values,color = 'orange' , alpha = 0.8)
ax[1].set_xticklabels(month_trend.index,rotation = 15,fontsize = 7)


# plt.tight_layout()
# plt.savefig("Graph_3.png",dpi = 300)


plt.tight_layout()
plt.show()
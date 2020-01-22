#Import dependencies
import pandas as pd
import numpy as np
import json
from sqlalchemy import create_engine
import psycopg2 as ps

# Read the csv
movie_data = pd.read_csv("./Resources/tmdb_5000_movies.csv")
# movie_data.head(2)
credits_data = pd.read_csv("./Resources/tmdb_5000_credits.csv")
# credits_data.head(2)
movie_data.count()
# credits_data.count()

# Convert the two datasets into a DataFrame
movie_data1 = pd.DataFrame(movie_data)
# movie_data1
credits_data1 = pd.DataFrame(credits_data)
# credits_data1.count()

# We merge teh two DatFrames into one
merge_df = pd.merge(left=movie_data1, right=credits_data1, how="left")
# merge_df.head(46)

# We will select all the rows that doesn't have the empty branches in the following columns
merge_df_1 = merge_df[merge_df.production_countries != '[]']
#merge_df_1.count()
merge_df_2 = merge_df_1[merge_df_1.genres != '[]']
#merge_df_2.head(273)
merge_df_3 = merge_df_2[merge_df_2.crew != '[]']
#merge_df_3.head()
merge_df_4 = merge_df_3[merge_df_3.cast != '[]']
#merge_df_4.head()

# We reset index
merge_new_index = merge_df_4.reset_index()
#merge_new_index.head()

# Clean the column genres ()
genre = []
for i in range(0,len(merge_new_index['genres'])):
    try:
        python_dict = json.loads(merge_new_index["genres"][i])
        genre.append(python_dict[0]['name'])
    except IndexError:
        genre.append(" ")

genres_df = pd.DataFrame(genre)
#genres_df.head(2)
#genres_df.count()

# Clean the column country
country =[]
for i in range(0,len(merge_new_index['production_countries'])):
    try:
        python_dict = json.loads(merge_new_index["production_countries"][i])
        country.append(python_dict[0]['name'])
    except IndexError:
        country.append(" ")
        
country_df = pd.DataFrame(country)
#country_df.head(2)
#country_df.count()

# Clean the column cast
cast1 =[]
for i in range(0,len(merge_new_index['cast'])):
    try:
        python_dict = json.loads(merge_new_index["cast"][i])
        cast1.append(python_dict[0]['name'])
    except IndexError:
        cast1.append(" ")
        
cast1_df = pd.DataFrame(cast1)
#cast1_df.head(2)
#cast1_df.count()

# Clean the column cast
cast2 =[]
for i in range(0,len(merge_new_index['cast'])):
    try:
        python_dict = json.loads(merge_new_index["cast"][i])
        cast2.append(python_dict[1]['name'])
    except IndexError:
        cast2.append(" ")

cast2_df = pd.DataFrame(cast2)
#cast2_df.head(2)
#cast2_df.count()

# Clean the column cast
cast3 =[]
for i in range(0,len(merge_new_index['cast'])):
    try:
        python_dict = json.loads(merge_new_index["cast"][i])
        cast3.append(python_dict[2]['name'])
    except IndexError:
        cast3.append(" ")
        
cast3_df = pd.DataFrame(cast3)
#cast3_df.head(2)
#cast3_df.count()

# Clean the column crew and take the information that we need (Director)
director=[]

for j in range(0,len(merge_new_index["crew"])):
    try:
        python_dict = json.loads(merge_new_index["crew"][j])
        directores = [x for x in python_dict if x["job"]=="Director"]
        if(len(directores)>0):
            director.append(directores[0]["name"])
        else:
            director.append("")
    except IndexError:
        director.append("")

director_df = pd.DataFrame(director)
#director_df.head(2)
#director_df.count()

# fill rows that don't have information with "NaN"
merge_new_index = merge_new_index.fillna(value="NaN")
#merge_new_index.count()

# Add the columns that we need for the analisis
merge_new_index["Genre"] = genres_df
merge_new_index["Country"] = country_df
merge_new_index["Leading Role"] = cast1_df
merge_new_index["Supporting Role"] = cast2_df
merge_new_index["Supporting Role 2"] = cast3_df
merge_new_index["Director"] = director_df
#merge_new_index.count()
#merge_new_index.head(20)

# Delete the columns that we don't need
movie_data_needed = merge_new_index.drop(['genres','homepage', 'keywords', 'overview',
              'popularity', 'production_companies', 'status','tagline',
              'original_title', 'production_countries', 'spoken_languages','index','cast','crew','movie_id','id','vote_count'], axis = 1)
#movie_data_needed.head(2)
#movie_data_needed.count()

# Rename columns
Renamed_Movie_Data_df = movie_data_needed.rename(columns = {'budget':'Budget',
                                            'original_language':'Language',
                                            'release_date':'Release_Date',
                                            'revenue':'Revenue',
                                            'runtime':'Runtime',
                                            'title':'Title',
                                            'vote_average':'Rating',
                                            'vote_count':'Vote_Count',
                                            'Leading Role':'Leading_Role',
                                            })
#Renamed_Movie_Data_df.count()
#Renamed_Movie_Data_df.head(3000)

# We count the unique values of genre
Renamed_Movie_Data_df.Genre.value_counts()

#We convert the DataFrame into python dicts
Movie_list = Renamed_Movie_Data_df.to_dict()
Movie_String = {key: str(value) for (key, value) in Movie_list.items()}


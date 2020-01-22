#Import dependencies
import pymongo
from pymongo import MongoClient
from data import Renamed_Movie_Data_df
import pandas as pd 
import json

#String connection
conn = "mongodb://localhost:27017"
#Creation of Mongo Client
client = pymongo.MongoClient(conn)
#Conection to the DataBase
db = client.moviesProject_DB
#Drop the content if any
db.moviesProject.drop() 

for x in range(0, len(Renamed_Movie_Data_df)):
    document = Renamed_Movie_Data_df.iloc[x].to_dict()
    document = {x: str(y) for x,y in document.items()}
    db.moviesProject.insert_one(document)
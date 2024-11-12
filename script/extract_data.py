from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI, database name, and collection name from environment variables
mongodb_uri = os.getenv('MONGO_URI')
dbname = os.getenv('MONGO_DBNAME')
query_news = os.getenv('QUERY_news')

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[dbname]
collection_fin = db['data_finance']
collection_news = db['data_news']

# Retrieve all documents from the collection
documents_fin = collection_fin.find()
documents_news = collection_news.find()

# Convert the documents to a list of dictionaries
data_fin = list(documents_fin)
data_news = list(documents_news)

# Convert the list of dictionaries to a DataFrame
df_fin = pd.DataFrame(data_fin)
df_news = pd.DataFrame(data_news)

# Split the source column into id_source and name_source columns
df_news[['id_source', 'name_source']] = df_news['source'].apply(lambda x: pd.Series([x['id'], x['name']]))
df_news.drop('source', axis=1, inplace=True)

df_news['title'] = df_news['title'].str.lower()
df_news['query_count_titre'] = df_news['title'].str.count(query_news)

df_news['content'] = df_news['content'].str.lower()
df_news['query_count_content'] = df_news['content'].str.count(query_news)

# Display the DataFrames
print("DataFrame df_fin:")
print(df_fin)
print("\nDataFrame df_news:")
print(df_news)

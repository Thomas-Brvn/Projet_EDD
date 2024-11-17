from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI, database name, and collection name from environment variables
mongodb_uri = os.getenv('MONGO_URI')
dbname = os.getenv('MONGO_DBNAME')

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

# Convert the date columns to datetime objects
df_fin['date'] = pd.to_datetime(df_fin['date'])
df_news['publishedAt'] = pd.to_datetime(df_news['publishedAt'])
 
# Format the date columns to a consistent format (e.g., 'YYYY-MM-DD')
df_fin['date'] = df_fin['date'].dt.strftime('%Y-%m-%d')
df_news['publishedAt'] = df_news['publishedAt'].dt.strftime('%Y-%m-%d')

# Export DataFrames to CSV files in the specified directory
base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, '..', 'data')
df_fin.to_csv(os.path.join(output_dir, 'data_finance.csv'), index=False, encoding='utf-8')
df_news.to_csv(os.path.join(output_dir, 'data_news.csv'), index=False, encoding='utf-8')

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

def connect_mongo(uri):
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client

def create_connect_db(client, db_name):
    db = client[db_name]
    return db

def create_connect_collection(db, col_name):
    collection = db[col_name]
    return collection

def extract_api_data(url):
    return requests.get(url).json()

def insert_data(col, data):
    docs = col.insert_many(data)
    n_doc_inseridos = len(docs.inserted_ids)
    return n_doc_inseridos

if __name__ == "__main__":
    client = connect_mongo(MONGO_URI)
    db = create_connect_db(client, "db_products_ch")
    col = create_connect_collection(db, "products")

    data = extract_api_data("https://labdados.com/produtos")
    print(f"\nQuantidade de dados extraidos: {len(data)}")

    n_docs = insert_data(col, data)
    print(f"\nQuantidade de documentos inseridos: {n_docs}")

    client.close()
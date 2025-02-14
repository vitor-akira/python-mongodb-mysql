from extract_and_save_data import connect_mongo, create_connect_db, create_connect_collection
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

def visualize_collection(col, limit=5):
    for i, doc in enumerate(col.find()):
        if i >= limit:
            break
        print(doc)

def rename_column(col, col_name, new_name):
    col.update_many({}, {"$rename": {f"{col_name}": f"{new_name}"}})

def select_category(col, category):
    query = { "Categoria do Produto": f"{category}"}
    
    lista_categoria = []
    for doc in col.find(query):
        lista_categoria.append(doc)

    return lista_categoria

def make_regex(col, regex):
    query = {"Data da Compra": {"$regex": f"{regex}"}}

    lista_regex = []
    for doc in col.find(query):
        lista_regex.append(doc)
    
    return lista_regex

def create_dataframe(lista):
    df =  pd.DataFrame(lista)
    return df

def format_date(df):
    if "Data da Compra" in df.columns:
        df["Data da Compra"] = pd.to_datetime(df["Data da Compra"], errors="coerce", format="%d/%m/%Y")
        df["Data da Compra"] = df["Data da Compra"].dt.strftime("%Y-%m-%d")
    else:
        print("⚠️ Aviso: Nenhum dado possui 'Data da Compra'. Verifique se essa coluna existe no MongoDB.")
        print(f"Colunas disponíveis no DataFrame: {df.columns.tolist()}")
        
def save_csv(df, path):
    df.to_csv(path, index=False)
    print(f"\nO arquivo {path} foi salvo")

if __name__ == "__main__":

    # estabelecendo a conexão e recuperando os dados do MongoDB
    client = connect_mongo(MONGO_URI)
    db = create_connect_db(client, "db_products_ch")
    col = create_connect_collection(db, "products")

    # renomeando as colunas de latitude e longitude
    rename_column(col, "lat", "Latitude")
    rename_column(col, "lon", "Longitude")

    # salvando os dados da categoria livros
    lst_livros = select_category(col, "livros")
    df_livros = create_dataframe(lst_livros)
    format_date(df_livros)
    save_csv(df_livros, "../data/tb_livros.csv")

    # salvando os dados dos produtos vendidos a partir de 2021
    lst_produtos = make_regex(col, "/202[1-9]")
    df_produtos = create_dataframe(lst_produtos)
    format_date(df_produtos)
    save_csv(df_produtos, "../data/tb_produtos_2021.csv")

    client.close()
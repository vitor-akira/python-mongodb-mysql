import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

def connect_mysql():
    cnx = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )
    print("Conectado ao MySQL!")
    return cnx

def create_cursor(cnx):
    cursor = cnx.cursor()
    return cursor

def create_database(cursor, db_name):
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")  # -> Remove o banco de dados se existir
    cursor.execute(f"CREATE DATABASE {db_name}")
    print(f"\nBase de dados {db_name} criada")

def show_databases(cursor):
    cursor.execute("SHOW DATABASES")
    for x in cursor:
        print(x)

def create_product_table(cursor, db_name, tb_name):    
    cursor.execute(f"DROP TABLE IF EXISTS {db_name}.{tb_name}")  # -> Remove a tabela se existir
    cursor.execute(f"""
        CREATE TABLE {db_name}.{tb_name}(
                id VARCHAR(100),
                Produto VARCHAR(100),
                Categoria_Produto VARCHAR(100),
                Preco FLOAT(10,2),
                Frete FLOAT(10,2),
                Data_Compra DATE,
                Vendedor VARCHAR(100),
                Local_Compra VARCHAR(100),
                Avaliacao_Compra INT,
                Tipo_Pagamento VARCHAR(100),
                Qntd_Parcelas INT,
                Latitude FLOAT(10,2),
                Longitude FLOAT(10,2),
                
                PRIMARY KEY (id));
    """)
                   
    print(f"\nTabela {tb_name} criada")

def show_tables(cursor, db_name):
    cursor.execute(f"USE {db_name}")
    cursor.execute("SHOW TABLES")
    for x in cursor:
        print(x)

def read_csv(path):
    df = pd.read_csv(path)
    return df

def add_product_data(cnx, cursor, df, db_name, tb_name):
    lista = [tuple(row) for _, row in df.iterrows()]
    sql = f"INSERT INTO {db_name}.{tb_name} VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    cursor.executemany(sql, lista)
    print(f"\n {cursor.rowcount} dados foram inseridos na tabela {tb_name}.")
    cnx.commit()

if __name__ == "__main__":
    
    # realizando a conexão com mysql
    cnx = connect_mysql()
    cursor = create_cursor(cnx)

    # criando a base de dados
    create_database(cursor, "db_produtos_teste")
    show_databases(cursor)

    # criando tabela
    create_product_table(cursor, "db_produtos_teste", "tb_livros")
    create_product_table(cursor, "db_produtos_teste", "tb_produtos_2021")
    show_tables(cursor, "db_produtos_teste")

    # lendo e adicionando os dados
    df = read_csv("../data/tb_livros.csv")
    add_product_data(cnx, cursor, df, "db_produtos_teste", "tb_livros")

    df2 = read_csv("../data/tb_produtos_2021.csv")  
    add_product_data(cnx, cursor, df2, "db_produtos_teste", "tb_produtos_2021")

    cursor.close()
    cnx.close()
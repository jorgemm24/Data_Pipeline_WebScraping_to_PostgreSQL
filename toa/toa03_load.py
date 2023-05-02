import pandas as pd
from .conn_posgres import conn_postgres_alchemy, load
#from conn_posgres import conn_postgres_alchemy, load

#pd.options.display.max_columns = None

def load_csv_to_postgresql(path:str, table:str):
    
    print("\nload.py -> def load_csv_to_postgresql")
    df = pd.read_csv(path, sep='|', dtype='unicode')
    engine = conn_postgres_alchemy()
    load(df=df, table_dest=table, engine= engine)
    

if __name__=='__main__':
    path_csv = r'D:\webscraping\data\toa\tramsformed\toa_final.csv'
    load_csv_to_postgresql(path=path_csv, table='toa')
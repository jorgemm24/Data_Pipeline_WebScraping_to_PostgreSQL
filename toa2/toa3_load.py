
import pandas as pd
from conexion_postgresql import conn_posgres as con

def load_csv_to_postgresql(path:str, table:str):
    
    print("\nload.py -> def load_csv_to_postgresql")
    df = pd.read_csv(path, sep='|', dtype='unicode')
    engine = con.conn_postgres_alchemy()
    con.load(df=df, table_dest=table, engine= engine)
    

if __name__=='__main__':
    path_csv = r'C:\CURSOS\Repositorios\Web_Scraping_pr\data\toa\tramsformed\toa_final.csv'
    load_csv_to_postgresql(path=path_csv, table='toa')
    
 
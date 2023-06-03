import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

load_dotenv()


def conn_postgres_alchemy() -> create_engine:
    """
    Función para conectarse a la base de datos destino (PostgreSQL)
    Returns:
        create_engine: Retorna el motor de conexión a PostgreSQL
    """
    try:        
        user =os.getenv('PGUSER')
        password=   os.getenv('PGPASSWORD')
        host =  os.getenv('PGHOST')
        schema = os.getenv('PGDATABASE')
        port =  os.getenv('PGPORT')       
        
        # sqlquery = "select * from API_topartists limit 10;"
        # print(create_engine.execute(sqlquery))
        engine_postgres = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{schema}")
    except Exception as e:
        print(f'Error durante conección a PostgreSQL: {e}')
    return engine_postgres


def load(df: pd.DataFrame, table_dest: str, engine: create_engine):
    """
    Función para cargar el Dataframe a la base de datos destino PostgreSQL, la función
    no retorna ningun valor.
    Nota: Los nombres de columnas y del df y la tabla desetino deben ser iguales, validar
          el formato de los registros deben aceptar la tabla destino
    Args:
        df (pd.DataFrame): Dataframe listo para cargar
        table_dest (str): Tabla destino donde se cargara el dataframe
    """
    #engine_postgres = conn_postgres_alchemy()
    try:
        #trans = engine_postgres.begin()
        with engine.begin() as trans:
            df.to_sql(table_dest,  engine, if_exists='append', index=False, chunksize=1000)
            print(f'Data cargada: {df.shape}')
        
    except Exception as e:
        trans.rollback()
        print(f'Erro durante la carga: {e}')  
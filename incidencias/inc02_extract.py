import pandas as pd
import os
#pd.options.display.max_columns = None
 

def extract(path_file: str, out_file:str):

    print()
    print('extract.py -> def extract')
    print("PROCESO CONVERTIR .xls A .CSV - INICIADO")
    
    try:
        # Eliminar el archivo .xls trabajado
        for file in files:
            if file.endswith('.xls'):
                os.remove(f'{path_file}\{file}') 
        print('Archivo .xls terminado')
    except:
        print("No hay ningun archivo .xls para eliminar")
 
    
    #Lee el archivo de path_file y lo transforma en un dataframe
    files = os.listdir(f'{path_file}')
    #print(files)
    
 
    for file in files:
        if file.endswith('.xls'):
            print(f'{path_file}\{file}')
            df = pd.read_html(f'{path_file}\{file}')       
    #print(df[0])
    
     
    #Exporta el dataframe en un archivo csv
    for i, table in enumerate(df):
        table.to_csv(f'{out_file}\\rep_incidenciascot.csv', sep=',', index=False, header=False)

    print("PROCESO CONVERTIR .xls A .CSV - TERMINADO")



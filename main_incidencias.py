from incidencias.inc01_scraping import main_scraping_inc
from incidencias.inc02_extract import extract
from incidencias.inc03_transform import transform
from incidencias.inc04_load import load_csv_to_postgresql
import time

if __name__=='__main__':
    
    inicio = time.time()
    
    # Parametros: extract
    path_file = r'D:\WebScraping\data\incidencias\raw'
    out_file = r'D:\WebScraping\data\incidencias\raw'
    
    # Parametros: transformed
    path_csv =  r'D:\WebScraping\data\incidencias\raw\rep_incidenciascot.csv'
    out_csv = r'D:\WebScraping\data\incidencias\transformed'
    period = '202304'
    
    # Parametros: load 
    path_csv_load = r'D:\webscraping\data\incidencias\transformed\data_incidencias.csv'

    # Parametros: scraping
    
    # load
    #period = '202304'
    
    # scraping
    main_scraping_inc()
    
    # extract
    extract(path_file=path_file, out_file=out_file)
    
    # transfomr
    transform(path_csv=path_csv, out_csv=out_csv, period=period)
    
    # load teradata
    load_csv_to_postgresql(path=path_csv_load, table='incidencias')
    
    fin = time.time()   
    print(f'\nTiempo total: {round(fin-inicio, 2)}')
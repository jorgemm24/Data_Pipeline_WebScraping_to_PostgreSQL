from psi.conn_posgres import conn_postgres_alchemy, load
from psi.psi01_scraping import main
from psi.psi02_transformed import transformed
from psi.psi03_load import load_csv_to_postgresql

if __name__=='__main__':
    
    # scraping
    main()
    
    # transformed
    input_folder = r'D:\webscraping\data\psi\raw'
    output_file = r'D:\webscraping\data\psi\transformed'
    transformed(input_folder=input_folder, output_file=output_file)
    
    # load
    path_csv = r'D:\webscraping\data\psi\transformed\data_psi_clean.csv'
    load_csv_to_postgresql(path=path_csv, table='psi')
    
    
    
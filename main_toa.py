from toa.conn_posgres import conn_postgres_alchemy, load
from toa.toa01_scraping import main
from toa.toa02_transform import transform
from toa.toa03_load import load_csv_to_postgresql

if __name__=='__main__':
    
    # scraping
    main()
    
    # transformed
    input_folder = r'D:\webscraping\data\toa\raw'
    output_file = r'D:\webscraping\data\toa\tramsformed'
    transform(input_folder=input_folder, output_file=output_file)
    
    # load
    path_csv = r'D:\webscraping\data\toa\tramsformed\toa_final.csv'
    load_csv_to_postgresql(path=path_csv, table='toa')
    
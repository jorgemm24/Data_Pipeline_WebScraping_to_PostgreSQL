
from toa.toa03_load import load_csv_to_postgresql

if __name__=='__main__':
    
    
    # load
    path_csv = r'C:\CURSOS\Repositorios\Web_Scraping_pr\data\toa\tramsformed\toa_final.csv'
    load_csv_to_postgresql(path=path_csv, table='toa')
    
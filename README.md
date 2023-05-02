## Proyecto Web Scraping

En este proyecto se realizaran web scraping a diferentes web y se extraera archivos 
csv y excel. Se realizara una limpieza de los archivo y sera cargado a un almacen de datos en PostgreSQL.

### Arquitectura

[![Arquitectura-Web-Scraping-to-Postgre-SQL-drawio.png](https://i.postimg.cc/XvkpLr24/Arquitectura-Web-Scraping-to-Postgre-SQL-drawio.png)](https://postimg.cc/mchL2gf5)

### Tecnologias y herramientas utilizadas:
- Python v3.9, VSCODE, PostgreSQL, DBeaver

### Explicación y Demo en Youtube
(PROXIMAMENTE)


### Pasos

1.- Primero se realiza web scraping a 3 CRM's internos para extraer archivos planos y excel. Para esto se usa Python y la lireria principal para scrapear la pagina es Selenium. El cual permirita ingresar al CRM loguearse con las credenciales, navegar por la web, realizar diferentes filtros y finalmente se exporta la información.

Todo esto es de manera automatica.

Archivos descargados: incidencias, psi, toa

2.- Una vez descargado los archivos. Se realiza la limpieza como limpieza de columnas, filtros, segmentación de datos, etc. Todo esto se realiza con python y principalmete con la libreria pandas.

3.- Finalmente la información limpia se carga a un almacen de datos en este caso se carga a PostgreSQL. Se usa python y las librerias de psycopg2 y sqlAlchemy

### Codigo - psi

##### conn_posgres.py
```python
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
        user = os.getenv('PGUSER')
        password=  os.getenv('PGPASSWORD')
        host = os.getenv('PGHOST')
        schema = os.getenv('PGDATABASE')
        port = os.getenv('PGPORT')
        
        # sqlquery = "select * from API_topartists limit 10;"
        # print(create_engine.execute(sqlquery))
        engine_postgres = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{schema}")
    except Exception as e:
        print(f'Error durante conección a PostgreSQL: {e}')
    return engine_postgres


def load(df: pd.DataFrame, table_dest: str, engine: create_engine):
    """
    Función para cargar el Dataframe a la base de datos destino PostgreSQL, la función
    no retorna ningun valor
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
```

##### psi01_scraping.py
```python
import os
import sys
import time 
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


load_dotenv()

def delete_files(path):
    for file in os.listdir(path):
        if file.endswith('.csv'):
            print(f'Eliminando: {os.path.join(path,file)}')
            os.remove(os.path.join(path,file))


def get_driver(path_download: str) -> webdriver.Chrome :
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("detach", True)
    # to supress the error messages/logs
    options.add_experimental_option("prefs",{"download.default_directory":f"{path_download}",})
    options.add_experimental_option("excludeSwitches",['enable-automation'])
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("log-level=3") # no mostrar log de alertas
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #driver.minimize_window() # FIXME:
    return driver


def scrape_page(driver ,url):
    # Open Browser
    driver.get(url)
    time.sleep(1)
    
    # Write Credentials
    user = os.getenv('user_psi')
    password = os.getenv('password_psi')
    
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.ID, "usuario"))).send_keys(user)
    driver.find_element(By.ID, value='password').send_keys(password)
    driver.find_element(By.ID, value='btnIniciar').click()  
    
    # Select 101_COT
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/aside[1]/section/ul/li[1]/a/span"))).click()
    
    # Select Bandeja de Pedidos
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/aside[1]/section/ul/li[1]/ul/li[3]/a"))).click()


def select_filters(driver):
    
    # Select 13 seleccionados
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='form_General']/div/div[1]/div[2]/div/button/span"))).click()
    
    # Desmarcar todo
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='form_General']/div/div[1]/div[2]/div/ul/li[2]/a/label"))).click()
    
    # Seleccionar Tramo 03
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='form_General']/div/div[1]/div[2]/div/ul/li[15]/a/label"))).click()
    
    # Seleccionar Boton Estado de Ticket
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='form_General']/div/div[1]/div[10]/div/button/span"))).click()

    # Seleccionar Estdo de ticket = Recepcionado
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='form_General']/div/div[1]/div[10]/div/ul/li[3]/a/label"))).click()


def select_range_dates(driver, fecha_ini, fecha_fin):
    
    # Select Rango de Fechas
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='txt_fecha_registro']"))).click()
    
    # Limpiar y Escribir Fecha Inicial
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div[1]/input"))).clear()
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div[1]/input"))).send_keys(fecha_ini)

    # Limpiar y Escribir Fecha Final
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/input"))).clear()
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/input"))).send_keys(fecha_fin)

    # Select Aplicar Rango Fechas
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/button[1]"))).click()
    
    # Select Descargar
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='form_General']/div/div[2]/div/div[2]/button"))).click()

""" 
def download_wait(path_downloads):
    dl_wait = True

    while dl_wait:
        for fname in os.listdir(path_downloads):
            if fname.endswith('.csv') and  not fname.endswith('.crdownload'):
                dl_wait = False  
    return dl_wait 
 """
 
def count_csv(path_downloads):
    #print(len(os.listdir(path_downloads)))
    files_csv = [file  for file in os.listdir(path_downloads) if file.endswith('.csv')]
    return len(files_csv)


def close_driver(driver):
    driver.close()

    
def main():
    inicio = time.time()
    
    path_download = r'D:\webscraping\data\psi\raw'
    url = os.getenv('url_psi')
    
    # Rango de Fechas (mes actual - 1)
    print()
    today_menos = datetime.now() - relativedelta(months=1) 
    month, year = today_menos.month, today_menos.year
    last_day = calendar.monthrange(year, month)[1]
    start_day, end_day = str(date(year,month,1)), str(date(year,month,last_day))
    fechaIni_1, fechaFin_1 = start_day, end_day  
    # FIXME: se puede colocar manualmente los rangos de fehcas
    print(f'Rango de fechas mes anterior: {fechaIni_1, fechaFin_1}')
     
    # Rango de Fechas (mes actual)
    now = date.today()
    month, year = now.month, now.year
    start_day = date(year,month,1)
    fechaIni_2, fechaFin_2 = str(start_day), str(now)
    # FIXME: se puede colocar manualmente los rangos de fehcas
    print(f'Rango de fechas mes actual: {fechaIni_2, fechaFin_2}')
    
    # Eliminando archivos csv
    print()
    delete_files(path=path_download)
    
    driver = get_driver(path_download=path_download)
    
    scrape_page(driver=driver ,url=url)
    select_filters(driver=driver)
    
    select_range_dates(driver, fechaIni_1, fechaFin_1)
    
    # Validar que exista un archivo CSV para que inicie la segunda descarga
    print()
    count_auxiliar = 0
    while True:
        #if  validate==False:
        nro_csv = count_csv(path_downloads=path_download) 
        if  nro_csv == 1:
            print(f'Existe un archivo csv, se empieza la segunda descarga')
            select_range_dates(driver, fechaIni_2, fechaFin_2)
            break
        if count_auxiliar>=10:
            print(f'No existen ningun archivo csv, se cierra el programa, limite superado')
            driver.close()
            sys.exit(-1)
        time.sleep(1)
        count_auxiliar+=1
    
    # Valida que exista dos archivos csv para cerrar el driver
    count_auxiliar = 0
    while True:
        nro_csv = count_csv(path_downloads=path_download)
        if  nro_csv > 1 or count_auxiliar>=10 :
            time.sleep(1)
            print(f'Existen dos archivos csv, Saliendo del programa')
            close_driver(driver=driver)
            break
        time.sleep(1)
        count_auxiliar+=1
    
    
    fin = time.time()
    print(f'\nTotal de Ejecución: {round(fin-inicio,2)}') 
    

if __name__=='__main__':
    main()
```

##### psi02_transformed.py
```python
import pandas as pd
import glob
import sys
#pd.options.display.max_columns = None

def transformed(input_folder, output_file:str):
    try:
        df = pd.concat([pd.read_csv(f, sep=',', encoding='latin-1', low_memory=False, dtype='unicode')
                            for f in glob.glob(input_folder + "\\*.csv")],ignore_index=True)

        df.columns = [x.lower().replace("?","") for x in df.columns]
        df =df.replace({',':'',r'\W':' ', '|':''})
        
        # Reemplazar vacios o fechas no validas
        df['fechaultmov'] = df['fechaultmov'].replace(' ',None)
        
        df['fecharegistrolegado'] = df['fecharegistrolegado'].replace(' ',None)
        df['fecharegistrolegado'] = df['fecharegistrolegado'].replace('0000-00-00 00:00:00',None)
        
        df['fechaliquidacion'] = df['fechaliquidacion'].replace(' ',None)
        df['fechaliquidacion'] = df['fechaliquidacion'].replace('0000-00-00 00:00:00',None)
        
        df['fecha_rellamada'] = df['fecha_rellamada'].replace(' ',None)
        df['fecha_rellamada'] = df['fecha_rellamada'].replace('0000-00-00 00:00:00',None)
        
        df['fechainigestion'] = df['fechainigestion'].replace(' ',None)
        df['fechainigestion'] = df['fechainigestion'].replace('0000-00-00 00:00:00',None)
        
        df['fechaasignacionusuario'] = df['fechaasignacionusuario'].replace(' ',None)
        df['fechaasignacionusuario'] = df['fechaasignacionusuario'].replace('0000-00-00 00:00:00',None)
    
        # transformar object a datetime
        df['fecharegistro']= pd.to_datetime(df['fecharegistro'], format='%d-%m-%y %H:%M:%S')
        df['fechaultmov']= pd.to_datetime(df['fechaultmov'], format='%Y-%m-%d %H:%M:%S')
        df['fecharegistrolegado']= pd.to_datetime(df['fecharegistrolegado'], format='%Y-%m-%d %H:%M:%S')
        df['fechaliquidacion']= pd.to_datetime(df['fechaliquidacion'], format='%Y-%m-%d %H:%M:%S')
        df['fecha_rellamada']= pd.to_datetime(df['fecha_rellamada'], format='%Y-%m-%d %H:%M:%S')
        df['fechainigestion']= pd.to_datetime(df['fechainigestion'], format='%Y-%m-%d %H:%M:%S')
        df['fechaasignacionusuario']= pd.to_datetime(df['fechaasignacionusuario'], format='%Y-%m-%d %H:%M:%S')
        df['fh_reg104']= pd.to_datetime(df['fh_reg104'],errors='coerce')
        df['fh_reg1l']= pd.to_datetime(df['fh_reg1l'],errors='coerce')
        df['fh_reg2l']= pd.to_datetime(df['fh_reg2l'],errors='coerce')
    except Exception as e:
        print(f'Error durante la transformación: {e}')
        sys.exit(-1)
    
    print('\nExportando CSV')
    df.to_csv(f'{output_file}\\data_psi_clean.csv', sep='|', index=False, encoding='utf-8')
    

if __name__=='__main__':
    
    input_folder = r'D:\webscraping\data\psi\raw'
    output_file = r'D:\webscraping\data\psi\transformed'
    
    transformed(input_folder=input_folder, output_file=output_file )
```

##### psi03_load.py
```python
import pandas as pd
from .conn_posgres import conn_postgres_alchemy, load
#from conn_posgres import conn_postgres_alchemy, load

#pd.options.display.max_columns = None

def load_csv_to_postgresql(path:str, table:str):
    
    print("\nload.py -> def load_csv_to_postgresql")
    df = pd.read_csv(path, sep='|', dtype='unicode')
    df.columns = [x.lower().replace("?","") for x in df.columns]
    engine = conn_postgres_alchemy()
    load(df=df, table_dest=table, engine= engine)
    

if __name__=='__main__':
    path_csv = r'D:\webscraping\data\psi\transformed\data_psi_clean.csv'
    load_csv_to_postgresql(path=path_csv, table='psi')
```

##### main_psi.py
```python
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
```

### Contacto:
ztejorge@hotmail.com


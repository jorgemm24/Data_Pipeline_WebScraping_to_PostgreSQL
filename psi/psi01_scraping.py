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
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
import keyboard

load_dotenv()

def delete_files(path):
    for file in os.listdir(path):
        if file.endswith('.csv'):
            print(f'Eliminando: {os.path.join(path,file)}')
            os.remove(os.path.join(path,file))

def get_driver(path_download: str) -> webdriver.Chrome :
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches",['enable-automation'])
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("log-level=3") # no mostrar log de alertas
    
    options.add_experimental_option("prefs",{ "download.default_directory":f"{path_download}"
                                              ,"download.prompt_for_download":False  #True 
                                              ,"download.directory_upgrade"  : False   #True  
                                             }
                                    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #driver.minimize_window() # FIXME:
    return driver


def input_credencitals(driver ,url, user, password):
    # Open Browser
    driver.get(url)
    
    # Credentials
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(user)
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sign-in']/div"))).click()
    time.sleep(5)
   

def close_another_session(driver, password):
    
    """Este proceso se realiza cuando, se supero el limite de sesiones
    """
    
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.ID, "del-oldest-session"))).click()
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sign-in']/div"))).click()


def wait_page(driver):
    driver.refresh()    
    

def select_filters(driver):
    
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "app-button.app-button--borderless.app-button--transparent")))
    print("SELECT FECHA ANTERIOR")
    date_prev = driver.find_elements(By.CLASS_NAME, value="app-button.app-button--icon-only.app-button--ghost.app-button--transparent")
    for i in date_prev:
        if i.get_attribute('aria-label') == 'Anterior':
            print("ENCONTRADO -> CLICK ANTERIOR")
            i.click()
            break
    
    
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "app-button.app-button--borderless.app-button--transparent")))
    time.sleep(1)
    print("SELECT VISTA")
    botton = driver.find_elements(By.CLASS_NAME, value= "app-button.app-button--borderless.app-button--transparent")
    time.sleep(1)
    for i in botton:
        #print(i)
        if i.get_attribute('aria-label') == 'Vista':
            print("ENCONTRADO -> CLICK VISTA")
            i.click()
            break
        

    print("\nSELECT TODOS LOS HIJOS")
    select = driver.find_elements(By.CLASS_NAME, value= "oj-radiocheckbox-label-text")
    for i in select:
        if i.text =='Todos los datos de hijos':
            print('ENCONTRADO -> CLICK Todos los datos de hijos')
            i.click()
            break
        
    time.sleep(1)
    print("\nSELECT APLICAR")
    botton_aplicar= driver.find_elements(By.CLASS_NAME, value="app-button-title")
    for i in botton_aplicar:
        if i.text == 'Aplicar':
            print('ENCONTRADO, CLICK APLICAR')
            i.click()
            break
    
    
    time.sleep(1)
    print("\nSELECT ACCIONES")
    acciones = driver.find_elements(By.CLASS_NAME, value= "app-button.app-button--borderless.app-button--transparent")
    for i in acciones:
        if i.get_attribute('aria-label') == 'Acciones':
            print('ENCONTRADO, CLICK ACCIONES')
            i.click()
            break
    
    time.sleep(0.5)
    print("\nSELECT EXPORTAR")
    botton_aplicar= driver.find_elements(By.CLASS_NAME, value="toolbar-menu-button-title")
    for i in botton_aplicar:
        if i.text == 'Exportar':
            print('ENCONTRADO, CLICK EXPORTAR')
            i.click()
            break  
    
    time.sleep(1)
 

def count_csv(path_downloads):
    files_csv = [file  for file in os.listdir(path_downloads) if file.endswith('.csv')]
    return len(files_csv)


def close_sesion(driver):
    
    print("SELECT USER MENU")
    time.sleep(1)
    user_menu = driver.find_elements(By.CLASS_NAME, value= "user-menu")
    for i in user_menu:
        if  i.get_attribute('aria-label') == '582485-INDRA-MAMANI MENDOZA JORGE LUIS':
            print('ENCONTRADO, CLICK USER-MENU')
            i.click()
            break   
    print()    
    print("SELECT CERRAR SESION")

    cerrar_sesion = driver.find_elements(By.CLASS_NAME, value= "item-caption.item-caption--logout") # si existe un espacio reemplazar por .
    for i in cerrar_sesion:
        if  i.text == 'Cerrar sesión':
            print('ENCONTRADO, CLICK CERRAR SESION')
            i.click()
            time.sleep(2)
            break
    
def close_driver(driver):
    try:
        WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.ID, "password")))
        user = driver.find_element(By.ID, value='username')
        if user.get_attribute('aria-label')=='Nombre de usuario':
            driver.close()
    except:
        driver.close()


def main():
    inicio = time.time()
    
    path_download = r'D:\webscraping\data\toa\raw'
    
    url = os.getenv('url_toa')
    user = os.getenv('user_toa')
    password = os.getenv('password_toa')
    
    delete_files(path=path_download)
    
    driver = get_driver(path_download)
    time.sleep(5)
    
    try:
        input_credencitals(driver ,url, user, password )
    except:
        close_another_session(driver, password)
    
    print("PRIMER REFRESH")
    driver.refresh()
    time.sleep(4)
    print("SEGUNDO REFRESH")
    driver.refresh()
    time.sleep(4)

    print()
    print("PAGINA CARGADA CORRECETAMENTE???????")
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'app-button.app-button--borderless.app-button--transparent')))
            print("PAGINA LISTA")
            time.sleep(1)
            break
        except :
            print("REFRESCANDO LA PAGINA")
            driver.refresh()
            time.sleep(5)
            driver.refresh()
            time.sleep(5)
    
    print()
    select_filters(driver)
        
    # Valida que exista un archivo CSV para que inicie la segunda descarga
    print()
    
    count_auxiliar = 0
    while True:
        nro_csv = count_csv(path_downloads=path_download) 
        if  nro_csv >= 1:
            print(f'Se completo la descarga CSV, se cierra la sesión')
            time.sleep(1)
            close_sesion(driver)
            time.sleep(1)
            break
        
        if count_auxiliar>=360:
            print(f'No existen ningun archivo csv, se cierra el programa, limite superado')
            close_sesion(driver)
            driver.close()
            sys.exit(-1)
        time.sleep(1)
        count_auxiliar+=1
    
    print()
    print('CERRANDO DRIVER')
    close_driver(driver)
    
    fin = time.time()
    print(f'\nTotal de Ejecución: {round(fin-inicio,2)}') 
    
if __name__=='__main__':
    main()
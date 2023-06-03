import os
import sys
import time 
import shutil
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
#import keyboard

load_dotenv()


def delete_files(path):
    for file in os.listdir(path):
        if file.endswith('.csv') or file.endswith('.crdownload'):    
            print(f'Eliminando: {os.path.join(path,file)}')
            os.remove(os.path.join(path,file))

def get_driver(path_download: str) -> webdriver.Chrome :
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("detach", True)
    # to supress the error messages/logs
    #options.add_exp
    # erimental_option('excludeSwitches', ['enable-logging'])
    
    options.add_experimental_option("excludeSwitches",['enable-automation'])
    #options.add_argument('--no-sandbox')
    #options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    #options.add_argument("--headless")
    options.add_argument("log-level=3") # no mostrar log de alertas
    
    

    
    options.add_experimental_option("prefs",{ "download.default_directory":f"{path_download}"
                                              ,"download.prompt_for_download":False  #True 
                                              ,"download.directory_upgrade"  : False   #True  
                                             }
                                    )

    #options.add_experimental_option('prefs', prefs)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #driver.minimize_window() # FIXME:
    return driver


def input_credencitals(driver ,url, user, password):
    # Open Browser
    driver.get(url)
    
    # Credentials
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(user)
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
    #time.sleep(3)
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sign-in']/div"))).click()
    time.sleep(5)
    
    
    print("\nPRIMER REFRESH")
    driver.refresh()
    time.sleep(4)
    print("SEGUNDO REFRESH")
    driver.refresh()
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'app-button.app-button--borderless.app-button--transparent')))
    
   
    
    
def close_another_session(driver:webdriver.Chrome, password):
    
    """Este proceso se realiza cuando, se supero el limite de sesiones
    """
    url = 'https://telefonica-pe.etadirect.com/mobility/'
    
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.ID, "del-oldest-session"))).click()
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='sign-in']/div"))).click()
    #time.sleep(5) 


def wait_page(driver:webdriver.Chrome):
    driver.refresh()    
    
    
def select_vista(driver:webdriver.Chrome):
    #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "app-button.app-button--borderless.app-button--transparent")))
    time.sleep(1)
    print("\nSELECT VISTA")
    botton = driver.find_elements(By.CLASS_NAME, value= "app-button.app-button--borderless.app-button--transparent")
    time.sleep(1)
    for i in botton:
        #print(i)
        if i.get_attribute('aria-label') == 'Vista':
            print("ENCONTRADO -> CLICK VISTA")
            i.click()
            break
        

    print("SELECT TODOS LOS HIJOS")
    select = driver.find_elements(By.CLASS_NAME, value= "oj-radiocheckbox-label-text")
    for i in select:
        if i.text =='Todos los datos de hijos':
            print('ENCONTRADO -> CLICK Todos los datos de hijos')
            i.click()
            break
        
    time.sleep(1)
    print("SELECT APLICAR")
    botton_aplicar= driver.find_elements(By.CLASS_NAME, value="app-button-title")
    for i in botton_aplicar:
        if i.text == 'Aplicar':
            print('ENCONTRADO, CLICK APLICAR')
            i.click()
            break
    
        
        
        
def acciones_exportar(driver:webdriver.Chrome):
    time.sleep(1)
    print("\nSELECT ACCIONES")
    acciones = driver.find_elements(By.CLASS_NAME, value= "app-button.app-button--borderless.app-button--transparent")
    for i in acciones:
        if i.get_attribute('aria-label') == 'Acciones':
            print('ENCONTRADO, CLICK ACCIONES')
            i.click()
            break
    
    time.sleep(0.5)
    print("SELECT EXPORTAR")
    botton_aplicar= driver.find_elements(By.CLASS_NAME, value="toolbar-menu-button-title")
    for i in botton_aplicar:
        if i.text == 'Exportar':
            print('ENCONTRADO, CLICK EXPORTAR')
            i.click()
            break  
    
    time.sleep(1)
         

def select_anterior(driver:webdriver.Chrome):

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "app-button.app-button--borderless.app-button--transparent")))
    #time.sleep(5)
    print("SELECT FECHA ANTERIOR")
    date_prev = driver.find_elements(By.CLASS_NAME, value="app-button.app-button--icon-only.app-button--ghost.app-button--transparent")
    for i in date_prev:
        if i.get_attribute('aria-label') == 'Anterior':
            print("ENCONTRADO -> CLICK ANTERIOR")
            i.click()
            time.sleep(2)
            break
    

def move_files(input_path:str, out_path:str):
    """Copiando archivos de origen a historico
    """
    try:
        for file in os.listdir(input_path):
            source = f'{input_path}\\{file}'
            out = f'{out_path}\\{file}'
            #print(f'Copiando -> {out_path}\\{file}')
            shutil.move(source, out)  
            #os.system(f'copy {source} {out}')    
    except Exception as e:
        print(f"Error durante la copia al directorio historico: {e}")  
      

def count_csv(path_downloads):
    files_csv = [file  for file in os.listdir(path_downloads) if file.endswith('.csv')]
    return len(files_csv)


def close_sesion(driver:webdriver.Chrome):
    
    #time.sleep(20) # cambiar por un validate
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
    #time.sleep(2)
    cerrar_sesion = driver.find_elements(By.CLASS_NAME, value= "item-caption.item-caption--logout") # si existe un espacio reemplazar por .
    for i in cerrar_sesion:
        #time.sleep(1)
        if  i.text == 'Cerrar sesión':
            print('ENCONTRADO, CLICK CERRAR SESION')
            #time.sleep(1)
            i.click()
            time.sleep(2)
            break
  
    
def close_driver(driver:webdriver.Chrome):
    try:
        WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.ID, "password")))
        user = driver.find_element(By.ID, value='username')
        if user.get_attribute('aria-label')=='Nombre de usuario':
            driver.close()
    except:
        driver.close()


def main_toa():
    inicio = time.time()
    
    temp_path = r'C:\CURSOS\Datasets\Directorio_temp'
    input_path = r'C:\CURSOS\Datasets\Fuente_origen'
    
    user, password, url = os.getenv('user_toa'), os.getenv('password_toa'), os.getenv('url_toa')
    
    delete_files(path=temp_path)
    
    driver = get_driver(temp_path)
    time.sleep(5)
    
    try:
        input_credencitals(driver ,url, user, password )
    except:
        close_another_session(driver, password)
    
    
    select_vista(driver=driver)
    acciones_exportar(driver=driver)
    
    
    print('\nDESCARGANDO PRIMER CSV')
    count_auxiliar = 0
    while True:
        nro_csv = count_csv(path_downloads=temp_path) 
        if  nro_csv >= 1:
            print(f'SE COMPLETO LA DESCARGA CSV, MOVIENDO ARCHIVO')
            time.sleep(1)
            move_files(input_path=temp_path, out_path=input_path)
            time.sleep(1)
            count_auxiliar=0
            break
        
        if count_auxiliar>=360:
            print(f'NO EXISTE NINGUN ARCHIVO CSV, SE CIERRA EL PROGRAMA, LIMITE SUPERADO')
            close_sesion(driver)
            driver.close()
            sys.exit(-1)
        time.sleep(1)
        count_auxiliar+=1
        
    
    print('\nDESCARGANDO ARCHIVOS RESTANTES')
    contador_anterior = 0
    count_auxiliar = 0   # TIEMPO SEGUNDOS DE DESCARGA
    select_anterior(driver=driver)
    acciones_exportar(driver=driver)
    while contador_anterior<=14:
        nro_csv = count_csv(path_downloads=temp_path) 
        if  nro_csv >= 1:
            print(f'SE COMPLETO LA DESCARGA CSV {contador_anterior+1}, MOVIENDO ARCHIVO')
            time.sleep(1)
            move_files(input_path=temp_path, out_path=input_path)
            time.sleep(1)
            count_auxiliar=0
            nro_csv=0
            
            contador_anterior +=1
            if contador_anterior==14:
                break

            select_anterior(driver=driver)
            acciones_exportar(driver=driver)
       
        if count_auxiliar>=360:
            print(f'NO EXISTE NINGUN ARCHIVO CSV, SE CIERRA EL PROGRAMA, LIMITE SUPERADO')
            close_sesion(driver)
            driver.close()
            sys.exit(-1)
        
        time.sleep(1)   
        count_auxiliar+=1
        
    print('\nCERRANDO SESIÓN')
    close_sesion(driver=driver)
        
    print('\nCERRANDO DRIVER')
    #time.sleep(1)
    close_driver(driver=driver)
    
    fin = time.time()
    print(f'\nTotal de Ejecución: {round(fin-inicio,2)}') 
    

    
if __name__=='__main__':
    main_toa()
    
    
    
   
import os
from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

load_dotenv()


def delete_xls_path(path:str, extension:str):
    for file in os.listdir(path):
        if file.endswith(extension):
            print(f'Eliminando: {os.path.join(path,file)}')
            os.remove(os.path.join(path,file))
            

def get_driver(path_download):
    
    options = Options()
    options.add_argument("start-maximized")
    # to supress the error messages/logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("prefs",{"download.default_directory":f"{path_download}",})
    options.add_experimental_option("excludeSwitches",['enable-automation'])
    options.add_argument("log-level=3") # no mostrar log de alertas
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #driver.minimize_window() # FIXME:
    return driver


def switch_to_ifrmae(driver , url):
    driver.get(url)
    print()
    print("Pagina:  : %s" %driver.title)

    # select Incidencias
    inc =  driver.find_element(by=By.XPATH, value= "//tbody/tr[1]/td[3]/img[1]")
    inc.click()
    print('OK -> Select Incidencias')

    # switch_to ifrmae
    driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/table/tbody/tr[6]/td[2]/div[2]/iframe"))
    print("OK -> driver.switch_to.frame")
    sleep(3)


def select_date_ini(driver ,day_i:str ,month_i:str ,year_i:str):
    # clear day
    day = driver.find_element(By.ID,value="dia_i")
    day.clear()
    print("OK -> Clear textbot dia_i")
    day.send_keys(day_i)

    # select month
    select_month = Select(driver.find_element(By.XPATH, value="//*[@id='mes_i']"))
    select_month.select_by_value(month_i)

    # select year
    select_year = Select(driver.find_element(By.ID, value="an_i"))
    select_year.select_by_value(year_i)


def select_date_fin(driver, day_f:str, month_f:str, year_f:str ):
    # clear day
    day = driver.find_element(By.ID,value="dia_f")
    day.clear()
    print("OK -> Clear textbot dia_f")
    day.send_keys(day_f)

    # select month
    select_month = Select(driver.find_element(By.XPATH, value="//*[@id='mes_f']"))
    select_month.select_by_value(month_f)

    # select year
    select_year = Select(driver.find_element(By.ID, value="an_f"))
    select_year.select_by_value(year_f)

def export_file(driver):
    print("Export File")
    sleep(1)
    export = driver.find_element(By.XPATH, value="/html/body/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td[5]")
    export.click()
    #driver.minimize_window() # FIXME:
    
    
def download_wait(path_to_downloads):
    dl_wait = True
    #while dl_wait and seconds < 5:
    while dl_wait:
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.xls') and  not fname.endswith('.crdownload'):
                dl_wait = False
                sleep(1)
        #seconds += 1
    return dl_wait


def driver_close(driver):
    print('Cerrando WebDriver')
    sleep(1)
    driver.close()


def main_scraping_inc():
    # Parametros
    path_download = r'D:\WebScraping\data\incidencias\raw'
    url =  os.getenv('url_inc')
    # siempre se filtra 10 dias antes y 10 dias despues del mes en curso
    # TODO: parametrizar automaticamente
    day_i, month_i ,year_i = '20', '03', '2023'
    day_f, month_f ,year_f = '10', '05', '2023'
    
    # delete file
    delete_xls_path(path=path_download, extension='.xls')
    
    # Scraping
    driver = get_driver(path_download)
    switch_to_ifrmae(driver=driver, url=url)
    select_date_ini(driver=driver ,day_i=day_i ,month_i=month_i ,year_i=year_i)
    select_date_fin(driver=driver, day_f=day_f, month_f=month_f ,year_f=year_f)
    export_file(driver=driver)
    
    validate = download_wait(path_to_downloads=path_download)    

    if validate==False:
        driver_close(driver=driver)
        
    print()
    

if __name__=='__main__':
    main_scraping_inc()
    

    
    









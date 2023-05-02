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
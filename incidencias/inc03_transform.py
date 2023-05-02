import pandas as pd
import sys
#pd.options.display.max_columns = None


def transform(path_csv, out_csv, period):
    
    print()
    print('transform.py -> def transform')
    path_csv = path_csv

    df = pd.read_csv(path_csv, dtype='unicode', encoding='utf-8')

    df.rename(columns = {'GESTOR COT':'Gestor_COT', 'FECHA REGISTRO':'FechaRegistro', 'C.INDICENCIA':'CodIncidencia', 'TP.INCIDENCIA':'TPIncidencia', 'MOTIVO':'Motivo'
                        ,'FEC.INICIO':'FechaInicio' ,'FEC.FIN':'FechaFin', 'DOID':'DOID', 'REGISTRADO POR':'Registrado_Por','MODO':'Modo', 'OBSERVACION':'Observacion'}, inplace = True)

    print(f'REGISTROS ORIGINALES: {df.shape}')

    try:
        df['Fecha']= pd.to_datetime(df['FechaInicio'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%d')
        df['Periodo_temp']= pd.to_datetime(df['FechaInicio'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%Y%m')
    except Exception as e:
        print(f'Error durante la transformación de la fecha {e}, casteando con otro formato')
        sys.exit(-1) # FIXME: CAmbiarlo por el formato
        # colocar otro formato de fecha si es necesario
      

    df = df[df['Periodo_temp']==period]


    #df['Fecha']= pd.to_datetime(df['FechaInicio'], format='%Y-%m-%d')
    #df['Fecha']= pd.to_datetime(df['FechaInicio'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%d')
    df["DOID"].fillna("?", inplace = True)
    df['FechaInicio'] = df['FechaInicio'].astype('datetime64[ns]')
    df['FechaFin'] = df['FechaFin'].astype('datetime64[ns]')
    df['DNI'] = df['DNI'].astype(str).str.zfill(8)

    ## 
    #df["DI"] = (df['FechaFin'] - df['FechaInicio'])/pd.Timedelta('1 hour')
    #df["DI2"] = (df['FechaFin'] - df['FechaInicio'])/pd.Timedelta('1 seconds')
    df["Tiempo_Incidencias_Minutos"] = (df['FechaFin'] - df['FechaInicio'])/pd.Timedelta('1 minutes')
    #df["Tiempo_Incidencias_Minutos"] = df["Tiempo_Incidencias_Segundos"]/60.00
    df['Tiempo_Incidencias_Formato'] = pd.to_datetime(df["Tiempo_Incidencias_Minutos"], unit='m').dt.strftime("%H:%M:%S")


    df = df.loc[:,['DNI', 'Gestor_COT', 'FechaRegistro','CodIncidencia','TPIncidencia','Motivo','Fecha','FechaInicio','FechaFin','DOID',\
                'Registrado_Por','Modo','Tiempo_Incidencias_Formato','Tiempo_Incidencias_Minutos','Observacion']]

    df[['FechaInicio','FechaFin','Tiempo_Incidencias_Minutos']] = df[['FechaInicio','FechaFin','Tiempo_Incidencias_Minutos']].astype(str)

    df.columns = [x.lower().replace("?","") for x in df.columns]
    
    print(f'REGISTROS PERIODO EN CURSO: {df.shape}')
    
    out_csv = out_csv
    df.to_csv(f'{out_csv}\\data_incidencias.csv',index=False, sep='|', encoding='utf-8')

    



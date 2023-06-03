import sys
import glob
import pandas as pd
#pd.options.display.max_columns = None


def funcion_fecha_toa(x):
    return str(x)[0:16]

def funcion_fecha_registro(x):
    if len(str(x))==16: 
        return str(x)+':'+'00'
    else:
        return str(x)


def transform(input_file: str, output_file:str ) -> None:

    print('PROCESO DE TRANSFORMACIÓN')
    all_files =  [i for i in glob.glob(f'{input_file}\*csv')]
    df = pd.concat([pd.read_csv(f, dtype='unicode', sep=',', encoding='utf-8' ) for f in all_files])
    #print(df.head(1))

    
    # seleccionando columnas
    columnas = [
        'Técnico',
        'Número OT',
        'Subtipo de Actividad',
        'Número de Petición',
        'Fecha de Cita',
        'SLA Inicio',
        'SLA Fin',
        'Localidad',
        'Dirección',
        'Clave Zona de Trabajo',
        'Nombre Cliente',
        'Estado actividad',
        'Categoría de Capacidad',
        'Fecha de Registro Legados',
        'Tipo de Devolución Instalaciones',
        'Motivo no realizado instalación',
        'Usuario',
        'Tipo de Cita',
        'Código de Requerimiento',
        'Orden trabajo',
        'Hora inicio actividad',
        'Hora fin',
        'Motivo no realizado',
        'Código de Cliente',
        'Observaciones en TOA', 
        'Fecha Hora de Cancelación',
        'Hora planificada de inicio de actividad ',
        'Empresa',
        'Bucket Inicial',
        'Fecha Registro de Actividad en TOA',
        'Tipo de Devolución COT',
        'Motivo No Realizado Instalación COT',
        'Usuario de No Realizado Técnico',
        'Hora de Pre No Realizado Técnico',
        'Motivo No Realizado Instalación Temático',
        'Teléfono de contacto 1',
        'Nombre Distrito',
        'MDF',
        'Armario',
        'Tipo de Tecnología Legados',
        'Tematico 1 - Prueba',
        'Tematico 2 - Prueba',
        'Tematico 3 - Prueba',
        'Nodo',
        'Troba',
        'Tipo de cliente',
        'Sub Tipo de Cliente',
        'Nombre de Provincia',
        'Documento de Identidad',
        'Departamento',
        'Teléfono de contacto 2',
        'Teléfono de contacto 3',
        'Teléfono Contacto 3',
        'Teléfono Contacto 2',
        'Teléfono Contacto 4',
        'Teléfono Contacto 5',
        'Telefono de Contacto',
        'Fecha de registro del caso',
        'Prioridad'
    ]

    # seleccionando columnas
    df = df[[*columnas]] 


    # Renombrar Columnas
    df.rename(columns={
        'Técnico':  'Tecnico',
        'Número OT':  'Num_OT',
        'Subtipo de Actividad':  'Subtipo_activ',
        'Número de Petición':  'Num_Peticion',
        'Fecha de Cita':  'Fec_Cita',
        'SLA Inicio':  'SLA_ini',
        'SLA Fin':  'SLA_Fin',
        'Localidad':  'Localidad',
        'Dirección':  'Direccion',   # ya estaba
        'Clave Zona de Trabajo':'Clave_Zona_Trabajo',  # add
        'Nombre Cliente':'Nombre_Cliente', # add
        'Estado actividad':  'Est_activ',   # ya estaba
        'Categoría de Capacidad':  'Categ_Capacidad',
        'Fecha de Registro Legados':  'Fec_reg_Legados',
        'Tipo de Devolución Instalaciones':  'Tipo_devol_Instal',
        'Motivo no realizado instalación':  'Mot_no_Real_instal', # ya estaba
        'Usuario':  'Usuario',
        'Tipo de Cita':  'Tipo_Cita',
        'Código de Requerimiento':  'Cod_Req',
        'Orden trabajo':  'Orden_trabajo',
        'Hora inicio actividad':  'Hora_ini_activ',
        'Hora fin':  'Hora_fin',
        'Motivo no realizado':  'Mot_no_Real',
        'Código de Cliente':  'Cod_Cliente',
        'Observaciones en TOA':'Observaciones_en_TOA',  # add
        'Fecha Hora de Cancelación':  'Fec_Hora_Canc',   # ya estaba
        'Hora planificada de inicio de actividad ':  'Hora_plan_ini_activ',
        'Empresa':  'Empresa',
        'Bucket Inicial':'Bucket_Inicial', # add
        'Fecha Registro de Actividad en TOA':  'Fec_reg_Activ_TOA',
        'Tipo de Devolución COT':  'Tipo_devol_COT',
        'Motivo No Realizado Instalación COT':  'Mot_No_Real_Instal_COT',
        'Usuario de No Realizado Técnico':  'Usu_No_Real_Tec',
        'Hora de Pre No Realizado Técnico':  'Hora_Pre_No_Real_Tec',
        'Motivo No Realizado Instalación Temático':  'Mot_No_Instal_Tema',
        'Teléfono de contacto 1':  'Tel_contacto_1',
        'Nombre Distrito':  'Nombre_Distrito',
        'MDF':  'MDF',
        'Armario':  'Armario',
        'Tipo de Tecnología Legados':  'Tipo_Tec_Legados', # ya estaba
        'Tematico 1 - Prueba':  'Tema_1_Prueba',
        'Tematico 2 - Prueba':  'Tema_2_Prueba',
        'Tematico 3 - Prueba':  'Tema_3_Prueba',
        'Nodo':  'Nodo',
        'Troba':  'Troba',
        'Tipo de cliente':  'Tipo_cliente',
        'Sub Tipo de Cliente':  'Sub_Tipo_Cliente',
        'Nombre de Provincia':  'Provincia',
        'Documento de Identidad':'Documento_Identidad', # add
        'Departamento':  'Departamento',
        'Teléfono de contacto 2':  'Telefono_contac2',
        'Teléfono de contacto 3':  'Telefono_contac3',
        'Teléfono Contacto 3':  'Tel_Contacto_3',
        'Teléfono Contacto 2':  'Tel_Contacto_2',
        'Teléfono Contacto 4':  'Tel_Contacto_4',
        'Teléfono Contacto 5':  'Tel_Contacto_5',
        'Telefono de Contacto':  'Tel_Contacto',
        'Fecha de registro del caso':  'Fecha_registro',
        'Prioridad':  'Prioridad'
    }, inplace=True
    )

    #print(df.head(5))


    # Reemplzar caracteres
    #df =df.replace({',':'',r'\W':' '})
    df = df.replace(',',' ', regex=True)

    #for fecha in df.Fec_reg_Activ_TOA.unique():
    #    print(fecha)

    #df['Fec_reg_Activ_TOA'] = df['Fec_reg_Activ_TOA'].apply(funcion_fecha_toa)
    df['Fec_reg_Activ_TOA'] = df['Fec_reg_Activ_TOA'].apply(lambda x: str(x)[0:16])
    #df['Fecha_registro'] = df['Fecha_registro'].apply(funcion_fecha_registro)
    df['Fecha_registro'] = df['Fecha_registro'].apply(lambda x: str(x)+':'+'00' if(len(str(x))==16) else str(x) )
    

    
    
    #for fecha in df.Fecha_registro.unique():
    #    print(fecha)
    #lambda a : True if (a > 10 and a < 20) else False

    try:
        print('\nCASTEO FECHAS')
        df["Fec_Cita"] =  pd.to_datetime(df["Fec_Cita"], format="%d/%m/%y")
        df['SLA_ini'] =  pd.to_datetime(df["SLA_ini"], format="%d/%m/%y %H:%M %p")
        df['SLA_Fin'] =  pd.to_datetime(df["SLA_Fin"], format="%d/%m/%y %H:%M %p")
        df['Fec_reg_Legados'] =  pd.to_datetime(df["Fec_reg_Legados"], format="%d/%m/%y %H:%M %p")

        df['Fec_Hora_Canc'] =  pd.to_datetime(df["Fec_Hora_Canc"], format="%Y-%m-%d %H:%M")  #
        df['Fec_reg_Activ_TOA'] =  pd.to_datetime(df["Fec_reg_Activ_TOA"], format="%Y-%m-%d %H:%M")
        df['Hora_Pre_No_Real_Tec'] =  pd.to_datetime(df["Hora_Pre_No_Real_Tec"], format="%Y-%m-%d %H:%M")

        df['Fecha_registro'] =  pd.to_datetime(df["Fecha_registro"], format="%Y-%m-%dT%H:%M:%S")
        
        #df['Hora_ini_activ'] = df['Hora_ini_activ'].dt.strftime('%I:%M %p')
        df['Hora_ini_activ'] = pd.to_datetime(df['Hora_ini_activ'], format='%H:%M %p')
        df['Hora_fin'] = pd.to_datetime(df['Hora_fin'], format='%H:%M %p')   # FORMATO 
        
        df['Hora_plan_ini_activ'] = pd.to_datetime(df['Hora_plan_ini_activ'], format='%H:%M')
        

        # Hora_ini_activ   08:47 AM
        # Hora_fin         12:41 PM
        
        #print(df.head(5))
        #print(df['Fec_Hora_Canc'].unique())
        #print(df.Fec_reg_Activ_TOA.unique())
        
        #for fecha in df.Fec_reg_Activ_TOA.unique():
        #    print(fecha)
        
        #print(df.Hora_fin.unique())
    
    except Exception as e:
        print(f"ERROR DURANTE EL CASTEO DE FECHAS {e}")
        sys.exit(-1)
       
    #print(df.head(5))   
        
    
    # Export CSV   
    try:
        df.to_csv(output_file,index=False,encoding='utf-8-sig') # si fallta cambiarlo por utf-8
    except Exception as e:
        print(f"Error en exportar en latin-1, se exportara en utf-8 -> {e}" )
        df.to_csv(output_file,index=False,encoding='latin-1') 

    

if __name__=='__main__':
    
    input_file = r'C:\CURSOS\Datasets\Fuente_origen'
    output_file = r'C:\CURSOS\Datasets\ToaConsolidado\consolidadoToa.csv'

    transform(input_file=input_file , output_file=output_file)

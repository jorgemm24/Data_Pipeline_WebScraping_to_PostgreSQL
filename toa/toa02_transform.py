import pandas as pd
import sys
import glob
#pd.options.display.max_columns = None


def transform(input_folder: str, output_file):
    print('\nTransformado datos')
    try:
        df = pd.concat([pd.read_csv(f, sep=',', encoding='utf-8', low_memory=False, dtype='unicode')
                                for f in glob.glob(input_folder + "\\*.csv")],ignore_index=True)
        
        # Replace symbols columns
        df.columns = [x.lower().replace(" ","_").replace('á','a').replace('é','e').replace('í','i')
                    .replace('ó','o').replace('ú','u').replace('?','').replace('(','').replace(')','')
                    .replace('/','').replace('.','_').replace('-','') for x in df.columns]
        
        print(df.shape)
        
        # Replace symbols
        df =df.replace({',':' ',r'\W':' ', '|':' '})
        
        # select columns
        df = df.iloc[:, 0:50]
        print(df.shape)
        #print(df.head(5))
        
        print('Exportando a CSV')
        df.to_csv(f'{output_file}\\toa_final.csv' , sep='|' , encoding='utf-8', index=False)
    except Exception as e:
        print(f'Error durante la transformación {e}')
        sys.exit(-1)
    


if __name__=='__main__':
    input_folder = r'D:\webscraping\data\toa\raw'
    output_file = r'D:\webscraping\data\toa\tramsformed'
    
    transform(input_folder=input_folder, output_file=output_file)

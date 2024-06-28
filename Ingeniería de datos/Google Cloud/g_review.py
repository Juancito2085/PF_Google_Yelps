import pandas as pd
import datetime

df=pd.read_json(r'E:\Data Science\PF\Datasets\Google Maps\reviews-estados\review-California\1.json', lines=True)
def transform_reviews(df):
    
    #Eliminamos las columnas que no nos interesan
    df.drop(columns=['pics','resp'],inplace=True)

    #Reordenamos las columnas 
    df=df[['gmap_id','name','rating','time','text']]

    #Modificamos la columna time para tener fecha
    df['time']=pd.to_datetime(df['time'], unit='ms')
    df['time']=pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
    df['time'] = df['time'].dt.floor('S') 
    
    #Nos quedamos con las reviews de los años 2016 a 2021
    df=df[(df['time'].dt.year>=2016) & (df['time'].dt.year<=2021)]
    return df

'''def leer_parquet(event, context):
    bucket = event["bucket"]
    name = event["name"]
    #df = pd.read_parquet(f'gs://{bucket}/{name}', engine='pyarrow')


    print(f"gs://{bucket}/{name}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(df.shape)
    print(df.head(5))
    print(event)
    return'''

df=transform_reviews(df)
print(df['time'])
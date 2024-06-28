import pandas as pd
import datetime 

df=pd.read_json(r'E:\Data Science\PF\Datasets\Yelp\checkin1.json',lines=True)
def transform_checkin(df):
    
    #Convertimos la cadena de texto a lista
    df['date'] = df['date'].str.split(',')

    # Usamos explode
    df = df.explode('date')

    #Normalizamos la columna date
    df['date'] = df['date'].astype(str)
    df['date'] = df['date'].str.strip()
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')

    #Nos quedamos con los datos que estan entre 2016 y 2021
    df = df[(df['date'].dt.year >= 2016) & (df['date'].dt.year <= 2021)]

    return df
df=transform_checkin(df)
print(df.head(1))
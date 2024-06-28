import pandas as pd
import numpy as np
import reverse_geocode

df=pd.read_json(r'E:\Data Science\PF\Datasets\Google Maps\metadata-sitios\1.json',lines=True)

def transform_metadata(df):
    
    #Eliminamos columnas que no nos interesan
    df.drop(columns=['description','hours','MISC','relative_results','url','price'],inplace=True)
    #Eliminamos filas con valores nulos en la columna category
    df.dropna(subset='category',inplace=True)
    #Filtramos el dataset con las palabras claves
    palabras_claves = ['restaurant', 'food','steakhouse','mexican','pizzeria','american','asian']

    #Genero una función para filtrar las palabras claves
    def filter_list_by_keywords(lst, palabras_claves):
        return [word for word in lst if any(palabra.lower() in word.lower() for palabra in palabras_claves)]
    
    #Aplico la función a la columna category
    df['category'] =df['category'].apply(lambda x: filter_list_by_keywords(x, palabras_claves))

    #Nos quedamos con las filas que no tienen nulos en la columna category
    df = df[df['category'].apply(lambda x: len(x) > 0)]

    #abrimos el diccionario categorias
    df_dicc=pd.read_excel(r'E:\Data Science\PF\Diccionario Categorías.xlsx')

    #hacemos un explode la columna categorias
    df = df.explode('category')
    
    #Antes del merge usamos title  y strip para normalizar los campos
    df['category'] = df['category'].apply(lambda x: x.title().strip())
    df_dicc['ORIGINAL'] = df_dicc['ORIGINAL'].apply(lambda x: x.title().strip())

    #Hacemos un merge con el diccionario de categorias
    df=df.merge(df_dicc, left_on='category', right_on='ORIGINAL', how='left')

    #Eliminamos las columnas que no nos interesan
    df.drop(columns=['ORIGINAL','category'],inplace=True)

    #Renombramos la columna TRADUCCION
    df.rename(columns={'TRADUCCION':'category'},inplace=True)

    #Eliminamos filas con valores nulos en la columna category
    df.dropna(subset='category',inplace=True)

    #Reseteamos el índice
    df.reset_index(drop=True, inplace=True)

    #Eliminamos los restaurantes que están permanentemente cerrados
    df=df[df['state']!='Permanently closed']
    
    #Eliminamos la columna state
    df.drop(columns='state',inplace=True)

    #Eliminamos las filas que tengan el mismo gmap_id
    df.drop_duplicates(subset='gmap_id',inplace=True)
    
    #Vamos a extraer la ciudad y el código postal de la columna address
    df['city'] =df['address'].str.extract(r',\s*([^,]+),\s*[A-Z]{2}\s+\d{5}', expand=False)
    df['zip_code'] =df['address'].str.extract(r'(\d{5})$', expand=False)
    
    #Creamos una funcion para verificar la ciudad y el estado
    def get_location(row):
        coordinates = [(row['latitude'], row['longitude'])]
        location = reverse_geocode.search(coordinates)[0]
        if location.get('country_code') == 'US' and 'city' in location and 'state' in location:
            return pd.Series([location['city'], location['state']])
        else:
            return pd.Series([None, None])
     
    df[['city', 'state']] = df.apply(get_location, axis=1)
    #Completo los nulos con "Sin Datos"
    df.fillna('Sin Datos', inplace=True)

    #Renombramos las columnas correspondientes
    #df.rename(columns={'estado':'state'},inplace=True)

    #Reordenamos las columnas
    df =df[['gmap_id', 'name', 'address', 'city', 'state', 'zip_code', 'latitude', 'longitude', 'category']]

    def abreviacion_estado(row):
        if row['state'] == 'New York':
            return 'NY'
        elif row['state'] == 'California':
            return 'CA'
        elif row['state'] == 'Texas':
            return 'TX'
        elif row['state'] == 'Florida':
            return 'FL'
        elif row['state'] == 'Pennsylvania':
            return 'PA'
        else:
            return 'Sin Datos'

    df['state'] = df.apply(abreviacion_estado, axis=1)
    
    #Nos quedamos con los restaurantes de los estados de Florida, Texas, California, New York y Pennsylvania
    df = df[df['state'].isin(['FL', 'TX', 'CA', 'NY', 'PA'])]
    
    #Finalmente devolvemos el dataframe
    return df
df=transform_metadata(df)
print(df['category'].value_counts())
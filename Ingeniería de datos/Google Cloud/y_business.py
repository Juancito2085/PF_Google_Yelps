import pandas as pd
import reverse_geocode

df=pd.read_pickle(r'E:\Data Science\PF\Datasets\Yelp\business1.pkl')

def transform_business(df):

    #Nos quedamos con las columnas que nos interesan
    df=df.iloc[:,:14]

    #Eliminamos las columnas que no nos interesan
    df.drop(columns=['attributes'], inplace=True)

    #Eliminamos las filas de la columna 'categories' donde hay nulos
    df.dropna(subset=['categories'], inplace=True)

    #Definimos las palabras claves
    palabras_claves = ['restaurant', 'food','steakhouse','mexican','pizzeria','american','asian']

    #Realizamos una función para convertir un string en una lista de palabras
    def string_to_list(x):
        return [item.strip() for item in x.split(',')]
    
    #Realizamos una función para filtrar las palabras claves
    def filter_list_by_keywords(lst, palabras_claves):
        return [word for word in lst if any(palabra.lower() in word.lower() for palabra in palabras_claves)]
    
    #Convertimos la columna 'categories' en una lista
    df['categories'] = df['categories'].apply(string_to_list)

    #Filtramos las palabras claves
    df['categories'] = df['categories'].apply(lambda x: filter_list_by_keywords(x, palabras_claves))

    #Realizamos una funcion para extraer las palabras claves que no tengan que ver con el rubro
    def filter_list_by_keywords(lst, palabras_claves):
        return [word for word in lst if any(palabra.lower() in word.lower() for palabra in palabras_claves)]
    
    #Eliminamos las filas con listas vacias
    df = df[df['categories'].apply(lambda x: len(x) > 0)]
    #EEEEEE
     #abrimos el diccionario categorias
    df_dicc=pd.read_excel(r'E:\Data Science\PF\Diccionario Categorías.xlsx')

    #hacemos un explode la columna categorias
    df = df.explode('categories')
    
    #Antes del merge usamos title  y strip para normalizar los campos
    df['categories'] = df['categories'].apply(lambda x: x.title().strip())
    df_dicc['ORIGINAL'] = df_dicc['ORIGINAL'].apply(lambda x: x.title().strip())

    #Hacemos un merge con el diccionario de categorias
    df=df.merge(df_dicc, left_on='categories', right_on='ORIGINAL', how='left')

    #Eliminamos las columnas que no nos interesan
    df.drop(columns=['ORIGINAL','categories'],inplace=True)

    #Renombramos la columna TRADUCCION
    df.rename(columns={'TRADUCCION':'categories'},inplace=True)

    #Eliminamos filas con valores nulos en la columna category
    df.dropna(subset='categories',inplace=True)



    #EEEEE
    #Reseteamos el index
    df.reset_index(drop=True, inplace=True)

    #Limpiamos los strings 
    df['name'] = df['name'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['address'] = df['address'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['city'] = df['city'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['state'] = df['state'].apply(lambda x: x.strip() if isinstance(x, str) else x)

    #Creamos una funcion para verificar la ciudad y el estado
    def get_location(row):
        coordinates = [(row['latitude'], row['longitude'])]
        location = reverse_geocode.search(coordinates)[0]
        if location['country_code'] == 'US':
            return pd.Series([location['city'], location['state']])
        else:
            return pd.Series([None, None])

    df[['city', 'state']] = df.apply(get_location, axis=1)

    #Cambiamos los nombres de los estados por sus abreviaturas de los estados que nos interesan
    df['state'] = df['state'].map({'Florida':'FL','Texas':'TX','California':'CA','New York':'NY','Pennsylvania':'PA'})

    #Filtramos los restaurantes por estado
    lista_estados=['FL','TX','CA','NY','PA']
    df = df[df['state'].isin(lista_estados)]

    #Se cambian los tipos de datos de latitude, logitude,stars,review_count
    df = df.astype({
        'latitude': 'float64',
        'longitude': 'float64',
        'stars': 'float64',
        'review_count': 'int64'
    })

    #Borramos la columna hours que finalmente no se usará
    df.drop(columns=['hours'], inplace=True)

    return df
df=transform_business(df)
print(df['categories'].value_counts())

import pandas as pd
from textblob import TextBlob
import re
from math import radians, sin, cos, sqrt, atan2
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import folium
from itertools import combinations
import math

df_full = pd.read_parquet(r'D:\Trabajos\Proyecto Final\DataSet limpios\ML_1.parquet')
df_categorias = pd.read_parquet(r'D:\Trabajos\Proyecto Final\DataSet limpios\categorias_numeros.parquet')
df_ciudades = pd.read_parquet(r'D:\Trabajos\Proyecto Final\DataSet limpios\ciudad_numeros.parquet')
df_full_2 = pd.read_parquet(r'D:\Trabajos\Proyecto Final\DataSet limpios\df_modelo.parquet')

def sentiment_score(review:str) -> int:
  
    if not review:
        return 1
    else:
        analisis = TextBlob(review)
        if analisis.sentiment.polarity < -0.2:
            return 0  
        elif analisis.sentiment.polarity > 0.2:
            return 2  
        else:
            return 1  
        
def separar_fecha(cadena: str) -> tuple:
    find = re.search(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})', str(cadena))
    if find:
        return find.group(1), find.group(2), find.group(3), find.group(4), find.group(5), find.group(6)
    else:
        return None, None, None, None, None, None
    
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371
    return c * r

def ciudad_numero_funcion(ciudad, df):
    for i, row in df.iterrows():
        if row.iloc[1] == ciudad:
            return i
    return -1

def lat_lon(ciudad, df):
    if ciudad in df['city'].values:
        lat=df[df['city']==ciudad]['latitude'].values[0]
        lon=df[df['city']==ciudad]['longitude'].values[0]
        return lat, lon
    else:
        return None, None
    
def categorias_funcion(categoria,df):
    lista_numeros = []
    for i in categoria:
        if i in df['category'].values:
            numero = df[df['category'] == i]['index'].values[0]
            lista_numeros.append(numero)
        else:
            lista_numeros.append(-1)
    while len(lista_numeros) < 5:
        lista_numeros.append(-1)
    return lista_numeros

def plot_predictions_for_categories(categorias1, year, model):
    ciudades_unicas = set(df_full['city'].values)
    predicciones = []
    fechas = []
    ciudades = []
    for ciudad in ciudades_unicas:
        ciudad_numero = ciudad_numero_funcion(ciudad, df_ciudades)
        lat, lon = lat_lon(ciudad_numero, df_full_2)
        categoria_numeros = categorias_funcion(categorias1, df_categorias)
        for anio in year:
            for mes in range(1, 13):
                features = [ciudad_numero, lat, lon] + categoria_numeros + [anio, mes]
                columns = ['city', 'latitude', 'longitude', 'category_1', 'category_2', 'category_3', 
                           'category_4', 'category_5', 'year', 'month']
                features_df = pd.DataFrame([features], columns=columns)
                prediccion = model.predict(features_df)[0]
                predicciones.append(prediccion)
                fechas.append(f"{anio}-{mes:02d}")
                ciudades.append(ciudad)
    resultados_df = pd.DataFrame({'city': ciudades, 'fecha': fechas, 'predicciones': predicciones})
    resultados_df['fecha'] = pd.to_datetime(resultados_df['fecha'])
    scaler = MinMaxScaler()
    resultados_df['predicciones'] = scaler.fit_transform(resultados_df[['predicciones']])
    condicion_prediccion = resultados_df['predicciones'].mean() + 1.8 * resultados_df['predicciones'].std()
    ciudades_filtradas = resultados_df.groupby('city').filter(lambda x: x['predicciones'].mean() > condicion_prediccion)
    ciudades_localizadas = list(ciudades_filtradas['city'].unique())
    latitud=[]
    longitud=[]
    for i in ciudades_localizadas:
        latitud.append(df_full[df_full['city']==i]['latitude'].values[0])
        longitud.append(df_full[df_full['city']==i]['longitude'].values[0])
    resultado_lat_lon = pd.DataFrame({'ciudad':ciudades_localizadas,'latitud': latitud, 'longitud': longitud})
    categoria_string = ' - '.join(categorias1)
    plt.figure(figsize=(12, 8))
    for ciudad in ciudades_filtradas['city'].unique():
        ciudad_df = ciudades_filtradas[ciudades_filtradas['city'] == ciudad]
        plt.plot(ciudad_df['fecha'], ciudad_df['predicciones'], label=ciudad)
    plt.xlabel('Fecha')
    plt.ylabel('Predicciones')
    plt.title(f'Predicciones por ciudad de la categoría {categoria_string}')
    plt.legend(title='Ciudad', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.subplots_adjust(left=0.1, right=0.75, top=0.9, bottom=0.2)
    plt.show()
    map_center = [resultado_lat_lon['latitud'].mean(), resultado_lat_lon['longitud'].mean()]
    mapa = folium.Map(location=map_center, zoom_start=12)
    for _, row in resultado_lat_lon.iterrows():
        folium.Marker(
            location=[row['latitud'], row['longitud']],
            popup=row['ciudad']
        ).add_to(mapa)
    mapa.save('mapa_ciudades.html')
    return mapa

def plot_predictions_for_city(ciudad, year, model, cantidad=1):
    predicciones = []
    fechas = []
    categorias_unicas = []
    categoria_combinations = list(combinations(df_categorias['category'], cantidad))
    total=math.comb(len(df_categorias['category']),cantidad)
    categoria_combinations = categoria_combinations[:total]
    for i in categoria_combinations:
        categorias = list(i)
        ciudad_numero = ciudad_numero_funcion(ciudad, df_ciudades)
        lat, lon = lat_lon(ciudad_numero, df_full_2)
        categoria_numeros = categorias_funcion(categorias, df_categorias)
        for anio in year:
            for mes in range(1, 13):
                features = [ciudad_numero, lat, lon] + categoria_numeros + [anio, mes]
                columns = ['city', 'latitude', 'longitude', 'category_1', 'category_2', 'category_3', 
                            'category_4', 'category_5', 'year', 'month']
                features_df = pd.DataFrame([features], columns=columns)
                prediccion = model.predict(features_df)[0]
                predicciones.append(prediccion)
                fechas.append(f"{anio}-{mes:02d}")
                categorias_unicas.append(categorias)                
            else:
                continue
    resultados_df = pd.DataFrame({'categorias': categorias_unicas, 'fecha': fechas, 'predicciones': predicciones})
    resultados_df['fecha'] = pd.to_datetime(resultados_df['fecha'])
    scaler = MinMaxScaler()
    resultados_df['predicciones'] = scaler.fit_transform(resultados_df[['predicciones']])
    condicion_prediccion_2 = resultados_df['predicciones'].mean() + 0.1 * resultados_df['predicciones'].std()
    resultados_df['categorias'] = resultados_df['categorias'].apply(lambda x: ' - '.join(x) if isinstance(x, list) else x)
    categorias_filtradas = resultados_df.groupby('categorias').filter(lambda x: x['predicciones'].mean() > condicion_prediccion_2)
    latitud=[]
    longitud=[]
    latitud.append(df_full[df_full['city']==ciudad]['latitude'].values[0])
    longitud.append(df_full[df_full['city']==ciudad]['longitude'].values[0])
    resultado_lat_lon = pd.DataFrame({'ciudad':ciudad,'latitud': latitud, 'longitud': longitud})
    plt.figure(figsize=(12, 8))
    for categoria in categorias_filtradas['categorias'].unique():
        categoria_df = categorias_filtradas[categorias_filtradas['categorias'] == categoria]
        plt.plot(categoria_df['fecha'], categoria_df['predicciones'], label=categoria)
    plt.xlabel('Fecha')
    plt.ylabel('Predicciones')
    plt.title(f'Predicciones por categoria en la ciudad {ciudad}')
    plt.legend(title='Categorias', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.subplots_adjust(left=0.1, right=0.75, top=0.9, bottom=0.2)
    plt.show()
    map_center = [resultado_lat_lon['latitud'].mean(), resultado_lat_lon['longitud'].mean()]
    mapa = folium.Map(location=map_center, zoom_start=12)
    for _, row in resultado_lat_lon.iterrows():
        folium.Marker(
            location=[row['latitud'], row['longitud']],
            popup=row['ciudad']
        ).add_to(mapa)
    mapa.save('mapa_ciudades.html')
    return mapa
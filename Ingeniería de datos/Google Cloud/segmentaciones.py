import pandas as pd
import numpy as np

#cargamos el archivo user.parquet
df = pd.read_parquet('E:/Data Science/PF/Datasets/Yelp/user.parquet')

#Lo seccionamos en 10 archivos
df_split = np.array_split(df, 20)

# Guardamos cada segmento en un archivo parquet separado
for i, segment in enumerate(df_split):
    segment.to_json(f'E:/Data Science/PF/Datasets/Yelp/user{i+1}.json', orient='records', lines=True)

#Ahora cargamos el archivo businees.parquet
df = pd.read_parquet('E:/Data Science/PF/Datasets/Yelp/business.parquet')

#Lo seccionamos en 2 archivos
df_split = np.array_split(df, 2)

# Guardamos cada segmento en un archivo parquet separado
for i, segment in enumerate(df_split):
    segment.to_pickle(f'E:/Data Science/PF/Datasets/Yelp/business{i+1}.pkl')

#Cargar el archivo review.parquet
df = pd.read_parquet('E:/Data Science/PF/Datasets/Yelp/review.parquet')

#Lo seccionamos en 5 archivos
df_split = np.array_split(df, 20)

# Guardamos cada segmento en un archivo parquet separado
for i, segment in enumerate(df_split):
    segment.to_json(f'E:/Data Science/PF/Datasets/Yelp/review{i+1}.json', orient='records', lines=True)

#Cargar el archivo checkin.parquet
df = pd.read_json('E:/Data Science/PF/Datasets/Yelp/checkin.json', lines=True)

#Lo seccionamos en 3 archivos
df_split = np.array_split(df, 3)

# Guardamos cada segmento en un archivo parquet separado
for i, segment in enumerate(df_split):
    segment.to_json(f'E:/Data Science/PF/Datasets/Yelp/checkin{i+1}.json', orient='records', lines=True)

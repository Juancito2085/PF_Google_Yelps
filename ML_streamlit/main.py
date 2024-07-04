import streamlit as st
import  bz2
import joblib
import pandas as pd
from funciones import plot_predictions_for_categories
from funciones import plot_predictions_for_city
import matplotlib.pyplot as plt
import pickle
import datetime
import calendar
import torch
import gcsfs
from io import BytesIO
import requests
from streamlit_folium import folium_static



df_full = pd.read_parquet(r'ML_streamlit/Datos/ML_1.parquet')
df_categorias = pd.read_parquet(r'ML_streamlit/Datos/categorias_numeros.parquet')
df_ciudades = pd.read_parquet(r'ML_streamlit/Datos/ciudad_numeros.parquet')
df_full_2 = pd.read_parquet(r'ML_streamlit/Datos/df_modelo.parquet')
#st.title("Proyecto Google-YELP")

# Lee el contenido del archivo styles.css y aplica el estilo
with open("ML_streamlit/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

import base64

def get_image_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Ruta a tu imagen local
image_path = "ML_streamlit/Logo.jpeg"

# Convertir la imagen a Base64
image_base64 = get_image_base64(image_path)

# Insertar la imagen usando HTML con codificación Base64
st.markdown(f"""
    <div class="imagen-especifica">
        <img src="data:image/jpeg;base64,{image_base64}" alt="Logo">
    </div>
""", unsafe_allow_html=True)

# Insertar un elemento HTML <hr>
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("""
    
    <div class="header">
        <h1>Proyecto Google-YELP</h1>
    </div>
    <div class="content">
        <!-- Contenido principal de la presentación -->
        <!-- <p>Aquí va el contenido principal de la presentación.</p> -->
  
    </div>
""", unsafe_allow_html=True)


#Abrimos el modelo
@st.cache_resource
def abrir_modelo(bucket_name, file_name):
    url="https://storage.googleapis.com/modelo_ml_111/Segementacion_modelo_bz2.pkl.bz2"

    response=requests.get(url)
    # Asegúrate de que la solicitud fue exitosa
    if response.status_code == 200:
        # Crea un stream de bytes a partir del contenido comprimido
        compressed_content = BytesIO(response.content)
        
        # Descomprime y carga el modelo directamente desde el stream de bytes
        with bz2.open(compressed_content, 'rb') as f:
            clf = joblib.load(f)
        
        return clf
    else:
        raise Exception(f"Error al acceder al archivo: {response.status_code}")

# Ejemplo de uso
bucket_name = 'modelo_ml_111'
file_name = 'Segementacion_modelo_bz2.pkl.bz2'
clf = abrir_modelo(bucket_name, file_name) 


modelo_seleccionado=st.sidebar.selectbox("Seleccione el tipo de modelo: ", ["Predicción de crecimiento", "Identificación de oportunidades"])



def entrada_seleccionada(modelo):
    if modelo=="Predicción de crecimiento":
        categorias=df_categorias['category'].unique()
        categorias=sorted(categorias)
        categoria_seleccionada = st.sidebar.selectbox("Seleccione las categorías:", categorias)
        categoria_seleccionada=[categoria_seleccionada]
        return categoria_seleccionada, 0
    else:
        ciudades=df_ciudades['city'].unique()
        ciudades=sorted(ciudades)
        ciudad_seleccionada = st.sidebar.selectbox("Seleccione una ciudad:", ciudades)
        cantidad=st.sidebar.slider("Seleccione la cantidad de categoris", 1, 5, 1)
        ciudad_seleccionada=ciudad_seleccionada
        return ciudad_seleccionada, cantidad

entrada, cantidad=entrada_seleccionada(modelo_seleccionado)


if modelo_seleccionado=="Predicción de crecimiento":
    img, mapa = plot_predictions_for_categories(entrada,clf)
    st.image(img, caption='Gráfico de Predicciones por Ciudad', use_column_width=True)
    folium_static(mapa)
else:
    img, mapa = plot_predictions_for_city(entrada,clf,cantidad)
    st.image(img, caption='Gráfico de Predicciones por Categoría' ,use_column_width=True)
    folium_static(mapa)

# Insertar el pie de página (footer)
st.markdown("""
    <style>
        .footer {
            
            font-size: 3px !important; /* Tamaño de fuente reducido */
            color: #FAFAFA !important;
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            height: 50px;
            background-color: #0E1117;
            text-align: center; /* Esto ya debería centrar el texto horizontalmente */
            padding: 10px;
        }
        /* Para asegurar que el texto dentro de .footer también esté centrado verticalmente */
        .footer p {
            margin-left: 230px;
            margin-top: 5px;
            display: flex;
            align-items: center; /* Centra el contenido verticalmente */
            justify-content: center; /* Centra el contenido horizontalmente */
            height: 100%; /* Asegura que el <p> ocupe todo el alto de .footer */
        }
    </style>
    <div class="footer">
        <p>Derechos reservados © 2024. CogniCorp Solutions: Engineering: Juan C. Brunello(MLO), Luis Cerelli;<br>Analyst: Nathaly Castro, Franco D'Auro; Data Science: Lucas Leguizamon.</p>
    </div>
""", unsafe_allow_html=True)
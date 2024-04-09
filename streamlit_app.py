import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import json

from google.cloud import firestore
from google.oauth2 import service_account

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="netflix-a180b")
doc_ref = db.collection(u'name')

# Obtener los documentos de la colección en Firebase
docs = doc_ref.get()
data = [doc.to_dict() for doc in docs]

# Convertir los datos a un DataFrame
df = pd.DataFrame(data)

# Resto del código para la aplicación Streamlit
# Inicio del dashboard con Streamlit
st.title('Netflix app')

# Checkbox para mostrar todos los filmes
if st.sidebar.checkbox('Mostrar todos los filmes'):
    st.dataframe(df)

# Búsqueda de filmes por título
title_search = st.sidebar.text_input('Título del filme')
search_button = st.sidebar.button('Buscar')

if search_button:
    try:
        result = df[df['name'].str.contains(title_search, case=False)]
        if not result.empty:
            st.dataframe(result)
        else:
            st.write('No se encontraron filmes con ese título.')
    except KeyError as e:
        st.error(f'Columna no encontrada en el DataFrame: {e}')

# Selección de director para filtrar filmes
try:
    director_list = df['director'].dropna().unique()
    selected_director = st.sidebar.selectbox('Seleccione un Director', director_list)
except KeyError:
    st.error('La columna "director" no se encuentra en el DataFrame.')
    selected_director = None  # Previene errores más adelante si la columna no existe

filter_button = st.sidebar.button('Filtrar por Director')

if filter_button and selected_director:
    result = df[df['director'] == selected_director]
    st.write(f'Total de filmes encontrados: {len(result)}')
    st.dataframe(result)

# Formulario para buscar filmes con más detalles
with st.sidebar.form("search_form"):
    st.write("Buscar filme:")
    form_name = st.text_input('Nombre del filme')
    form_company = st.text_input('Compañía productora')
    form_director = st.text_input('Director del filme')
    form_genre = st.text_input('Género del filme')
    submit_search = st.form_submit_button('Buscar')

if submit_search:
    # Asegúrate de que estas columnas existen en tu DataFrame.
    query = df
    if form_name:
        query = query[query['name'].str.contains(form_name, case=False)]
    if form_company:
        query = query[query['company'].str.contains(form_company, case=False)]
    if form_director:
        query = query[query['director'].str.contains(form_director, case=False)]
    if form_genre:
        query = query[query['genre'].str.contains(form_genre, case=False)]
    
    st.write(f'Total de filmes encontrados: {len(query)}')
    st.dataframe(query)


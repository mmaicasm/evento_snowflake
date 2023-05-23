# Streamlit
import streamlit as st
# Snowpark
from snowflake.snowpark.session import Session
from snowflake.snowpark.types import Variant
from snowflake.snowpark.functions import udf,sum,col,array_construct,month,year,call_udf,lit
# Librerias necesarias
import numpy as np
import pandas as pd
# Funciones necesarias
from utils import snowpark

# Configuración de la página
st.set_page_config(
  page_title = "Sales Prediction App",
  page_icon = "📈",
  layout = "wide",
  initial_sidebar_state = "auto",
  menu_items = {
    "Get Help": "https://www.hiberus.com/tecnologia/snowflake-ld",
    "Report a bug": None,
    "About": "This is an *extremely* cool app powered by Snowpark and Streamlit"
  }
)

# Imagenes
image_path_1 = "https://raw.githubusercontent.com/mmaicasm/evento_snowflake/main/streamlit_src/hiberus-logo.png"
image_path_2 = "https://raw.githubusercontent.com/mmaicasm/evento_snowflake/main/streamlit_src/snowflake-logo.png"
qr_path = "https://raw.githubusercontent.com/mmaicasm/evento_snowflake/main/streamlit_src/app-qr-code.png"

# Variables
lista_modelos = ["Modelo_1", "Modelo_2"]
lista_paises = ["Alemania","Austria","Bulgaria","Bélgica","Dinamarca","España","Estados Unidos","Finlandia","Francia","Grecia","Holanda","Irlanda","Italia","México","Polonia","Portugal","Reino Unido","Rumania","Rusia","Suecia"]
lista_generos = ["Unisex", "Niño", "Niña"]
lista_productos = []

# Ocultar índices de tablas
hide_table_row_index = """
  <style>
  thead tr th:first-child {display:none}
  tbody th {display:none}
  </style>
  """
st.markdown(hide_table_row_index, unsafe_allow_html = True)

# Barra lateral
st.sidebar.image(image_path_1, use_column_width = True)
st.sidebar.image(qr_path, use_column_width = True)

# Secciones de la App (Containers)
icol1, icol2, icol3, icol4, icol5 = st.columns(5)
with icol1:
  st.write(' ')
with icol2:
  st.write(' ')
with icol3:
  st.image(image_path_2, use_column_width = True)
with icol4:
  st.write(' ')
with icol5:
  st.write(' ')
st.title("Predicción de ventas con Machine Learning")
cabecera = st.container()
col1, _, col2 = st.columns([4, 1, 4])
dataset = st.container()
features_and_output = st.container()

# Cabecera
with cabecera:
  cabecera.write("""Esta app permite visualizar la previsión de venta mes a mes filtrando en base a ciertas variables ajustables mediante widgets. 
    Los modelos fueron entrenados con datos anonimizados de una empresa del sector Retail.""")
  cabecera.write('---')
  
# Check de conexión
if st.session_state['logged'] == True:
  session = st.session_state['session']
  
  # Variables dinámicas
  prediction = []
  table = ''
  
  # Función para cargar los distintos productos
  lista_productos = session.sql('SELECT DISTINCT TIPO_PRENDA AS PRODUCTO FROM EVENTO_SNOWFLAKE.PUBLIC_DATA.DATOS_DEMO ORDER BY TIPO_PRENDA').to_pandas()['PRODUCTO'].to_list()
  
  with col1:
    modelo = st.selectbox(label = 'Modelo', options = lista_modelos, index = 0, help = None)
    var_1 = st.multiselect(label = 'Pais', options = lista_paises, default = None, max_selections = None, help = None)
    prediction.append(modelo)
    prediction.append(var_1)
  
  with col2:
    
    var_2 = st.selectbox(label = 'Producto', options = lista_productos, index = 0, help = None)
    var_3 = st.radio(label = 'Género', options = lista_generos, index = 0, help = None)
    prediction.append(var_2)
    prediction.append(var_3)
    
  # Función para cargar los datos según los widgets
  @st.cache_data(show_spinner = False)
  def load_data(_session, prediction):
    
    if prediction[0] == 'X':
      table = 'xxxxxxxx'
    elif prediction[0] == 'X':
      table = 'xxxxxxxx'
    elif prediction[0] == 'X':
      table = 'xxxxxxxx'
    else:
      st.error('Modelo no reconococido')
      
    if prediction[3] != 'Unisex':
      filtro_gen = f' AND GENERO = {prediction[3]}'
    else:
      filtro_gen = ''
    
    df = _session.sql(f'SELECT XXXXX FROM {table} WHERE PAIS in ({prediction[1]}) AND TIPO_PRENDA = {prediction[2]} {filtro_gen}').to_pandas()
    df['DATE'] = pd.to_datetime(df['DATE'])
    return df
  
  # Gráfico
  with dataset:
    dataset.header("Predicted revenue")
    @st.cache_data(show_spinner = False)
    def predict(prediction):
      
      df = session.sql(f"SELECT xxx=").to_pandas()
        
else:
  st.error("Tienes que loguearte en Snowflake antes de utilizar esta función")
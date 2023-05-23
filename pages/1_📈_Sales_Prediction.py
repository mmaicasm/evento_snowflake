# Streamlit
import streamlit as st
# Snowpark
from snowflake.snowpark.session import Session
from snowflake.snowpark.types import Variant
from snowflake.snowpark.functions import udf,sum,col,array_construct,month,year,call_udf,lit
# Librerias necesarias
import numpy as np
import pandas as pd
import altair as alt
# Funciones necesarias
from utils import snowpark

# Configuración de la página
st.set_page_config(
  page_title = "Sales Prediction App",
  page_icon = "📈",
  layout = "centered",
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

# Variables fijas
lista_paises = ["Alemania","Holanda","Italia"]
lista_productos = ["Pantalón largo", "Pantalón corto"]

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
st.title("Predicción de ventas con ML")
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
  
  # Función para dibujar el gráfico
  def draw(_session, prediction):
    df = snowpark.load_data(_session, prediction)

    months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

    bars = alt.Chart(df).mark_bar().encode(
      x = alt.X("MES", sort = months, title = 'Mes'),
      y = alt.Y("CANTIDAD_PEDIDA", title = "Unidades vendidas"),
      color = alt.Color("TIPO_PRENDA", legend = alt.Legend(orient = "top", title = ""), title = 'Producto'),
      opacity = alt.condition(alt.datum.YEAR == 2022 and alt.datum.MES == "Jun", alt.value(1), alt.value(0.5)),
    )
    chart = alt.layer(bars).resolve_scale(y = "independent")
    chart = chart.configure_view(strokeWidth=0).configure_axisY(domain=False).configure_axis(labelColor="#808495", tickColor="#e6eaf1", gridColor="#e6eaf1", domainColor="#e6eaf1", titleFontWeight=600, titlePadding=10, labelPadding=5, labelFontSize=14).configure_range(category=["#FFE08E", "#03C0F2", "#FFAAAB", "#995EFF"])
    
    try:
      st.altair_chart(chart, use_container_width = True)
    except Exception as e:
      st.error(e)
      st.stop()
  
  # Variables dinámicas
  prediction = []

  with col1:
    var_1 = st.selectbox(label = 'Pais', options = lista_paises, index = 0, help = None)

  with col2:
    var_2 = st.multiselect(label = 'Producto', options = lista_productos, default = None, max_selections = None, help = None)

  prediction.append(var_1)
  prediction.append(var_2)

  # Gráfico
  with dataset:
    if prediction[0] and prediction[1]:
      draw(session, prediction)

else:
  st.error("Tienes que loguearte en Snowflake antes de utilizar esta función")
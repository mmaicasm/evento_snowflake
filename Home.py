# Streamlit
import streamlit as st
# Funciones necesarias
from utils import snowpark

# Formato de página
st.set_page_config(
  page_title = "Home",
  page_icon = "🏠",
  layout = "centered",
  initial_sidebar_state = "expanded",
  menu_items = {
    'Get Help': 'https://www.hiberus.com/tecnologia/snowflake-ld',
    'Report a bug': None,
    'About': "This is an *extremely* cool app powered by Snowpark and Streamlit"
  }
)

# Imagenes
image_path_1 = "https://raw.githubusercontent.com/mmaicasm/evento_snowflake/main/streamlit_src/hiberus-logo.png"
image_path_2 = "https://raw.githubusercontent.com/mmaicasm/evento_snowflake/main/streamlit_src/snowflake-logo.png"
qr_path = "https://raw.githubusercontent.com/mmaicasm/evento_snowflake/main/streamlit_src/app-qr-code.png"

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
st.title('Home')
st.subheader('Conexión a Snowflake mediante Snowpark')

# Inicializar estados
if 'logged' not in st.session_state:
  st.session_state['logged'] = False
  st.session_state['user']  = ''
  st.session_state['role']  = ''
  st.session_state['warehouse']  = ''

# Widget manual
with st.form(key = "login"):
  
  user = st.text_input(placeholder = 'usuario@hiberus.com', label = 'Usuario')
  password = st.text_input(type = 'password', label = 'Contraseña')
  
  login = st.form_submit_button("Conectar")
  guest = st.form_submit_button("Acceder como invitado", disabled = True)
  
  if login or guest:
    if guest:
      # Crear sesión
      with st.spinner('Conectando a Snowflake...'):
        session = snowpark.guest_connect()
      
      # Informar conexión correcta
      st.success('Sesión confirmada!')
      st.snow()
      
      # Mostrar parámetros de la sesión
      #st.write('Parámetros de la sesión:')
      #st.table(session.sql('select current_user(), current_role()').collect())
  
    elif login:
      if user and password:
        # Crear sesión
        with st.spinner('Conectando a Snowflake...'):
          session = snowpark.user_connect(user, password)
        
        # Informar conexión correcta
        st.success('Sesión confirmada!')
        st.snow()
        
        # Mostrar parámetros de la sesión
        #st.write('Parámetros de la sesión:')
        #st.table(session.sql('select current_user(), current_role()').collect())
        
      else:
        st.warning("Introduce tu usuario y contraseña")

if 'logged' in st.session_state and 'session' in st.session_state:
  disconnect = st.button(label = 'Cerrar sesión')
  
  if disconnect:
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state['session'].close()
    for key in st.session_state.keys():
      del st.session_state[key]
    st.warning('Sesión cerrada')
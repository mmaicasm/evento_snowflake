# Streamlit
import streamlit as st
# Snowpark
from snowflake.snowpark.session import Session
from snowflake.snowpark import DataFrame
# Librerias necesarias
import pandas as pd
import random as ra

# Parámetros de conexión
user_connection_parameters = {
  "account": st.secrets["snowflake_account"],
  #"user": st.secrets["snowflake_user"],
  #"password": st.secrets["snowflake_password"],
  "role": "EVENTO_SNOWFLAKE_READ",
  "warehouse": "COMPUTE_WH"
}
guest_connection_parameters = {
  "account": st.secrets["snowflake_account"],
  "user": st.secrets["guest_user"],
  "password": st.secrets["guest_password"],
  "role": "STREAMLIT_READ",
  "warehouse": "STREAMLIT_WH"
}

# Funciones con memoria
@st.cache_resource(show_spinner = False)
def user_connect(user, password):
  # Se crea la conexión
  user_connection_parameters["user"] = user
  user_connection_parameters["password"] = password
  
  try:
    session = Session.builder.configs(user_connection_parameters).create()
  
    # Se actualiza la cache
    st.session_state['logged'] = True
    st.session_state['user'] = user
    st.session_state['role'] = session.get_current_role()
    st.session_state['warehouse'] = user_connection_parameters["warehouse"]
    if 'session' not in st.session_state:
      st.session_state['session'] = session

  except Exception as e:
    st.error('Usuario y/o contraseña erróneos')
    st.stop()
    
  return session

@st.cache_resource(show_spinner = False)
def guest_connect():
  # Se randomiza el usuario si aún no tiene
  if st.session_state['user'] == '':
    n = ra.randint(1,10)
    guest_connection_parameters["user"] += str(n)
  
  try:
    # Se crea la conexión
    session = Session.builder.configs(guest_connection_parameters).create()
    
    # Se actualiza la cache
    st.session_state['logged'] = True
    st.session_state['user'] = guest_connection_parameters["user"]
    st.session_state['role'] = session.get_current_role()
    st.session_state['warehouse'] = guest_connection_parameters["warehouse"]
    if 'session' not in st.session_state:
      st.session_state['session'] = session
  
  except Exception as e:
    st.error('Usuario y/o contraseña erróneos')
    st.stop()
    
  return session

# function - run sql query and return data
@st.cache_data(show_spinner = False)
def query_snowflake(_session, sql) -> pd.DataFrame:

  try:
    df = _session.sql(sql).to_pandas()
      
  except Exception as e:
    st.error(e)
    return e

  return df
# Streamlit
import streamlit as st
from streamlit import components
# Librerias necesarias
import openai
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
# Funciones necesarias
from utils.chain import get_chain
from utils.snowchat_ui import reset_chat_history, extract_code, message_func, is_sql_query
from utils import snowpark

# Configuración de la página
st.set_page_config(
  page_title = "SnowChat",
  page_icon = "❄️",
  layout = "wide",
  initial_sidebar_state = "auto",
  menu_items = {
    "Get Help": "https://www.hiberus.com/tecnologia/snowflake-ld",
    "Report a bug": None,
    "About": '''SnowChat is a chatbot designed to help you with Snowflake Database. It is built using OpenAI's GPT-3.5 and Streamlit. 
      Go to the GitHub repo to learn more about the project. https://github.com/kaarthik108/snowChat'''
  }
)

# Imagenes
image_path_1 = "https://raw.githubusercontent.com/mmaicasm/evento_snowflake/main/streamlit_src/hiberus-logo.png"
image_path_2 = "https://raw.githubusercontent.com/mmaicasm/evento_snowflake/main/streamlit_src/snowflake-logo.png"
image_path_3 = "https://raw.githubusercontent.com/mmaicasm/evento_snowflake/main/streamlit_src/openai-logo.png"
qr_path = "https://raw.githubusercontent.com/mmaicasm/evento_snowflake/main/streamlit_src/app-qr-code.png"

# Variables
openai.api_key = st.secrets["OPENAI_API_KEY"]
MAX_INPUTS = 3
chat_history = []
RESET = True

# Barra lateral
st.sidebar.image(image_path_1, width = 150)
st.sidebar.image(qr_path, width = 150)

# Secciones de la App (Containers)
st.title("SnowChat")
cabecera = st.container()
messages_container = st.container()

# Cabecera
with cabecera:
  cabecera.write("SnowChat es un chatbot que utiliza Chat-GPT para ayudarte con tus consultas en Snowflake.")
  cabecera.image([image_path_2,image_path_3], width = 150)
  cabecera.write('---')
  
# Check de login
if st.session_state['logged'] == True:

  @st.cache_resource(show_spinner = False)
  def load_chain():
    '''
    Load the chain from the local file system

    Returns:
      chain (Chain): The chain object
    '''

    embeddings = OpenAIEmbeddings(openai_api_key = st.secrets["OPENAI_API_KEY"])
    vectorstore = FAISS.load_local("faiss_index", embeddings)
    return get_chain(vectorstore)

  chain = load_chain()

  if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hola! Soy tu asistente virtual especializado en consultas SQL. Dime que necesitas y ya me aclararé yo con Snowflake ❄️🔍"]
  if 'past' not in st.session_state:
    st.session_state['past'] = ["Hola"]
  if "input" not in st.session_state:
    st.session_state["input"] = ""
  if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []
  if 'messages' not in st.session_state:
    st.session_state['messages'] = [("Hola! Soy un chatbot diseñado para ayudarte con tu base de datos en Snowflake.")]
  if "query_count" not in st.session_state:
    st.session_state["query_count"] = 0

  with st.form(key = 'my_form'):
    query = st.text_input("Query: ", key = "input", value = "", placeholder = "Escribe tu pregunta aqui", label_visibility = "hidden")
    submit_button = st.form_submit_button(label = 'Submit')
  col1, col2 = st.columns([1, 3.2])
  reset_button = col1.button("Reset Chat History")

  if reset_button or st.session_state['query_count'] >= MAX_INPUTS and RESET:
    RESET = False
    st.session_state['query_count'] = 0
    reset_chat_history()

  if 'messages' not in st.session_state:
    st.session_state['messages'] = []

  def update_progress_bar(value, prefix, progress_bar = None):
    if progress_bar is None:
      progress_bar = st.empty()

    key = f'{prefix}_progress_bar_value'
    if key not in st.session_state:
      st.session_state[key] = 0

    st.session_state[key] = value
    progress_bar.progress(st.session_state[key])
    if value == 100:
      st.session_state[key] = 0
      progress_bar.empty()

  if len(query) > 2 and submit_button:
    submit_progress_bar = st.empty()
    messages = st.session_state['messages']
    update_progress_bar(33, 'submit', submit_progress_bar)

    result = chain({"question": query, "chat_history": chat_history})
    update_progress_bar(66, 'submit', submit_progress_bar)
    chat_history.append((result["question"], result["answer"]))
    st.session_state['query_count'] += 1
    messages.append((query, result["answer"]))
    st.session_state.past.append(query)
    st.session_state.generated.append(result['answer'])
    update_progress_bar(100, 'submit', submit_progress_bar)

  with messages_container:
    if st.session_state['generated']:
      for i in range(len(st.session_state['generated'])):
        message_func(st.session_state['past'][i], is_user=True)
        message_func(st.session_state["generated"][i])
        if i > 0 and is_sql_query(st.session_state["generated"][i]):
          code = extract_code(st.session_state["generated"][i])
          try:
            if code:
              df = snowpark.query_snowflake(st.session_state["session"], code)
              st.table(df)
          except:  # noqa: E722
            pass

  if st.session_state['query_count'] == MAX_INPUTS and RESET:
    st.warning("Has alcanzado el número máximo de consultas. El historial de chat se borrará en la próxima consulta.")

  col2.markdown(f'<div style="line-height: 2.5;">{st.session_state["query_count"]}/{MAX_INPUTS}</div>', unsafe_allow_html = True)

  st.markdown('<div id="input-container-placeholder"></div>', unsafe_allow_html = True)

  components.v1.html(
    """
    <script>
    window.addEventListener('load', function() {
        const inputContainer = document.querySelector('.stTextInput');
        const inputContainerPlaceholder = document.getElementById('input-container-placeholder');
        inputContainer.id = 'input-container';
        inputContainerPlaceholder.appendChild(inputContainer);
        document.getElementById("input").focus();
    });
    </script>
    """,
    height = 0,
  )
  
else:
  st.error("Tienes que loguearte en Snowflake antes de utilizar esta función")
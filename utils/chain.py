from langchain.prompts.prompt import PromptTemplate
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import (
  ConversationalRetrievalChain,
  LLMChain
)
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
import streamlit as st

template = """Considerando el historial de chat y la pregunta que te proporciono, reescribe la siguiente pregunta como una pregunta independiente. Alternativamente, concluye la conversación si parece que está completada.
Historial de chat:\"""
{chat_history}
\"""
Pregunta: \"""
{question}
\"""
Pregunta independiente:"""

#template = """Considering the provided chat history and a subsequent question, rewrite the follow-up question to be an independent query. Alternatively, conclude the conversation if it appears to be complete.
#Chat History:\"""
#{chat_history}
#\"""
#Follow Up Input: \"""
#{question}
#\"""
#Standalone question:"""
 
condense_question_prompt = PromptTemplate.from_template(template)

TEMPLATE = """ Eres un desarrollador SQL Senior. Debes escribir código SQL para Snowflake considerenado la siguiente pregunta. Además ignora las palabras clave en SQL y da una explicación de una o dos frases de como obtuviste ese código SQL. Muestra el código SQL en formato de código (no asumas nada, si la columna no está disponible di que no lo está, no te inventes el código).
Si no sabes la respuesta solo di "Hmm, no estoy seguro. Estoy entrenado para responder preguntas relacionadas con queries SQL. Por favor vuelve a intentarlo." No te inventes una respuesta.

Pregunta: {question}
{context}
Respuesta:"""  

#TEMPLATE = """ You're a senior SQL developer. You have to write sql code in snowflake database based on the following question. Also you have to ignore the sql keywords and give a one or two sentences about how did you arrive at that sql code. display the sql code in the code format (do not assume anything if the column is not available then say it is not available, do not make up code).
#If you don't know the answer, just say "Hmm, I'm not sure. I am trained only to answer sql related queries. Please try again." Don't try to make up an answer.
#
#Question: {question}
#{context}
#Answer:"""  
QA_PROMPT = PromptTemplate(template=TEMPLATE, input_variables=["question", "context"])


def get_chain(vectorstore):
  """
  Get a chain for chatting with a vector database.
  """
  llm = ChatOpenAI(temperature=0.08, openai_api_key=st.secrets["OPENAI_API_KEY"], model_name='gpt-3.5-turbo')
  
  streaming_llm = ChatOpenAI(
    model_name='gpt-3.5-turbo',
    streaming=False, # Not working yet
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    max_tokens=500,
    temperature=0.08,
    openai_api_key=st.secrets["OPENAI_API_KEY"]
  )
  
  question_generator = LLMChain(
    llm=llm,
    prompt=condense_question_prompt
  )
  
  doc_chain = load_qa_chain(
    llm=streaming_llm,
    chain_type="stuff",
    prompt=QA_PROMPT
  )
  chain = ConversationalRetrievalChain(
    retriever=vectorstore.as_retriever(),
    combine_docs_chain=doc_chain,
    question_generator=question_generator
  )
  return chain
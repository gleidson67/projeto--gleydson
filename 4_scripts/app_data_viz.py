import streamlit as st
import pandas as pd
import plotly.express as px
import requests as r
import seaborn as sns
from sqlalchemy import create_engine
import sqlite3 as sql
engine = create_engine('sqlite:///banco.db', echo=True)

def carregar_dados():
    engine = create_engine('sqlite:///banco.db')
    query = 'SELECT * FROM dados'
    df = pd.read_sql(query, con=engine)
    return df 

df_lido = carregar_dados()


#def carregar_dados():
 #   engine = create_engine('sqlite:///banco.db')

    # Verificar se o banco tem a tabela
  #  with engine.connect() as connection:
   #     result = connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #    tables = [row[0] for row in result]
     #   if 'dados' not in tables:
      #      st.error("Tabela 'dados' não encontrada no banco de dados.")
       #     return pd.DataFrame()  # Retorna um DataFrame vazio

    # Carregar os dados da tabela 'dados'
   # try:
    #    query = 'SELECT * FROM dados'
     #   df = pd.read_sql(query, con=engine)
      #  if df.empty:
       #     st.warning("Tabela 'dados' está vazia.")
        #return df
  #  except Exception as e:
   #     st.error(f"Erro ao carregar os dados: {e}")
    #    return pd.DataFrame()


# def carregar_dados():
#    engine = create_engine('sqlite:///banco.db')  # Conexão com o banco local
#    query = 'SELECT * FROM dados'
#    df = pd.read_sql(query, con=engine)
#    return df

df_lido = carregar_dados()

st.write('**MULTAS EM 2021**')
st.sidebar.header('Municipio')

municipio = df_lido['Nome_Municipio'].drop_duplicates()
municipio_escolhido = st.sidebar.selectbox('Selecione um municipio:', municipio)

df2 = df_lido.loc[df_lido['Nome_Municipio'] == municipio_escolhido]
df2['Total'] = pd.to_numeric(df2['Total'], errors='coerce')
st.write(f'Municipio escolhido: {municipio_escolhido}')

col1, col2, col3 = st.columns(3)
col1.metric('Média de multas por Descrição', value= df2['Total'].mean().round(2))
col2.metric('Mediana de multas por Descrição', value= df2.Total.median().round(2))
col3.metric('Desvio Padrão de multas por Descrição', value= df2.Total.std().round(2))

#UNIVARIADA 1 
fig1 = px.histogram(df_lido.Enq)
st.plotly_chart(fig1)

#UNIVARIADA 2
fig_hist = px.histogram(df_lido, x='Total', nbins=30, title='Histograma do Total de Infrações')
st.plotly_chart(fig_hist)

#UNIVARIADA 3
top_municipios = df_lido['Nome_Municipio'].value_counts().head(10).reset_index()
top_municipios.columns = ['Nome_Municipio', 'Frequência']
fig_pie = px.pie(top_municipios, values='Frequência', names='Nome_Municipio', title='Infrações por Município - Top 10',
                 color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_pie)

# MULTIVARIADA 1
top_descricoes = df_lido['Descricao'].value_counts().head(10).reset_index()
top_descricoes.columns = ['Descricao', 'Frequência']
fig_bar_desc = px.bar(top_descricoes, x='Descricao', y='Frequência', title='Infrações que mais resultam em multas')
fig_bar_desc.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig_bar_desc)

# MULTIVARIADA 2
fig_scatter = px.scatter(df_lido, x='janeiro', y='fevereiro', title='Infrações de Janeiro vs Fevereiro')
st.plotly_chart(fig_scatter)

# MULTIVARIADA 3
top_municipios = df_lido['Nome_Municipio'].value_counts().head(10).index
df_top_municipios = df_lido[df_lido['Nome_Municipio'].isin(top_municipios)]
fig_box_mun = px.box(df_top_municipios, x='Nome_Municipio', y='Total', title='Total de Infrações por Município')
st.plotly_chart(fig_box_mun)

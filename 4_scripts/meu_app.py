import streamlit as st
import pandas as pd
import sqlite3

def carregar_dados():
    try:
        # Conexão com o banco SQLite
        conexao = sqlite3.connect('banco.db')
        query = "SELECT * FROM dados"
        df = pd.read_sql_table(query, conexao)

        if df.empty:
            st.warning("A tabela 'dados' está vazia.")
        return df
    except sqlite3.OperationalError as e:
        st.error(f"Erro ao acessar o banco de dados: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()


# Função para exibir métricas básicas
def exibir_metricas(df, col1, col2, col3):
    col1.metric('Média de multas por Descrição', value=df['Total'].mean().round(2))
    col2.metric('Mediana de multas por Descrição', value=df['Total'].median().round(2))
    col3.metric('Desvio Padrão de multas por Descrição', value=df['Total'].std().round(2))


# Função para criar gráficos usando Streamlit e Pandas
def criar_graficos(df):
    st.subheader("Distribuição das Infrações")

    # Histograma do Total de Infrações
    st.bar_chart(df['Total'].value_counts().sort_index())

    # Pie Chart básico (percentuais por município)
    top_municipios = df['Nome Municipio'].value_counts(normalize=True).head(10) * 100
    st.write("Top 10 Municípios (%)")
    st.bar_chart(top_municipios)

    # Relação entre Janeiro e Fevereiro (apenas se existirem essas colunas)
    if 'janeiro' in df.columns and 'fevereiro' in df.columns:
        st.subheader("Relação entre Infrações em Janeiro e Fevereiro")
        scatter_data = df[['janeiro', 'fevereiro']].dropna()
        st.line_chart(scatter_data)
    else:
        st.warning("Colunas de meses não disponíveis para análise.")


# Carregar os dados
df_lido = carregar_dados()

if not df_lido.empty:
    st.title('**Análise de Multas em 2021**')

    # Sidebar para seleção de município
    st.sidebar.header('Filtro por Município')
    municipios = df_lido['Nome Municipio'].drop_duplicates()
    municipio_escolhido = st.sidebar.selectbox('Selecione um município:', municipios)

    # Filtrar dados pelo município escolhido
    df2 = df_lido[df_lido['Nome Municipio'] == municipio_escolhido]
    df2['Total'] = pd.to_numeric(df2['Total'], errors='coerce')

    # Exibir município escolhido e métricas
    st.write(f'Município escolhido: {municipio_escolhido}')
    col1, col2, col3 = st.columns(3)
    exibir_metricas(df2, col1, col2, col3)

    # Criar gráficos
    criar_graficos(df_lido)
else:
    st.error("Não foi possível carregar os dados. Verifique o banco de dados.")

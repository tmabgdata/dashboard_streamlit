import streamlit as st
import requests
import pandas as pd
import time

@st.cache_data
def converte_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso!', icon="✅")
    time.sleep(5)
    sucesso.empty()

st.title('DADOS BRUTOS')

url = 'https://labdados.com/produtos'

response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))

# Sidebar com filtros
st.sidebar.title('Filtros')

# Filtro por produto
produtos = st.sidebar.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique())

# Filtro por categoria
categoria = st.sidebar.multiselect('Selecione as categorias', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())

# Filtro por preço
preco = st.sidebar.slider('Selecione o preço', 0, 5000, (0, 5000))

# Filtro por frete
frete = st.sidebar.slider('Frete', 0, 250, (0, 250))

# Filtro por data de compra
data_compra = st.sidebar.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))

# Filtro por vendedor
vendedores = st.sidebar.multiselect('Selecione os vendedores', dados['Vendedor'].unique(), dados['Vendedor'].unique())

# Filtro por local de compra
local_compra = st.sidebar.multiselect('Selecione o local da compra', dados['Local da compra'].unique(), dados['Local da compra'].unique())

# Filtro por avaliação
avaliacao = st.sidebar.slider('Selecione a avaliação da compra', 1, 5, value=(1, 5))

# Filtro por tipo de pagamento
tipo_pagamento = st.sidebar.multiselect('Selecione o tipo de pagamento', dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())

# Filtro por quantidade de parcelas
qtd_parcelas = st.sidebar.slider('Selecione a quantidade de parcelas', 1, 24, (1, 24))

# Construindo a query
query = f'''
Produto in {produtos} and \
`Categoria do Produto` in {categoria} and \
{preco[0]} <= Preço <= {preco[1]} and \
{frete[0]} <= Frete <= {frete[1]} and \
{data_compra[0]} <= `Data da Compra` <= {data_compra[1]} and \
Vendedor in {vendedores} and \
`Local da compra` in {local_compra} and \
{avaliacao[0]} <= `Avaliação da compra` <= {avaliacao[1]} and \
`Tipo de pagamento` in {tipo_pagamento} and \
{qtd_parcelas[0]} <= `Quantidade de parcelas` <= {qtd_parcelas[1]}
'''

dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

# Exibindo a tabela filtrada
st.dataframe(dados_filtrados)

# Exibindo a quantidade de registros
st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas')

# Entrada para o nome do arquivo
st.markdown('Escreva um nome para o arquivo')

coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input('', label_visibility='collapsed', value='dados')
    nome_arquivo += '.csv'

with coluna2:
    st.download_button('Fazer o download da tabela em csv', data=converte_csv(dados_filtrados), file_name=nome_arquivo, mime='text/csv', on_click=mensagem_sucesso)

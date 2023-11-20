# Importação de bibliotecas
import streamlit as st
import pandas as pd 
import plotly.graph_objects as go 
import numpy as np 
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Definição da função para plotar séries temporais
def plot_ts(df, nome, units, chart):
    fig = go.Figure()
    colors = ['#e97510','#111a39','#0d6986','#FF5003','#195385','#fead67','#266a7c','#3f6a73','#586b69','#716c5f','#8b6c56','#a46d4c','#bd6e42','#d66e39','#ef6f2f']

    # Adicionando séries ao gráfico
    for i in range(len(df.columns)):
        fig.add_trace(go.Scatter(
                    x=df.index, y=df.iloc[:, i], line=dict(color=colors[i], width=2), name=str(df.columns[i])))

    # Configuração de anotações no gráfico
    fig.add_annotation(
    text = (f"fonte: BLS | Tenax Capital.")
    , showarrow=False
    , x = 0
    , y = -0.19
    , xref='paper'
    , yref='paper' 
    , xanchor='left'
    , yanchor='bottom'
    , xshift=-1
    , yshift=-5
    , font=dict(size=10, color="grey")
    , font_family= "Verdana"
    , align="left"
    )

    # Configuração de layout do gráfico
    fig.update_layout(
        title={ 'text': '<b>'+ nome +'<b>', 'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
        paper_bgcolor='rgba(250,250,250)', # Cor de fundo do gráfico
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_size=20,
        font_color = '#0D1018',
        yaxis_title=units, 
        template='plotly_white',
        font_family="Verdana",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="center",
            x=0.5,
            font_family='Verdana'),
            autosize=True,
            height=500,
            )

    # Configurações adicionais dos eixos do gráfico
    fig.update_xaxes(showgrid=False, zeroline=False, showline=True, linewidth=1.2, linecolor='black')
    fig.update_yaxes(showgrid=False, zeroline=False, showline=True, linewidth=1.2, linecolor='black')
    fig.update_layout(title_x=0.5)
    
    # Configuração do modo de interação com o gráfico
    if chart == 'normal':
        fig.update_layout(hovermode="x")    
    else:
        fig.update_layout(yaxis={'tickformat': ',.2%'})
        fig.update_layout(hovermode="x")        
        
    return fig


# Definição da função para calcular a taxa anualizada
def calculate_annualized_rate(df):
    # Função interna para calcular a taxa composta
    def compound_rate(arr):
        return np.product(1 + arr) ** (12 / len(arr)) - 1

    # Aplicando a função a cada coluna do DataFrame e atualizando a coluna
    for column in df.columns:
        print(column)
        df[column] = df[column].rolling(3).apply(compound_rate).dropna()
        print(df[column])

    return df

# Função para visualização de dados por data
def date_visual(years=2):
    start_date = datetime.now() - relativedelta(years=years)
    end_date = datetime.now() 
    fig.update_xaxes(type="date", range=[start_date, end_date])

# Começo da aplicação
# Configuração do título da aplicação Streamlit
st.title("Relatorio de Inflação Tenax Capital")

# Leitura do arquivo CSV e definição da coluna 'date' como índice
df = pd.read_csv('db.csv').set_index('date')
# Cálculo da variação percentual anual e média móvel de 3 meses
df_12m = df.pct_change(12)
df_3MA = calculate_annualized_rate(df.pct_change(1))

# Extraindo e exibindo os dados mais recentes
# Formatação da tabela para exibir valores em porcentagem
df_latest = df.pct_change(12)[df.index == df.last_valid_index()].style.format("{:.2%}")
st.write(df_latest)

# Index(['All items', 'All items less food and energy', 'Food', 'Energy',
#        'Apparel', 'Education and communication', 'Other goods and services',
#        'Medical care', 'Recreation', 'Transportation'],
#       dtype='object')

tab1,tab2 = st.tabs(["Inflação",''])
with tab1:
    col1, col2 = st.columns(2)

    #Plotar All items vs All items less food and energy

    fig = plot_ts(df_12m[['All items','All items less food and energy']],'Inflation All items vs All items less food and energy','Inflation by year','')
    col1.plotly_chart(fig,use_container_width=True)

    fig = plot_ts(df_3MA[['All items','All items less food and energy']],'Inflation All items vs All items less food and energy','Inflation 3 months annualized','')
    date_visual()
    col2.plotly_chart(fig,use_container_width=True)
    
    # Plotar All items vs Food

    fig = plot_ts(df_12m[['All items','Food']],'Inflation All items vs Food','Inflation by year','')
    col1.plotly_chart(fig,use_container_width=True)

    fig = plot_ts(df_3MA[['All items','Food']],'Inflation All items vs Food','Inflation 3 months annualized','')
    date_visual()
    col2.plotly_chart(fig,use_container_width=True)

    # Plotar All items vs Energy

    fig = plot_ts(df_12m[['All items','Energy']],'Inflation All items vs Energy','Inflation by year','')
    col1.plotly_chart(fig,use_container_width=True)

    fig = plot_ts(df_3MA[['All items','Energy']],'Inflation All items vs Energy','Inflation 3 months annualized','')
    date_visual()
    col2.plotly_chart(fig,use_container_width=True)

    
    # Plotar All items vs Apparel

    fig = plot_ts(df_12m[['All items','Apparel']],'Inflation All items vs Apparel','Inflation by year','')
    col1.plotly_chart(fig,use_container_width=True)

    fig = plot_ts(df_3MA[['All items','Apparel']],'Inflation All items vs Apparel','Inflation 3 months annualized','')
    date_visual()
    col2.plotly_chart(fig,use_container_width=True)

    # Plotar All items vs Education and communication
    
    fig = plot_ts(df_12m[['All items','Education and communication']],'Inflation All items vs Education and communication','Inflation by year','')
    col1.plotly_chart(fig,use_container_width=True)

    fig = plot_ts(df_3MA[['All items','Education and communication']],'Inflation All items vs Education and communication','Inflation 3 months annualized','')
    date_visual()
    col2.plotly_chart(fig,use_container_width=True)

    # Plotar All items vs Other goods and services

    fig = plot_ts(df_12m[['All items','Other goods and services']],'Inflation All items vs Other goods and services','Inflation by year','')
    col1.plotly_chart(fig,use_container_width=True)

    fig = plot_ts(df_3MA[['All items','Other goods and services']],'Inflation All items vs Other goods and services','Inflation 3 months annualized','')
    date_visual()
    col2.plotly_chart(fig,use_container_width=True)

    # Plotar All items vs Medical care

    fig = plot_ts(df_12m[['All items','Medical care']],'Inflation All items vs Medical care','Inflation by year','')
    col1.plotly_chart(fig,use_container_width=True)

    fig = plot_ts(df_3MA[['All items','Medical care']],'Inflation All items vs Medical care','Inflation 3 months annualized','')
    date_visual()
    col2.plotly_chart(fig,use_container_width=True)

    # Plotar All items vs Recreation

    fig = plot_ts(df_12m[['All items','Recreation']],'Inflation All items vs Recreation','Inflation by year','')
    col1.plotly_chart(fig,use_container_width=True)

    fig = plot_ts(df_3MA[['All items','Recreation']],'Inflation All items vs Recreation','Inflation 3 months annualized','')
    date_visual()
    col2.plotly_chart(fig,use_container_width=True)

    # Plotar All items vs Transportation

    fig = plot_ts(df_12m[['All items','Transportation']],'Inflation All items vs Transportation','Inflation by year','')
    col1.plotly_chart(fig,use_container_width=True)

    fig = plot_ts(df_3MA[['All items','Transportation']],'Inflation All items vs Transportation','Inflation 3 months annualized','')
    date_visual()
    col2.plotly_chart(fig,use_container_width=True)

    st.write(df_12m.corr())







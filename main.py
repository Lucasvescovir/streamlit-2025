import streamlit as st 
import pandas as pd

st.set_page_config(page_title='Finanças', page_icon="💰")

st.markdown("""
# Boas vindas!
            
## Nosso APP Financeiro!

Espero que você curta a experiência da nossa solução para organização financeira.
""")

# Widget de upload de dados
file_upload = st.file_uploader(label="Faça upload dos dados aqui", type=['csv'])
# Verifica se algum arquivo deu upload
if file_upload:
    # Leitura dos dados
    df = pd.read_csv(file_upload)
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date
    

    # Exibição dos dados
    exp1 = st.expander("Dados Brutos")
    columns_fmt = {"Valor": st.column_config.NumberColumn("Valor", format="R$ %f")}
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)
    
    # Visão Instituição
    exp2 = st.expander("Instituições")
    df_instituicao = df.pivot_table(index="Data", columns="Instituição",values="Valor")

    # Cria 3 abas DENTRO do expander 2
    tab_data, tab_history, tab_share = exp2.tabs(["Dados", "Histórico","Distribuição"])
    
    # Organiza os dados dentro das abas (Usar sempre ST dentro das tabs)
    with tab_data:
        st.dataframe(df_instituicao)

    # Exibe gráfico do histórico
    with tab_history:
    # Puxa automaticamente o gráfico da planilha de instituições
        st.line_chart(df_instituicao)
    # Exibe gráfico de barras de um dia em específico
    with tab_share:
        # Filtro de data
        date = st.selectbox("Filtro Data", options=df_instituicao.index)
        st.bar_chart(df_instituicao.loc[date])

# Não tem arquivos...
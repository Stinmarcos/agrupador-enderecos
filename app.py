import streamlit as st
import pandas as pd
from io import BytesIO

st.title("📦 Agrupador de Endereços e Pacotes")

uploaded_file = st.file_uploader("Envie sua planilha Excel (.xlsx)", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.write("Prévia da planilha original:")
    st.dataframe(df.head())

    # Padronizar nomes das colunas
    df.columns = df.columns.str.strip().str.lower()

    # Ajuste aqui conforme o nome exato das colunas
    endereco_col = "endereco"
    pacote_col = "sequencia"

    if endereco_col not in df.columns or pacote_col not in df.columns:
        st.error("Verifique se as colunas 'endereco' e 'sequencia' existem na planilha.")
    else:
        agrupado = (
            df.groupby(endereco_col)[pacote_col]
            .apply(lambda x: ", ".join(x.astype(str)))
            .reset_index()
        )

        st.write("Planilha Agrupada:")
        st.dataframe(agrupado)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            agrupado.to_excel(writer, index=False)

        st.download_button(
            label="📥 Baixar Planilha Agrupada",
            data=output.getvalue(),
            file_name="enderecos_agrupados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

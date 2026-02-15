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
   # Detectar automaticamente colunas parecidas
colunas = df.columns.tolist()

endereco_col = None
pacote_col = None

for col in colunas:
    if "end" in col:
        endereco_col = col
    if "seq" in col:
        pacote_col = col

if endereco_col is None or pacote_col is None:
    st.error("Não consegui identificar automaticamente as colunas de endereço e sequência.")
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
)
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

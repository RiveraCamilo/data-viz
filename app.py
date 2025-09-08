"""
Aplicación Streamlit
Librerías: streamlit, pandas, matplotlib, requests (via api_client)
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from api_client import cache_csv, RESOURCE_ID
from transform import clean_and_filter
from analysis import monthly_empresas_capital, kpis

st.set_page_config(page_title="Constituciones 2025 — DataViz Chile", layout="wide")


@st.cache_data(show_spinner=True)
def load_data(force: bool = False, max_rows: int | None = None) -> tuple[pd.DataFrame, str]:
    """Carga desde cache o API, limpia, y si falla intenta refrescar el cache automáticamente."""
    try:
        df = cache_csv(force=force, max_rows=max_rows)
        df, date_col = clean_and_filter(df)
        return df, date_col
    except Exception:
        # Reintento forzando descarga por si el cache corresponde a otro recurso o esquema
        df = cache_csv(force=True, max_rows=max_rows)
        df, date_col = clean_and_filter(df)
        return df, date_col


st.title("Constituciones de Empresas — 2025 (corte 31-jul-2025)")
st.caption("Fuente: datos.gob.cl / Registro de Empresas y Sociedades (API CKAN Datastore)")

with st.sidebar:
    st.header("Controles")
    force = st.checkbox("Forzar actualización desde API", value=False)
    max_rows = st.number_input("Límite de filas (opcional)", min_value=0, value=0, step=1000)

    df, date_col = load_data(force=force, max_rows=(max_rows or None))

    st.markdown(":information_source: **Columna de fecha usada:** ")
    st.code(date_col)

# KPIs
met = kpis(df)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Filas", f"{met['filas']:,}")
c2.metric("Capital total", f"{int(met['capital_total']):,}")
c3.metric("Desde", met['min_fecha'].strftime("%Y-%m") if met['min_fecha'] is not None else "-")
c4.metric("Hasta", met['max_fecha'].strftime("%Y-%m") if met['max_fecha'] is not None else "-")

# Serie mensual
agg = monthly_empresas_capital(df, id_col="RUT" if "RUT" in df.columns else None)

st.subheader("Empresas por mes y Capital total (2025)")
colA, colB = st.columns([2, 1])

with colA:
    # Gráfico combinado: línea (empresas) + barras (capital)
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(agg["mes_str"], agg["empresas"], marker="o", label="Empresas")
    ax2.bar(agg["mes_str"], agg["capital_total"], alpha=0.3, label="Capital total")

    ax1.set_title("Constituciones 2025 — Empresas por mes y Capital total")
    ax1.set_xlabel("Mes")
    ax1.set_ylabel("Empresas (conteo)")
    ax2.set_ylabel("Capital total")
    plt.xticks(rotation=45)
    fig.tight_layout()
    st.pyplot(fig)

with colB:
    st.write("\n")
    st.write("**Tabla mensual**")
    st.dataframe(agg, use_container_width=True)
    st.download_button("Descargar CSV mensual", agg.to_csv(index=False).encode("utf-8"), file_name="constituciones_2025_mensual.csv", mime="text/csv")

st.subheader("Detalle")
st.dataframe(df.head(1000), use_container_width=True)
st.download_button("Descargar CSV (detalle filtrado)", df.to_csv(index=False).encode("utf-8"), file_name="constituciones_2025_detalle.csv", mime="text/csv")


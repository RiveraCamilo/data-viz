"""
Funciones de análisis: KPIs y series mensuales (# empresas y capital total).
"""

import pandas as pd


def monthly_empresas_capital(df: pd.DataFrame, id_col: str | None = "RUT") -> pd.DataFrame:
    # Si no hay RUT, cuenta filas
    if id_col is None or id_col not in df.columns:
        agg = (
            df.groupby("mes")
              .agg(empresas=("mes", "size"), capital_total=("Capital", "sum"))
              .reset_index()
              .sort_values("mes")
        )
    else:
        agg = (
            df.groupby("mes")
              .agg(empresas=(id_col, "nunique"), capital_total=("Capital", "sum"))
              .reset_index()
              .sort_values("mes")
        )
    agg["mes_str"] = agg["mes"].dt.strftime("%Y-%m")
    return agg


def kpis(df: pd.DataFrame) -> dict:
    out = {
        "filas": len(df),
        "columnas": df.shape[1],
        "min_fecha": df["mes"].min() if "mes" in df.columns else None,
        "max_fecha": df["mes"].max() if "mes" in df.columns else None,
        "capital_total": float(df.get("Capital", pd.Series(dtype=float)).sum()),
    }
    return out

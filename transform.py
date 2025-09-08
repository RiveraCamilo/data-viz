"""
Limpieza y enriquecimiento: parseo de fechas, capital, filtros por 2025 y corte 31-jul-2025.
"""

import pandas as pd

DATE_CANDIDATES = [
    "Fecha de actuacion (1era firma)",
    "Fecha de actuación (1era firma)",
    "Fecha de registro (ultima firma)",
    "Fecha de registro (última firma)",
    "Fecha de aprobacion x SII",
    "Fecha de aprobación x SII",
    "Fecha",
    "fecha",
]

def _strip_accents(text: str) -> str:
    import unicodedata
    if not isinstance(text, str):
        text = str(text)
    return "".join(ch for ch in unicodedata.normalize("NFD", text) if unicodedata.category(ch) != "Mn")


def _norm(text: str) -> str:
    return _strip_accents(text).lower().strip()

CUT_OFF_START = pd.Timestamp("2025-01-01")
CUT_OFF_END = pd.Timestamp("2025-07-31")  # según nombre del recurso


def choose_date_column(df: pd.DataFrame) -> str:
    # Limpia posibles BOM y espacios en encabezados
    df.rename(columns=lambda c: str(c).replace("﻿", "").strip(), inplace=True)

    # 1) Busca coincidencias exactas (normalizadas con/ sin acentos)
    cols_norm_map = {col: _norm(col) for col in df.columns}
    for target in DATE_CANDIDATES:
        t = _norm(target)
        for original, normed in cols_norm_map.items():
            if normed == t:
                return original

    # 2) Heurística: cualquier columna que contenga "fecha" o "date"
    for original, normed in cols_norm_map.items():
        if "fecha" in normed or "date" in normed:
            return original

    raise ValueError("No se encontró una columna de fecha en el dataset.")


def parse_capital(series: pd.Series) -> pd.Series:
    # Normaliza separadores de miles/decimal y convierte a numérico
    s = (
        series.astype(str)
        .str.replace(r"[^\d,\.\-]", "", regex=True)
        .str.replace(".", "", regex=False)   # quita miles con punto
        .str.replace(",", ".", regex=False)  # coma a punto
    )
    return pd.to_numeric(s, errors="coerce").fillna(0)


def clean_and_filter(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    df = df.copy()

    # Normaliza nombres de columnas (BOM, espacios)
    df.rename(columns=lambda c: str(c).replace("﻿", "").strip(), inplace=True)

    # 1) Determina columna de fecha y parsea (maneja YYYY-MM-DD y DD-MM-YYYY)
    date_col = choose_date_column(df)
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
    df = df.dropna(subset=[date_col])

    # 2) Filtra tipo de actuación = CONSTITUCIÓN (si existe la columna)
    if "Tipo de actuacion" in df.columns:
        df = df[df["Tipo de actuacion"].astype(str).str.contains("CONSTIT", case=False, na=False)]
    if "Tipo de actuación" in df.columns:
        df = df[df["Tipo de actuación"].astype(str).str.contains("CONSTIT", case=False, na=False)]

    # 3) Filtra por año 2025 y respeta el corte del recurso
    df = df[(df[date_col] >= CUT_OFF_START) & (df[date_col] <= CUT_OFF_END)]

    # 4) Capital a numérico
    if "Capital" in df.columns:
        df["Capital"] = parse_capital(df["Capital"])
    else:
        df["Capital"] = 0

    # 5) Clave mensual
    df["mes"] = df[date_col].dt.to_period("M").dt.to_timestamp()

    # 6) Normaliza tipos string
    for c in df.select_dtypes(include="object").columns:
        df[c] = df[c].astype("string")

    return df, date_col
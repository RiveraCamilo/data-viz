"""
Cliente simple para CKAN Datastore (datos.gob.cl)
Librerías permitidas: requests, json, pandas
"""

import os
import json
import requests
import pandas as pd

BASE_URL = "https://datos.gob.cl/api/3/action"
RESOURCE_ID = "71c8e355-226a-461e-809a-870c2275a178"  # Constituciones 2025 (corte 31-jul-2025)
PAGE_SIZE = 1000


def _datastore_search(resource_id: str, limit: int = PAGE_SIZE, offset: int = 0, base_url: str = BASE_URL, extra_params: dict | None = None) -> dict:
    url = f"{base_url}/datastore_search"
    params = {"resource_id": resource_id, "limit": limit, "offset": offset}
    if extra_params:
        params.update(extra_params)
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if not data.get("success", False):
        raise RuntimeError(f"CKAN error: {data}")
    return data["result"]


def fetch_all_to_df(resource_id: str = RESOURCE_ID, page_size: int = PAGE_SIZE, base_url: str = BASE_URL, max_rows: int | None = None) -> pd.DataFrame:
    """Descarga paginada completa (o hasta max_rows) y retorna DataFrame."""
    records: list[dict] = []
    offset = 0
    total = None
    while True:
        res = _datastore_search(resource_id, limit=page_size, offset=offset, base_url=base_url)
        if total is None:
            total = res.get("total", 0)
        chunk = res.get("records", [])
        if not chunk:
            break
        records.extend(chunk)
        offset += len(chunk)
        if max_rows and len(records) >= max_rows:
            records = records[:max_rows]
            break
        if offset >= total:
            break
    return pd.DataFrame.from_records(records)


def cache_csv(path: str = "data/cache.csv", force: bool = False, max_rows: int | None = None) -> pd.DataFrame:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and not force:
        return pd.read_csv(path)
    df = fetch_all_to_df(max_rows=max_rows)
    df.to_csv(path, index=False)
    return df
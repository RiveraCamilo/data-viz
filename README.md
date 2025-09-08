# Constituciones de Empresas 2025 — DataViz Chile (Streamlit)


Aplicación web simple (hecha con **Streamlit**) que **consume datos públicos** desde el portal **datos.gob.cl** (API CKAN) para el *Registro de Empresas y Sociedades (RES)* y muestra:


- **Empresas constituidas por mes (2025)**  
- **Capital total mensual**  
- **Tablas** con detalle y opción de **descargar CSV**  


> **Fuente de datos**: Recurso "Constituciones 2025 (corte 31‑jul‑2025)" — `resource_id` = `71c8e355-226a-461e-809a-870c2275a178` (no requiere credenciales).


---


## 1) ¿Qué hace la app?


1. **Descarga** los datos desde la API pública (GET a CKAN Datastore) y guarda un **cache local** en `data/cache.csv` para que cargue rápido.  
2. **Limpia y estandariza** fechas y el campo **Capital**.  
3. **Filtra** automáticamente el **año 2025** y respeta el corte **hasta 31‑jul‑2025**.  
4. Calcula la **serie mensual**: número de **empresas** y **capital total**.  
5. Muestra un **gráfico combinado** (línea = empresas, barras = capital) y tablas descargables.  


Librerías usadas: `requests`, `json`, `pandas`, `matplotlib`, `streamlit`.


---


## 2) Requisitos


- **Python 3.10 o superior**  
- Acceso a internet (para consultar la API)  
- (Opcional) *Git* para clonar el repositorio  


---


## 3) Instalación y ejecución (paso a paso, no técnicos)


1. **Descarga** este proyecto (botón *Download ZIP* o `git clone ...`).  
2. **Abre una terminal** dentro de la carpeta del proyecto.  
3. (Opcional) **Crea y activa un entorno virtual**:  
- Ejecuta: `python -m venv .venv` (o `python3 -m venv .venv` en macOS/Linux).  
- **Activa** el entorno:  
- En **macOS/Linux**: `source .venv/bin/activate`  
- En **Windows**: abre la carpeta `.venv` y luego `Scripts`; ejecuta el archivo `Activate` desde tu terminal.  
4. **Instala dependencias**:  

```bash
pip install streamlit pandas requests matplotlib  
```
5. **Ejecuta la app**:  
```bash
streamlit run app.py
```
6. Se abrirá tu navegador (o copia el enlace que aparece en la terminal, normalmente `http://localhost:8501`).  


---


## 4) ¿Cómo usar la app?


- **Barra lateral (izquierda):**  
- **Forzar actualización desde API**: vuelve a descargar datos (ignora el cache).  
- **Límite de filas** (opcional): útil si tu conexión es lenta; por defecto trae todo.  


- **Pantalla principal:**  
- **KPIs**: número de filas, capital total, mes inicial y final disponible.  
- **Gráfico combinado**: línea = **empresas por mes**; barras (transparencia) = **capital total mensual**.  
Eje izquierdo: empresas; eje derecho: capital.  
- **Tabla mensual** con botón **Descargar CSV**.  
- **Detalle** (primeras 1000 filas) con botón **Descargar CSV** del detalle.  


> Consejo: Si no ves datos, pulsa **Forzar actualización** para traer la última versión desde la API.


---


## 5) Estructura del proyecto


```
├─ app.py # App Streamlit (UI y gráficos)  
├─ api_client.py # Cliente CKAN (descarga y cache CSV)  
├─ transform.py # Limpieza, parseo de fechas/capital, filtro 2025 (corte julio)  
├─ analysis.py # Agregaciones mensuales y KPIs  
├─ data/ # Cache local (se crea automáticamente)  
└─ README.md # Este archivo  
```


---


## 6) Configuración (opcional)


- **Cambiar dataset**: abre `api_client.py` y reemplaza `RESOURCE_ID` por el del recurso que quieras (de **datos.gob.cl**).  
- **Elegir otra fecha**: en `transform.py`, la función `choose_date_column` prioriza columnas típicas del RES. Puedes editar el orden o el nombre si tu recurso usa otra convención.  
- **Quitar el corte al 31‑jul‑2025**: cambia `CUT_OFF_END` en `transform.py`.  
- **Contar filas en lugar de RUT**: en `analysis.py`, función `monthly_empresas_capital`, pasa `id_col=None`.  


---


## 7) Solución de problemas


- **La app abre pero el gráfico sale vacío** → Verifica conexión y pulsa **Forzar actualización**.  
- **Error de conexión / proxy corporativo** → Tu red podría requerir un proxy. Prueba desde otra red.  
- **Fechas mal interpretadas** → Ajusta `pd.to_datetime(..., dayfirst=True)` en `transform.py`.  
- **Capital con valores raros** → Revisa `parse_capital` en `transform.py`.  
- **Quiero que siempre descargue todo de nuevo** → Activa **Forzar actualización** o borra `data/cache.csv`.  


---


## 8) Preguntas frecuentes (FAQ)


**¿Necesito cuenta o token?** No. Es público y no requiere autenticación.


**¿Se guardan mis datos personales?** No. Solo se descarga información pública y se guarda un cache local (`data/cache.csv`). Puedes borrarlo cuando quieras.


**¿Puedo desplegar la app en la nube?** Sí. Por ejemplo, en *Streamlit Community Cloud* (sube el repo a GitHub y selecciona `app.py`).


---


## 9) Créditos


- Datos públicos de Chile — **datos.gob.cl** (API CKAN)
- Registro de Empresas y Sociedades (RES) — *Constituciones 2025 (corte 31‑jul‑2025)*


---
"""Streamlit interface for the generated TSE catalog."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "catalog" / "tse" / "datasets" / "manifest.json"
st.set_page_config(page_title="Brasil Eleitoral DataLab", layout="wide")
st.title("Brasil Eleitoral DataLab")
st.caption("Exploração do catálogo público do TSE. Esta tela apresenta metadados, não resultados eleitorais processados.")
if not MANIFEST.is_file():
    st.info("Catálogo local ainda não gerado. Execute python scripts/discover_tse_catalog.py em ambiente com acesso ao TSE.")
    st.code("python scripts/discover_tse_catalog.py", language="bash")
    st.stop()
try:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    st.error(f"Não foi possível ler o manifesto: {exc}")
    st.stop()
items = payload.get("datasets", payload.get("packages", []))
if isinstance(items, dict):
    items = list(items.values())
if not isinstance(items, list):
    st.error("Formato inesperado no manifesto.")
    st.stop()
frame = pd.json_normalize(items) if items else pd.DataFrame()
st.metric("Conjuntos catalogados", len(frame))
if frame.empty:
    st.warning("O manifesto existe, mas não contém conjuntos.")
    st.stop()
search = st.text_input("Buscar por nome, título ou descrição")
columns = [c for c in ("name", "title", "notes", "organization.title", "metadata_modified") if c in frame]
if search and columns:
    mask = frame[columns].fillna('').astype(str).apply(lambda col: col.str.contains(search, case=False, regex=False)).any(axis=1)
    frame = frame[mask]
st.write(f"Registros exibidos: {len(frame)}")
st.dataframe(frame, use_container_width=True, hide_index=True)
st.download_button("Exportar resultado filtrado (CSV)", frame.to_csv(index=False).encode("utf-8"), file_name="tse-catalog-filtered.csv", mime="text/csv")
st.caption("A tela reflete o manifesto local; cobertura e atualização dependem da última execução de descoberta.")

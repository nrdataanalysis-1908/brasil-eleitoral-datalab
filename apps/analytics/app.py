"""Painel analítico do catálogo público do TSE. Gráficos de metadados, não de votação."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "catalog" / "tse" / "datasets" / "manifest.json"
st.set_page_config(page_title="Brasil Eleitoral DataLab | Analytics", page_icon="🗳️", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Barlow+Condensed:wght@500;600;700;800&display=swap');
:root{--cyan:#60e6ff;--blue:#168bd0;--green:#b8ff5c}
.stApp{background:radial-gradient(ellipse at 50% 0%,#10283b 0%,#07111b 52%)}
.block-container{padding-top:1.4rem;max-width:1600px}
h1,h2,h3{font-family:'Barlow Condensed',sans-serif!important}
[data-testid="stMetric"]{background:linear-gradient(145deg,#102235,#09131e);border:1px solid #25445a;padding:14px;border-radius:4px}
[data-testid="stMetricLabel"] p{color:#91aab8!important;font-family:'DM Mono',monospace;font-size:.72rem}
[data-testid="stMetricValue"]{color:var(--cyan);font-family:'Barlow Condensed',sans-serif}
[data-testid="stSidebar"]{background:#081421;border-right:1px solid #23445a}
.eyebrow{color:#60e6ff;font:.72rem 'DM Mono',monospace;letter-spacing:2px}
.panel-note{color:#7892a6;font:.72rem 'DM Mono',monospace}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="eyebrow">NR TECH LAB / DATA INTELLIGENCE / 001</div>', unsafe_allow_html=True)
st.title("BRASIL ELEITORAL DATALAB")
st.caption("Observatório de metadados eleitorais · fonte primária: Portal de Dados Abertos do TSE")
st.markdown('<div class="panel-note">PAINEL ANALÍTICO · CATÁLOGO CKAN · INDICADORES DE METADADOS, NÃO DE VOTAÇÃO</div>', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_catalog(path: str, modified: float) -> tuple[dict[str, Any], pd.DataFrame]:
    del modified
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    items = payload.get("datasets", payload.get("packages", []))
    if isinstance(items, dict):
        items = list(items.values())
    if not isinstance(items, list):
        raise ValueError("O campo datasets/packages do manifesto não é uma lista.")
    return payload, pd.json_normalize(items, sep=".")

def series(frame: pd.DataFrame, candidates: tuple[str, ...], default: str = "") -> pd.Series:
    for col in candidates:
        if col in frame.columns:
            return frame[col].fillna(default).astype(str)
    return pd.Series([default] * len(frame), index=frame.index, dtype="object")

def resources_for(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in frame.iterrows():
        items = row.get("resources", [])
        if isinstance(items, list):
            for resource in items:
                if isinstance(resource, dict):
                    rows.append({"dataset":str(row.get("title") or row.get("name") or "Sem título"),
                                 "format":str(resource.get("format") or "Não informado").strip().upper(),
                                 "name":str(resource.get("name") or resource.get("description") or "Recurso sem nome")})
    return pd.DataFrame(rows, columns=["dataset","format","name"])

if not MANIFEST.is_file():
    st.warning("Catálogo local ainda não gerado. Os gráficos serão habilitados após a descoberta CKAN.")
    st.code("python scripts/discover_tse_catalog.py", language="bash")
    st.info("Execute o coletor com acesso à internet. Nenhum número fictício é usado como demonstração.")
    st.stop()
try:
    payload, original = load_catalog(str(MANIFEST), MANIFEST.stat().st_mtime)
except (OSError, json.JSONDecodeError, ValueError) as exc:
    st.error(f"Falha ao carregar o manifesto: {exc}")
    st.stop()

df = original.copy()
df["title_display"] = series(df, ("title","name"), "Sem título")
df["organization_display"] = series(df, ("organization.title","organization.name","organization"), "Sem órgão")
df["modified_display"] = pd.to_datetime(series(df, ("metadata_modified",)), errors="coerce", utc=True)
df["created_display"] = pd.to_datetime(series(df, ("metadata_created","created")), errors="coerce", utc=True)
with st.sidebar:
    st.markdown("## CONTROLES")
    st.caption("Filtros aplicados aos metadados locais")
    orgs = sorted(df["organization_display"].unique().tolist())
    selected_orgs = st.multiselect("Órgão responsável", orgs)
    all_resources = resources_for(df)
    formats = sorted(all_resources["format"].unique().tolist()) if not all_resources.empty else []
    selected_formats = st.multiselect("Formato de recurso", formats)
    search = st.text_input("Busca textual", placeholder="Nome, descrição ou órgão")
    st.divider()
    st.caption("Manifesto local")
    st.caption(f"Gerado: {payload.get('generated_at') or payload.get('generated') or 'não informado'}")

filtered = df.copy()
if selected_orgs:
    filtered = filtered[filtered["organization_display"].isin(selected_orgs)]
if search:
    text = series(filtered, ("title","name","notes","description")) + " " + filtered["organization_display"]
    filtered = filtered[text.str.contains(search, case=False, regex=False, na=False)]
resources = resources_for(filtered)
if selected_formats:
    resources = resources[resources["format"].isin(selected_formats)]
c1,c2,c3,c4 = st.columns(4)
c1.metric("CONJUNTOS", f"{len(filtered):,}".replace(",","." ))
c2.metric("RECURSOS", f"{len(resources):,}".replace(",","." ))
c3.metric("ÓRGÃOS", f"{filtered['organization_display'].nunique():,}".replace(",","." ))
c4.metric("COM DATA DE ATUALIZAÇÃO", f"{filtered['modified_display'].notna().sum():,}".replace(",","." ))

st.divider()
st.subheader("01 / DISTRIBUIÇÃO DO CATÁLOGO")
left,right = st.columns(2, gap="large")
with left:
    st.markdown("#### Recursos por formato")
    if resources.empty:
        st.info("Nenhum recurso encontrado para os filtros selecionados.")
    else:
        data = resources.groupby("format",as_index=False).size().sort_values("size",ascending=False)
        fig = px.pie(data,names="format",values="size",hole=.62,
                     color_discrete_sequence=["#60e6ff","#168bd0","#b8ff5c","#f4c95d","#8c7bff","#ff7b91"])
        fig.update_traces(textposition="inside",textinfo="percent+label",marker_line_color="#07111b",marker_line_width=2)
        fig.update_layout(height=350,margin=dict(l=8,r=8,t=12,b=8),paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#d9eaf4"))
        st.plotly_chart(fig,use_container_width=True)
with right:
    st.markdown("#### Conjuntos por órgão")
    if filtered.empty:
        st.info("Nenhum conjunto encontrado.")
    else:
        data = filtered.groupby("organization_display",as_index=False).size().sort_values("size").tail(12)
        fig = px.bar(data,x="size",y="organization_display",orientation="h",text="size",
                     color="size",color_continuous_scale=["#0877bd","#60e6ff"])
        fig.update_traces(textposition="outside",cliponaxis=False)
        fig.update_layout(height=350,margin=dict(l=8,r=36,t=12,b=8),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#d9eaf4"),xaxis_title="Quantidade de conjuntos",yaxis_title="",coloraxis_showscale=False)
        st.plotly_chart(fig,use_container_width=True)

st.subheader("02 / COBERTURA TEMPORAL")
a,b = st.columns(2,gap="large")
with a:
    st.markdown("#### Conjuntos criados por ano")
    created = filtered.dropna(subset=["created_display"]).copy()
    if created.empty:
        st.info("Sem datas de criação válidas nos registros filtrados.")
    else:
        created["ano"] = created["created_display"].dt.year
        data = created.groupby("ano",as_index=False).size()
        fig = px.bar(data,x="ano",y="size",text="size",color_discrete_sequence=["#168bd0"])
        fig.update_layout(height=300,margin=dict(l=8,r=8,t=12,b=8),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#d9eaf4"),xaxis_title="Ano de criação",yaxis_title="Conjuntos")
        st.plotly_chart(fig,use_container_width=True)
with b:
    st.markdown("#### Atualizações por mês")
    modified = filtered.dropna(subset=["modified_display"]).copy()
    if modified.empty:
        st.info("Sem datas de atualização válidas nos registros filtrados.")
    else:
        modified["mês"] = modified["modified_display"].dt.strftime("%Y-%m")
        data = modified.groupby("mês",as_index=False).size().sort_values("mês").tail(24)
        fig = px.line(data,x="mês",y="size",markers=True,color_discrete_sequence=["#60e6ff"])
        fig.update_traces(line_width=3,marker_size=7,fill="tozeroy",fillcolor="rgba(96,230,255,.08)")
        fig.update_layout(height=300,margin=dict(l=8,r=8,t=12,b=8),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#d9eaf4"),xaxis_title="Mês da última modificação",yaxis_title="Conjuntos atualizados")
        st.plotly_chart(fig,use_container_width=True)

st.subheader("03 / RECURSOS POR CONJUNTO")
if resources.empty:
    st.info("Não há recursos vinculados aos conjuntos filtrados.")
else:
    data = resources.groupby("dataset",as_index=False).size().sort_values("size",ascending=False).head(15).sort_values("size")
    fig = px.bar(data,x="size",y="dataset",orientation="h",text="size",color_discrete_sequence=["#b8ff5c"])
    fig.update_traces(textposition="outside",cliponaxis=False)
    fig.update_layout(height=max(320,24*len(data)),margin=dict(l=8,r=36,t=12,b=8),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#d9eaf4"),xaxis_title="Quantidade de recursos",yaxis_title="")
    st.plotly_chart(fig,use_container_width=True)

st.subheader("04 / EXPLORADOR DE CONJUNTOS")
cols = [c for c in ("title_display","name","organization_display","metadata_modified","metadata_created","num_resources","license_title") if c in filtered.columns]
table = filtered[cols].rename(columns={"title_display":"Conjunto","name":"Identificador","organization_display":"Órgão","metadata_modified":"Última atualização","metadata_created":"Criação","num_resources":"Recursos (fonte)","license_title":"Licença declarada"})
st.dataframe(table,use_container_width=True,hide_index=True,height=420)
st.download_button("EXPORTAR CONJUNTOS FILTRADOS · CSV",table.to_csv(index=False).encode("utf-8-sig"),file_name="brasil-eleitoral-catalogo-filtrado.csv",mime="text/csv")
with st.expander("METODOLOGIA E LIMITAÇÕES"):
    st.markdown("""
    - Gráficos calculados a partir do manifesto local gerado pela descoberta CKAN.
    - Formatos e contagem de recursos descrevem arquivos cadastrados no catálogo.
    - Séries temporais usam metadata_created e metadata_modified informados pela fonte.
    - Este painel ainda não apresenta votos, candidatos, comparecimento ou abstenção.
    - Indicadores eleitorais dependem da ingestão dos arquivos oficiais, validação de schemas e tabelas Gold documentadas.
    """)
st.caption("NR TECH LAB · BRASIL ELEITORAL DATALAB · DADOS ABERTOS DO TSE")

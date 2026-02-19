import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="quant-system-hf", layout="wide")
st.title("quant-system-hf")

tabs = st.tabs(["Taxonomy (Weekly)", "Trades (Sample)"])

with tabs[0]:
    p = Path("data/taxonomy/weekly/taxonomy_weekly.parquet")
    if p.exists():
        df = pd.read_parquet(p)
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.info("Run pipeline to generate taxonomy: python scripts/run_pipeline.py")

with tabs[1]:
    p = Path("data/curated/trades/trades_standard.parquet")
    if p.exists():
        df = pd.read_parquet(p).head(2000)
        st.dataframe(df, use_container_width=True, height=600)
    else:
        st.info("Run pipeline to generate trades_standard.parquet")

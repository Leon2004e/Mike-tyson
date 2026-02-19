# quant-system-hf

Hedge-fund style systematic trading system scaffold (open-source stack).

## Data flow
raw -> interim -> curated -> features -> taxonomy -> (api/ui/live)

## Quickstart (local)
1) Install
   - python -m venv .venv && source .venv/bin/activate
   - pip install -e .

2) Put broker exports into:
   data/raw/broker_exports/backtest/*.csv  (or live/demo)

3) Run pipeline:
   python scripts/run_pipeline.py --config config/pipelines.yml

4) Start API:
   uvicorn src.api.app:app --reload

5) Start UI:
   streamlit run src/ui/streamlit_app.py

## Conventions (hard rules)
- UTC only (all timestamps)
- raw is append-only (never modify)
- curated tables are rebuildable
- features are versioned (vX_Y)
- sample_type is mandatory: backtest/live/demo/prop

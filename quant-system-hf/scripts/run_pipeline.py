from __future__ import annotations
import argparse
from pathlib import Path
import yaml

from src.ingest.import_trades import ingest_trades
from src.transform.standardize_trades import standardize_trades
from src.transform.enrich_calendar import enrich_calendar
from src.features.build_features import build_features
from src.taxonomy.build_taxonomy import build_taxonomy

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/pipelines.yml")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    steps = {s["name"]: s for s in cfg.get("pipelines", [])}

    # Paths
    interim_trades = Path("data/interim/trades_standardized/trades_raw_concat.parquet")
    curated_trades = Path("data/curated/trades/trades_standard.parquet")
    curated_calendar = Path("data/curated/calendar/calendar.parquet")
    feat_version = steps.get("build_features", {}).get("feature_version", "v1_0")
    features_out = Path(f"data/features/{feat_version}/features.parquet")
    taxonomy_weekly = Path("data/taxonomy/weekly/taxonomy_weekly.parquet")

    if steps.get("ingest_trades", {}).get("enabled", False):
        ingest_trades("data/raw/broker_exports", interim_trades)

    if steps.get("standardize_trades", {}).get("enabled", False):
        standardize_trades(interim_trades, curated_trades)

    if steps.get("enrich_calendar", {}).get("enabled", False):
        enrich_calendar(curated_trades, curated_calendar)

    if steps.get("build_features", {}).get("enabled", False):
        build_features(curated_trades, features_out, feature_version=feat_version)

    if steps.get("build_taxonomy", {}).get("enabled", False):
        build_taxonomy(features_out, taxonomy_weekly, freq="weekly")

    print("OK:", {
        "curated_trades": str(curated_trades),
        "features": str(features_out),
        "taxonomy_weekly": str(taxonomy_weekly),
    })

if __name__ == "__main__":
    main()

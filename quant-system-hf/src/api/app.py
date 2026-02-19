from fastapi import FastAPI
from src.api.routes_trades import router as trades_router
from src.api.routes_taxonomy import router as taxonomy_router
from src.api.routes_jobs import router as jobs_router
from src.api.routes_live import router as live_router

app = FastAPI(title="quant-system-hf")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(trades_router)
app.include_router(taxonomy_router)
app.include_router(jobs_router)
app.include_router(live_router)

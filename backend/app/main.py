from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler

from app.database import Base, engine, SessionLocal
from app.config import CORS_ORIGINS, AUTO_SEED, BASE_DIR
from app import models
from app.prediction import refresh_predictions
from app.routers import auth, products, sales, stock, alerts, analytics, customers

Base.metadata.create_all(bind=engine)

scheduler = BackgroundScheduler()


def refresh_all_shops():
    """Recomputes predictions/alerts for every shop. Runs on a schedule so
    alerts stay fresh even on days with no new sales logged."""
    db = SessionLocal()
    try:
        shop_ids = [row[0] for row in db.query(models.Shop.id).all()]
        for shop_id in shop_ids:
            refresh_predictions(db, shop_id)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if AUTO_SEED:
        # Seed in the background so the server starts accepting requests at once
        # (hosting platforms give up on services that are slow to open their port).
        # It is a no-op if the demo shop already exists.
        import threading
        from app.demo_seed import run as seed_demo_data
        threading.Thread(target=seed_demo_data, daemon=True).start()
    scheduler.add_job(refresh_all_shops, "interval", hours=24, id="daily_prediction_refresh")
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(
    title="StockSense API",
    description="Demand prediction and smart restocking API for small retailers.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(stock.router)
app.include_router(alerts.router)
app.include_router(analytics.router)
app.include_router(customers.router)


@app.get("/health")
def health():
    return {"status": "healthy"}


# ---------------------------------------------------------------------------
# Serve the built React website from this same server (single deployment).
# The compiled frontend lives in backend/static (see README: "Rebuilding the
# frontend"). If it isn't there (e.g. during local API development), "/" just
# returns a small JSON status instead.
# ---------------------------------------------------------------------------
STATIC_DIR = BASE_DIR / "static"

if (STATIC_DIR / "index.html").exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/", include_in_schema=False)
    def serve_website():
        return FileResponse(STATIC_DIR / "index.html")
else:
    @app.get("/")
    def root():
        return {"status": "ok", "service": "StockSense API", "docs": "/docs"}

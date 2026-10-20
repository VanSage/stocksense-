# StockSense

**Demand prediction and smart restocking assistant for small retailers** — kirana
stores, medical/pharmacy shops, and stationery outlets that manage inventory
by memory and instinct, with no barcode scanner, no POS terminal, and no IT
budget.

This is the full-stack implementation: a Python/FastAPI backend (with the
prediction engine built in) and a React + Bootstrap frontend, talking to
each other over a REST API.

---

## Quick start

You need two terminals — one for the backend, one for the frontend.

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed.py                    # creates a demo shop with sample data
uvicorn app.main:app --reload --port 8000
```

Backend is now running at **http://localhost:8000** (API docs at `/docs`).

Runs on SQLite by default — zero setup. To use MySQL instead, see
`backend/README.md`.

### 2. Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend is now running at **http://localhost:5173**.

### 3. Log in

Open http://localhost:5173 and log in with the seeded demo account:

- **Email:** `owner@sharmastore.in`
- **Password:** `password123`

Or click "create a new shop account" to sign up fresh — every shop's data
is fully isolated from every other shop.

---

## What's included

| Feature (from the project synopsis) | Where it lives |
|---|---|
| User & shop management (signup/login, JWT auth, edit profile, change password) | `backend/app/routers/auth.py` + `frontend/src/components/SettingsModal.jsx` |
| Sales logging (quick product search, no barcode needed, optional credit sale) | `frontend/src/pages/SalesEntry.jsx` + `backend/app/routers/sales.py` |
| Real-time stock tracking | `backend/app/routers/stock.py` |
| Demand prediction engine (moving average + trend, via pandas) | `backend/app/prediction.py` |
| Smart reorder alerts + wastage warnings | `backend/app/routers/alerts.py` + auto-generated in `prediction.py` |
| **Customers & udhaar (credit) ledger** | `backend/app/routers/customers.py` + `frontend/src/pages/Customers.jsx` |
| Analytics dashboard (sales trend, category breakdown, top movers, savings estimate, credit outstanding) | `frontend/src/pages/Analytics.jsx` + `backend/app/routers/analytics.py` |

The gear icon in the top bar opens Settings (edit shop name/category/location, your name, and change your password); the bell icon jumps straight to the Alerts page.

### Customers & udhaar (credit) ledger

A shop owner can add customers (name, phone, address) and either:
- Mark a sale as **"sell on credit"** against a customer at the point of sale, which automatically creates a ledger entry, or
- Record a **manual credit or payment** entry directly from a customer's ledger (e.g. correcting a balance, or logging a payment received).

Each customer's current balance is always computed live from their transaction history (sum of credit entries minus payments) — never stored as a separate number that could drift out of sync. The Dashboard and Analytics pages both surface total outstanding credit across all customers.

**Note on scope:** this feature was added after the original synopsis was written, which listed payment/credit tracking as out-of-scope for Version 1 (to differentiate from Vyapar/Khatabook, which are credit-tracking-first). If you're submitting the synopsis alongside this code, make sure both documents are updated to match — either add this feature to the synopsis, or keep it as a clearly-labeled "added beyond original scope" note, so your submitted documentation and your working demo don't contradict each other.

The prediction engine and alert generation re-run automatically every time
a sale is logged, and again on a 24-hour background schedule (via
APScheduler) so alerts never go stale even on days with no new sales.

## Easiest way to run it locally (one window, no Node needed)

The compiled website is already included in `backend/static`, and the backend
serves it. So you only need the backend:

```bash
cd backend
python -m venv venv
venv\Scripts\activate            # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --port 8000
```

Then open **http://localhost:8000** and log in with `owner@sharmastore.in` /
`password123`. The demo shop is created automatically on startup (set
`AUTO_SEED=0` to turn that off) - no `python seed.py` step needed.

The two-window developer mode (backend on :8000 + `npm run dev` on :5173)
described above still works for editing the frontend.

### Rebuilding the frontend (only after you change files in `frontend/src`)

```bash
cd frontend
npm install
npm run build
cd ..
rmdir /s /q backend\static          # Mac/Linux: rm -rf backend/static
xcopy /E /I /Y frontend\dist backend\static   # Mac/Linux: cp -r frontend/dist backend/static
```

## Deploying online for free (single service)

Because the backend serves the website too, there is only ONE thing to deploy.
Do **not** use Vercel for this project - Vercel cannot run a FastAPI server or
keep a database file.

1. Push this project to GitHub.
2. On render.com: New -> Web Service -> pick the repo. Settings:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Instance type: Free
3. Under **Environment** add:
   - `PYTHON_VERSION` = `3.12.7`   (Render's default Python is now 3.14, too new for some libraries)
   - `SECRET_KEY` = any long random text
4. Deploy, then open your `https://<name>.onrender.com` address. That one URL
   is the whole app.

**Keeping data permanently (recommended):** Render's free disk is wiped on every
restart/redeploy, so signups made on the SQLite default would disappear (the
demo shop is recreated automatically, your own data is not). To keep data, create a
free Postgres database at neon.tech, copy its connection string (starts with
`postgresql://`) and add it in Render as the environment variable `DATABASE_URL`.
Nothing else changes - the app switches database by itself.

The free Render instance goes to sleep after ~15 minutes without visitors; the
first visit afterwards takes up to a minute to wake. Open the site a few minutes
before any demo.

## Verifying it works

The backend ships with a real end-to-end test suite (not a stub) that
exercises every endpoint, including edge cases and multi-shop data
isolation:

```bash
cd backend
rm -f stocksense.db     # start from a clean database
python tests/test_api.py
```

Every check prints `OK:` and the script exits non-zero on first failure.

This project was built and verified the same way: the backend test suite
was run for real, the frontend was built with `npm run build` to confirm
zero compile errors, and the whole stack was exercised end-to-end (login,
every page, logging a real sale, resolving a real alert) against the
actual running backend before this was packaged up.

## Project structure

```
stocksense/
├── backend/        # FastAPI + SQLAlchemy + prediction engine — see backend/README.md
└── frontend/       # React + Vite + react-bootstrap + Recharts
```

Each half has its own README with more detail — `backend/README.md` covers
the API and how to switch from SQLite to MySQL; the frontend structure is
straightforward Vite conventions (`src/pages`, `src/components`,
`src/context`, `src/api.js`).

## Design notes

The UI deliberately avoids a generic admin-template look. The palette
(deep plum + saffron + teal) and the "Stock Pulse" bar — the animated,
color-coded health indicator that appears on every product row — exist to
make the core idea of the product (prediction-driven stock health)
visually unmistakable rather than decorative.

## Known limitations (by design, see the project synopsis, Section 4)

- Single-shop focus in this version — no multi-store management yet.
- Prediction uses moving-average + trend analysis, not machine learning —
  intentionally lightweight and explainable (see synopsis Section 2.2 for
  the reasoning).
- No payment gateway or delivery/logistics integration.
- Barcode scanner support is optional and not required for any workflow.

These are documented as future scope, not oversights.

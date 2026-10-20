# StockSense — Smart Inventory Management & Retail Analytics

StockSense is a full-stack inventory management application designed to help small retailers manage products, track sales, monitor stock levels, and make more informed inventory decisions.

The project combines a React-based user interface with a Python FastAPI backend, bringing inventory operations, demand prediction, alerts, and analytics into one application.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Application Architecture](#application-architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Environment Configuration](#environment-configuration)
- [Current Status](#current-status)
- [Future Improvements](#future-improvements)

## Overview

Small retailers need to balance product availability with the cost of holding excess inventory. StockSense aims to make this process easier by bringing stock management, sales tracking, demand prediction, and business analytics into a single application.

The project demonstrates how a full-stack application can combine backend API development, frontend engineering, data processing, and analytical insights to address a practical business problem.

## Key Features

### Inventory Management
- Manage and monitor product inventory.
- Track stock levels and inventory-related information.
- Support stock management workflows through a dedicated interface.

### Sales Management
- Record sales transactions.
- Connect sales activity with inventory management workflows.
- Make sales information available for business analysis.

### Demand Prediction & Smart Restocking
- Provide demand prediction functionality.
- Support inventory planning through stock alerts and restocking-related features.
- Help users identify inventory conditions that may require attention.

*Forecast accuracy and prediction performance should be evaluated against suitable historical data before drawing conclusions about model quality.*

### Analytics Dashboard
- Present business and inventory information through a dashboard.
- Organize analytics into dedicated views.
- Help users explore operational information and identify useful patterns.

### Customer Management
- Provide customer-related management functionality.
- Include a dedicated customer interface and customer credit tracking functionality.

### Authentication & Application Security
- Provide login and signup workflows.
- Organize application access through authentication and protected frontend routes.
- Use backend authentication and security components.

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, JavaScript, Vite |
| Backend | Python, FastAPI |
| API validation | Pydantic-based schemas |
| Data layer | Backend database and data models |
| Analytics | Python-based data processing and analytics |
| Testing | Python test suite |
| Development tools | Git, GitHub, VS Code |

The project uses a separate frontend and backend, allowing each part to be developed and maintained independently.

## Application Architecture

```text
                 User
                   |
                   v
          React Frontend (Vite)
                   |
                   v
           FastAPI REST API
                   |
          +--------+--------+
          |        |        |
          v        v        v
      Products   Sales   Customers
          |        |        |
          +--------+--------+
                   |
                   v
             Data Layer
                   |
          +--------+--------+
          |        |        |
          v        v        v
       Analytics Alerts  Predictions
```

*Conceptual overview of the application. Refer to the backend source code for the exact implementation and data flow.*

## Project Structure

```text
stocksense-/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── alerts.py
│   │   │   ├── analytics.py
│   │   │   ├── auth.py
│   │   │   ├── customers.py
│   │   │   ├── products.py
│   │   │   ├── sales.py
│   │   │   └── stock.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── demo_seed.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── prediction.py
│   │   ├── schemas.py
│   │   └── security.py
│   ├── tests/
│   │   └── test_api.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── .gitignore
├── .python-version
└── README.md
```

## Getting Started

Follow these steps to run StockSense locally.

### Prerequisites

Install the following tools:

- Git
- Python version compatible with the project's `.python-version` file
- Node.js and npm compatible with the frontend dependencies

### 1. Clone the repository

```bash
git clone https://github.com/VanSage/stocksense-.git
cd stocksense-
```

### 2. Set up the backend

From the project root, create a Python virtual environment:

**Windows PowerShell**

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**macOS / Linux**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Configure the backend environment variables using `backend/.env.example` as a reference. Follow the variable names and requirements used by the application configuration.

Do not commit your real `.env` file or credentials.

### 3. Set up the frontend

Open a second terminal from the repository root:

```bash
cd frontend
npm install
```

Configure any frontend environment variables required by `frontend/.env.example`. In particular, ensure that the frontend API base URL points to the backend address used in your local setup.

Do not place private API keys or backend secrets in frontend environment variables.

## Running the Application

### Start the backend

In the backend terminal, with the virtual environment activated:

```powershell
python -m uvicorn app.main:app --reload
```

The API will normally be available at:

`http://127.0.0.1:8000`

If your configuration specifies a different port, use that configured address instead.

### Start the frontend

In the frontend terminal:

```bash
npm run dev
```

Open the local URL printed by Vite in your terminal. The default development address is commonly `http://localhost:5173`.

Keep both development servers running while using the application.

> **Troubleshooting:** If login, signup, or dashboard requests fail, verify that the backend is running and that the frontend API base URL points to the correct backend. A frontend configured to call `localhost` will not automatically connect to a separately deployed backend.

## API Documentation

FastAPI can provide interactive API documentation at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

These endpoints are available when enabled by the running backend configuration.

Use the interactive documentation to inspect available endpoints and test API requests.

## Testing

The backend includes API tests under `backend/tests/`.

From the backend directory, activate the virtual environment and run:

```bash
python -m pytest
```

If pytest is not installed, install it in your development environment before running the tests.

Check the test output to confirm which tests pass or fail. Do not assume the application is fully tested solely because the test suite exists.

## Environment Configuration

The repository contains example environment files:

- `backend/.env.example`
- `frontend/.env.example`

Use these files to identify the configuration needed by each application component.

Before running or deploying the application:

1. Review the example environment files.
2. Configure the required database and API settings.
3. Set the frontend API URL to the correct backend address.
4. Keep private credentials out of source control.
5. Verify that production settings differ appropriately from local development settings.

Never publish passwords, access tokens, database credentials, or production secrets.

## Current Status

StockSense is under active development. The repository contains the frontend, backend API, authentication components, inventory-related modules, analytics, prediction functionality, and backend tests.

Deployment status and production readiness should be confirmed separately. No live application URL is listed here because a verified public deployment link has not been established in this README.

## Future Improvements

Potential areas for further development include:

- Evaluate prediction quality using historical sales data and suitable error metrics.
- Improve analytical reporting and inventory performance insights.
- Strengthen automated testing across frontend and backend workflows.
- Improve deployment configuration and production monitoring.
- Document API contracts and database setup in greater detail.

## Project Goals

StockSense brings together several areas of software and analytics practice:

- **Full-stack development:** building a React frontend and FastAPI backend.
- **API development:** organizing endpoints and data validation.
- **Data analytics:** presenting operational information in useful analytical views.
- **Inventory intelligence:** supporting demand prediction and stock-related decisions.
- **Software quality:** maintaining source code, configuration examples, and automated tests.

---

**Repository:** [VanSage/stocksense-](https://github.com/VanSage/stocksense-)

*Built as a practical project exploring full-stack development, retail operations, and data-driven inventory management.*

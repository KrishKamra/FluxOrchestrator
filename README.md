
# FluxOrchestrator 🛰️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![MySQL](https://img.shields.io/badge/MySQL-Storage-4479A1?style=flat&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Telemetry-47A248?style=flat&logo=mongodb&logoColor=white)](https://www.mongodb.com/)


**FluxOrchestrator is a modular infrastructure designed to bridge the gap between heavy computational workloads and real-time operational monitoring. By utilizing **Polyglot Persistence**, it decouples administrative state from high-velocity telemetry streams.**

---

## 📊 Feature Matrix

| Feature | FluxOrchestrator | W&B / MLflow | Airflow |
| :--- | :---: | :---: | :---: |
| **Self-Hosted** | ✅ Yes | ⚠️ Partial | ✅ Yes |
| **Real-time Telemetry** | ✅ Yes | ✅ Yes | ❌ No |
| **Relational Metadata** | ✅ Yes | ✅ Yes | ✅ Yes |
| **NoSQL Logging** | ✅ Yes | ❌ No | ❌ No |
| **Local-First Ops** | ✅ Yes | ❌ No | ⚠️ Partial |

## 🏗️ Architecture Overview

FluxOrchestrator implements a **Distributed Systems** approach to job management:

```
graph TD
    A[Client/Dashboard] -->|API Requests| B[FastAPI Gateway]
    B -->|Auth/RBAC/State| C[(MySQL: Metadata)]
    B -->|Async Job Ingestion| D[Job Simulator]
    D -->|Real-time Telemetry| E[(MongoDB: Time-Series Logs)]
    E -->|Live Updates| A
````

### 🗄️ Database Strategy

We utilize two distinct database engines to optimize for the **CAP Theorem**:

1.  **Relational Core (MySQL):** Ensures strict **Referential Integrity** for user accounts, role-based access (RBAC), and model registries.
2.  **Telemetry Stream (MongoDB):** Optimized for **High Write-Throughput** of non-relational time-series logs (Accuracy/Loss) during training cycles.

-----

## 🛠️ Data Modeling & Design

This project follows rigorous database design principles. Below are the core architectural diagrams found in the `docs/` directory:

### Entity Relationship Diagram

Describes the conceptual entities and their logical relationships.

### Relational Schema Model

Detailed physical mapping of the MySQL relational structure.

-----

## 🛡️ Security & Governance

  * **Stateless Authorization:** Secure session handling via JWT (JSON Web Tokens).
  * **Credential Protection:** Industry-standard Bcrypt hashing for secure password storage.
  * **Granular RBAC:** Distinct permission tiers for Admins, Researchers, and Viewers.
  * **Traffic Control:** Integrated Rate Limiting to ensure equitable resource distribution and protect backend stability.

## ✨ Key Features

  * **Simulation Engine:** Asynchronous background processing pipeline that never blocks the main event loop.
  * **Experiment Tracking:** Live streaming of performance metrics (loss, accuracy) from the NoSQL layer to an interactive Plotly dashboard.
  * **Resource Management:** Centralized tracking and local storage management for data assets.

-----

## 📂 Project Organization

```text
├── backend/
│   ├── core/       # Security, rate limiting, and DB connectivity
│   ├── models/     # Relational persistence and validation schemas
│   └── routes/     # Decoupled API endpoints (Auth, Resources, Jobs)
├── databases/
│   ├── mongodb/    # Sample telemetry logs and NoSQL config
│   └── mysql/      # SQL initialization schemas
├── docs/           # Architecture diagrams and technical documentation
├── uploads/        # Isolated local storage for data assets
└── dashboard.py    # Streamlit interface for administration & analytics
```

## 🚀 Quick Start (Local Development)

### 1\. Clone & Setup

```bash
git clone [https://github.com/Krish-Kamra/FluxOrchestrator.git](https://github.com/Krish-Kamra/FluxOrchestrator.git)
cd FluxOrchestrator
python -m venv .venv
# Activate venv
# Windows: .venv\Scripts\activate | Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

### 2\. Environment Configuration

Create a `.env` file based on `.env.example`:

```env
DATABASE_URL=mysql+mysqlconnector://user:pass@localhost/flux_db
MONGO_URI=mongodb://localhost:27017/
SECRET_KEY=your_super_secret_key
```

### 3\. Launch the System

```bash
# Start the Backend
uvicorn backend.main:app --reload

# Start the Dashboard (In a new terminal)
streamlit run dashboard.py
```

-----

## 🛠️ Feature Roadmap

  - **Phase 1:** Docker Containerization & WebSocket Streaming.
  - **Phase 2:** Native Hugging Face & PyTorch Job Templates.
  - **Phase 3:** Automated Model Versioning (Model Registry 2.0).

-----

## 🤝 Contributing

Contributions make the open-source community an amazing place to learn and create. Please see the [CODE\_OF\_CONDUCT.md](https://www.google.com/search?q=CODE_OF_CONDUCT.md) for community guidelines.

## 👨‍🔬 Author

**Krish Kamra**

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

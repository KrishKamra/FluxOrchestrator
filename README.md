
-----

# FluxOrchestrator 🛰️

[](https://opensource.org/licenses/MIT)
[](https://www.python.org/downloads/)
[](https://fastapi.tiangolo.com)
[](https://www.mysql.com/)
[](https://www.mongodb.com/)

**FluxOrchestrator** is a modular infrastructure designed to bridge the gap between heavy computational workloads and real-time operational monitoring. By utilizing **Polyglot Persistence**, it decouples administrative state from high-velocity telemetry streams, ensuring high availability and low-latency feedback during AI training cycles.

-----

## ⚡ Core Value Proposition

| Capability              | Why It Matters                          |
|-------------------------|-----------------------------------------|
| 🧩 Polyglot Persistence | Optimizes storage per workload type     |
| 📡 Real-time Telemetry  | Enables live monitoring of training jobs|
| ⚙️ Async Processing     | Prevents API bottlenecks                |
| 🔐 RBAC + JWT           | Production-grade security model         |
| 🖥️ Local-first Design   | Full control without cloud lock-in      |

---

## 📊 Feature Matrix

| Feature | FluxOrchestrator | W\&B / MLflow | Airflow |
| :--- | :---: | :---: | :---: |
| **Self-Hosted** | ✅ Yes | ⚠️ Partial | ✅ Yes |
| **Real-time Telemetry** | ✅ Yes | ✅ Yes | ❌ No |
| **Relational Metadata** | ✅ Yes | ✅ Yes | ✅ Yes |
| **NoSQL Logging** | ✅ Yes | ❌ No | ❌ No |
| **Local-First Ops** | ✅ Yes | ❌ No | ⚠️ Partial |

-----

## 🏗️ Architecture Overview

FluxOrchestrator implements a distributed systems approach to job management and telemetry ingestion.

```mermaid
graph TD;
    %% Nodes
    Client[Client / Streamlit Dashboard]
    API[FastAPI Gateway]
    JobSim[Async Job Simulator]

    subgraph Storage [Polyglot Layer]
        MySQL[(MySQL: Meta State)]
        Mongo[(MongoDB: Telemetry)]
    end

    %% Flow
    Client <-->|REST / JWT| API
    API <-->|Auth / RBAC| MySQL
    API -->|Trigger Task| JobSim
    JobSim -->|High-Velocity Logs| Mongo
    Mongo -.->|Live Ingestion| Client

    %% Styling
    style Client fill:#f9f,stroke:#333,stroke-width:2px
    style API fill:#009688,color:#fff
    style MySQL fill:#4479A1,color:#fff
    style Mongo fill:#47A248,color:#fff
    style JobSim fill:#f96,stroke:#333
```


### 🗄️ Database Strategy

We utilize two distinct database engines to optimize for the **CAP Theorem**:

1.  **Relational Core (MySQL):** Ensures strict **Referential Integrity** and ACID compliance for user accounts, Role-Based Access Control (RBAC), and model registries.
2.  **Telemetry Stream (MongoDB):** Optimized for **High Write-Throughput** of non-relational time-series logs (Loss, Accuracy, System Heat) during intensive training cycles.

-----

## 🛡️ Security & Governance

  * **Stateless Authorization:** Secure session handling via **JWT (JSON Web Tokens)**.
  * **Credential Protection:** Industry-standard **Bcrypt** hashing for secure password storage.
  * **Granular RBAC:** Distinct permission tiers for Admins, Researchers, and Viewers.
  * **Traffic Control:** Integrated **Rate Limiting** to ensure backend stability and protect against resource exhaustion.

-----

## ✨ Key Features

  * **Simulation Engine:** An asynchronous background processing pipeline that utilizes Python's `asyncio` to prevent blocking the main event loop.
  * **Experiment Tracking:** Live streaming of performance metrics from the NoSQL layer to an interactive Plotly-driven dashboard.
  * **Local-First Resource Management:** Centralized tracking and local storage management for data assets, optimized for NPU-accelerated hardware.

-----

## 📂 Project Organization

```text
├── backend/
│   ├── core/           # Security, rate limiting, and DB connectivity
│   ├── models/         # Relational SQLAlchemy models & Pydantic schemas
│   └── routes/         # Decoupled API endpoints (Auth, Resources, Jobs)
├── databases/
│   ├── mongodb/        # NoSQL config & telemetry scripts
│   └── mysql/          # SQL initialization & migration schemas
├── docs/               # Architecture diagrams and technical documentation
├── uploads/            # Isolated local storage for datasets/models
└── dashboard.py        # Streamlit interface for administration & analytics
```

-----

## 🚀 Quick Start

### 1\. Clone & Setup

```bash
git clone https://github.com/Krish-Kamra/FluxOrchestrator.git
cd FluxOrchestrator
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2\. Environment Configuration

Create a `.env` file in the root directory:

```env
DATABASE_URL=mysql+mysqlconnector://user:pass@localhost/flux_db
MONGO_URI=mongodb://localhost:27017/
SECRET_KEY=your_generated_secure_key
```

### 3\. Launch the System

```bash
# Start the Backend Gateway
uvicorn backend.main:app --reload

# Start the Analytics Dashboard
streamlit run dashboard.py
```

-----

## 🛠️ Feature Roadmap

  - **Phase 1:** Docker Containerization & WebSocket real-time streaming.
  - **Phase 2:** Native Hugging Face & PyTorch integration templates.
  - **Phase 3:** Automated Model Versioning (Model Registry 2.0).

-----

## 👨‍🔬 Author

**Krish Kamra** 

-----

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

-----

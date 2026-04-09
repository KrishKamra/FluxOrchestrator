# Universal Job & Telemetry Orchestrator

A modular infrastructure designed for the secure execution of simulated workloads and the high-frequency tracking of performance telemetry. This platform implements a polyglot persistence strategy to decouple administrative metadata from high-velocity operational logs.

## 🏗️ Technical Architecture
The system architecture is optimized for data throughput and integrity using two distinct database layers:
* **Relational Layer (MySQL):** Managed via SQLAlchemy to handle structured metadata, including User identity management and Resource registries.
* **Telemetry Layer (MongoDB):** Utilized for non-relational, time-series log ingestion to ensure maximum write-performance during active job execution cycles.

## 🛡️ Security & Governance Framework
* **Stateless Authorization:** Secure session handling via JWT (JSON Web Tokens).
* **Credential Protection:** Industry-standard Bcrypt hashing for secure password storage.
* **Granular RBAC:** Role-Based Access Control enforcing specific execution and viewing rights across Admin, Operator, and Auditor roles.
* **Traffic Control:** Integrated Rate Limiting to ensure equitable resource distribution and protect backend stability.

## ✨ Functional Capabilities
* **Resource Management:** Centralized tracking and local storage of specialized data assets.
* **Simulation Engine:** Asynchronous job processing pipeline with live telemetry streaming to the NoSQL backend.
* **Performance Insights:** Interactive dashboard for visualizing historical telemetry trends and operational metrics.

## 📂 Project Organization
* `backend/core/`: Contains the fundamental logic for security, rate limiting, and database connectivity.
* `backend/models/`: Defines the schemas for relational persistence and data validation.
* `backend/routes/`: Decoupled API endpoints for authentication, resource management, and job orchestration.
* `uploads/`: Isolated local storage for uploaded data assets.
* `dashboard.py`: Streamlit-based interface for system monitoring and data visualization.

## 🚀 Setup & Execution
1.  **Environment:** Configure a `.env` file with the required SQL and NoSQL connection strings.
2.  **Dependencies:** Install requirements using `pip install -r requirements.txt`.
3.  **Initialization:** Execute the database scripts to generate the core relational schema.
4.  **Launch:**
    * Backend: `uvicorn backend.main:app --reload`
    * Frontend: `streamlit run dashboard.py`
## 👨‍🔬 Author
**Krish Kamra** 
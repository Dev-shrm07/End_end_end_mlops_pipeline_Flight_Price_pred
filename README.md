# ✈️ Flight Price Prediction – End-to-End ML Pipeline

This project is a full-scale **end-to-end machine learning pipeline** for predicting flight prices. It's designed with modularity, scalability, and production-readiness in mind, using orchestration, experiment tracking, and real-time model serving.

---

## 🚀 Features

### 🔁 End-to-End Pipeline
- **Data Ingestion**: Loads raw flight fare data from **Amazon S3** (can be extended to other sources).
- **Preprocessing**: Cleans, transforms, and encodes data.
- **Model Training**: Trains multiple ML models and selects the best one based on evaluation metrics.
- **Model Registry & Logging**: Uses **MLflow** to log experiments and register the best model.
- **Prediction Pipeline**: Automatically prepares incoming data for inference using trained transformers.
- **Artifact Storage**: Stores trained models and processors back in **S3**.

### ⚙️ Orchestration with Airflow
- All tasks are orchestrated using **Apache Airflow**.
- DAG defined in `airflow/dags/model_pipeline.py`.
- Airflow is protected using **FAB-based authentication**.
- DAG runs include ingestion, preprocessing, training, artifact upload, and more.

### 🌐 API Endpoint with FastAPI
- Serves model predictions via a REST endpoint at `/predict`.
- Uses **Pydantic** for strict input validation and schema enforcement.
- Deployed using **Uvicorn**.

### 📊 MLflow Tracking
- Tracks all experiment runs including parameters, metrics, and artifacts.
- MLflow UI available at `http://localhost:5000`.

---

## 🧱 Architecture

### Three services run simultaneously:

| Service     | Port  | Description                      |
|-------------|-------|----------------------------------|
| Airflow     | 8080  | Web UI for DAG orchestration     |
| FastAPI     | 8000  | Model prediction endpoint        |
| MLflow      | 5000  | Experiment tracking UI           |

> **Note**: Can be split into **separate microservices** and deployed on different instances for scale.

---

## 🌩️ Deployment

### 🐳 Docker-Based

Everything runs via Docker. Just use:

```bash
bash run.sh
```

This script:
- Boots up Airflow with the configured DAG
- Starts MLflow tracking UI
- Launches the FastAPI app for inference

### 🧪 Local Setup (Optional)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Airflow standalone
airflow standalone

# Start API
uvicorn api.app:app --reload

# MLflow UI
mlflow ui
```

---

## 📦 CI/CD

- Configured with **GitHub Actions** to build and deploy Docker image.
- Can be deployed to **AWS EC2** (or ECS) using shell or Terraform scripts.
- Example deployment (currently only API live due to RAM constraints on free tier):

🔗 **Live API Endpoint:** [http://](API)

---

## 📁 Project Structure

```
E2E/
│
├── airflow/
│   └── dags/
│       └── model_pipeline.py          # DAG for orchestrating the pipeline
│
├── api/
│   ├── app.py                         # FastAPI app
│   └── request_model.py              # Pydantic model for input validation
│
├── src/
│   └── components/
│       ├── data_collection.py
│       ├── data_ingestion.py
│       ├── data_preprocessing.py
│       ├── model_training.py
│       ├── predict_pipeline.py
│       └── handles3.py              # S3 utility functions
├── notebooks/
├── Dockerfile
├── requirements.txt
├── run.sh                             # Spins up Airflow, MLflow, and FastAPI
```

---

## 📞 Sample API Call

**POST `/predict`**

```json
{
  "airline": "SpiceJet",
  "source": "Delhi",
  "destination": "Mumbai",
  "departure_time": "Evening",
  "arrival_time": "Night",
  "duration": 2.5,
  "stops": "zero",
  "days_left":1,
  "class": "Economy"
}
```

**Response**

```json
{
  "price": 3456.78
}
```

## 🧠 Tech Stack

- **Python**
- **Apache Airflow**
- **MLflow**
- **FastAPI**
- **Docker**
- **AWS (EC2, S3)**
- **GitHub Actions**

---

## ✅ Highlights

- 🔄 Modular pipeline with isolated components
- 🔁 Automated with Airflow DAGs
- 🔍 Transparent model tracking with MLflow
- 📦 Dockerized for consistency
- 🌐 Real-time predictions via FastAPI
- 🚀 Deployed on AWS with CI/CD

---

## 📌 Future Enhancements


- Add support for more data sources (e.g. PostgreSQL, APIs, Web Scrapping)
- Deploy each service as an independent microservice

---

## 🙌 Contributions

Open to improvements, ideas, or issues! Feel free to fork and raise a PR 🚀

---

> 💡 Built to showcase end-to-end ML engineering and deployment skills with production-level architecture.
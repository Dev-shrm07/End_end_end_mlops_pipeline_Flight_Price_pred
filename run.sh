#!/bin/bash


mlflow ui --host 0.0.0.0 --port 5000 &
MLFLOW_UI_PID=$!
echo "MLflow started! Webserver: http://localhost:5000"


export AIRFLOW_HOME=$(pwd)/airflow
export AIRFLOW__CORE__LOAD_EXAMPLES=False
airflow db migrate


airflow api-server --host 0.0.0.0 --port 8080 &
AIRFLOW_WEBSERVER_PID=$!
airflow scheduler &
AIRFLOW_SCHEDULER_PID=$!
airflow dag-processor &
AIRFLOW_DAG_PROCESSOR_PID=$!
echo "Airflow started! Webserver: http://localhost:8080"
echo "DAGs folder: $AIRFLOW_HOME/dags"


uvicorn api.app:app --host 0.0.0.0 --port 8000 &
API_PID=$!
echo "API started! Webserver: http://localhost:8000"


trap "echo 'Stopping all services...'; \
      kill $MLFLOW_UI_PID $AIRFLOW_WEBSERVER_PID $AIRFLOW_SCHEDULER_PID $AIRFLOW_DAG_PROCESSOR_PID $API_PID" SIGINT


wait $MLFLOW_UI_PID $AIRFLOW_WEBSERVER_PID $AIRFLOW_SCHEDULER_PID $AIRFLOW_DAG_PROCESSOR_PID $API_PID



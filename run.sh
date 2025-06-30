#!/bin/bash

## Only running API service as of now on EC2 due to ram issues, to run mlflow and airflow uncomment subsequent commands.
# mlflow ui --host 0.0.0.0 --port 5000 &
# MLFLOW_UI_PID=$!
# echo "MLflow started! Webserver: http://localhost:5000"


# export AIRFLOW_HOME=$(pwd)/airflow
# export AIRFLOW__CORE__LOAD_EXAMPLES=False
# export AIRFLOW__CORE__AUTH_MANAGER=airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager

# airflow db migrate

# airflow users create \
#   --username airflow \
#   --firstname Airflow \
#   --lastname Admin \
#   --email airflow@example.com \
#   --role Admin \
#   --password "$AIRFLOW_PASSWORD"   


# airflow api-server --host 0.0.0.0 --port 8080 &
# AIRFLOW_WEBSERVER_PID=$!
# airflow scheduler &
# AIRFLOW_SCHEDULER_PID=$!
# airflow dag-processor &
# AIRFLOW_DAG_PROCESSOR_PID=$!
# echo "Airflow started! Webserver: http://localhost:8080"
# echo "DAGs folder: $AIRFLOW_HOME/dags"


uvicorn api.app:app --host 0.0.0.0 --port 8000 &
API_PID=$!
echo "API started! Webserver: http://localhost:8000"


# trap "echo 'Stopping all services...'; \
#       kill $MLFLOW_UI_PID $AIRFLOW_WEBSERVER_PID $AIRFLOW_SCHEDULER_PID $AIRFLOW_DAG_PROCESSOR_PID $API_PID" SIGINT

trap "echo 'Stopping all services...'; \
      kill $API_PID" SIGINT
# wait $MLFLOW_UI_PID $AIRFLOW_WEBSERVER_PID $AIRFLOW_SCHEDULER_PID $AIRFLOW_DAG_PROCESSOR_PID $API_PID

wait  $API_PID

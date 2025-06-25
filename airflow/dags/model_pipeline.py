from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import joblib
import os

import sys


try:
    from src.components.data_ingestion import DataIngestion
    from src.components.data_preprocessing import DataPreprocssing
    from src.components.model_training import ModelTrainer
    from src.components.data_collection import getData
except ImportError:
    dag_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(dag_dir)) 
    sys.path.insert(0, project_root)
    from src.components.data_ingestion import DataIngestion
    from src.components.data_preprocessing import DataPreprocssing
    from src.components.model_training import ModelTrainer
    from src.components.data_collection import getData



DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'artifacts', 'airflow_pipeline')

def check_data():
    result = getData()
    if result:
        return 'ingest_data'
    else:
        return 'skip_ingestion'
    
    
def ingest_data():
    d = DataIngestion()
    d.ingest_data()
    


def preprocess_data():
    P = DataPreprocssing()
    X, Y = P.preprocess_data()
    joblib.dump((X, Y), os.path.join(DATA_DIR, 'XY.pkl'))
    

def train_model():
    X, Y = joblib.load(os.path.join(DATA_DIR, 'XY.pkl'))
    m = ModelTrainer()
    m.initiate_model_trainer(X, Y)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['sample@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    'ml_pipeline_dag',
    default_args=default_args,
    description='End-to-End ML pipeline DAG',
    schedule=None,
    start_date=datetime(2025, 6, 24),
    catchup=False,
    tags=['ml_pipeline'],
) as dag:
    
    branch = BranchPythonOperator(
        task_id='check_data',
        python_callable=check_data
    )

    ingest = PythonOperator(
        task_id='ingest_data',
        python_callable=ingest_data
    )

    preprocess = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data
    )

    train = PythonOperator(
        task_id='train_model',
        python_callable=train_model
    )
    
    

    
    skip = EmptyOperator(task_id='skip_ingestion')
    
    branch >> [ingest, skip]
    ingest >> preprocess >> train

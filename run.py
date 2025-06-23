from src.components.data_preprocessing import DataPreprocssing
from src.components.data_ingestion import DataIngestion
from src.components.model_training import ModelTrainer


if __name__ == "__main__":
    d = DataIngestion()
    d.ingest_data()
    P = DataPreprocssing()
    X,Y = P.preprocess_data()
    m = ModelTrainer()
   # m.initiate_model_trainer(X,Y)
   # ,airline,flight,source_city,departure_time,stops,arrival_time,destination_city,class,duration,days_left,price
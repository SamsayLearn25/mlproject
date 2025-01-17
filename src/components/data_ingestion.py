import os, sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd


from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngesetionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

@dataclass
class DataIngestionArtifact:
    train_data_path: str
    test_data_path: str

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngesetionConfig):

        self.ingestion_config = data_ingestion_config

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        # read from data source
        logging.info("Entered Data Ingestion Method")
        try:
            df = pd.read_csv("data/stud.csv")
            logging.info("Read the dataset as df")
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, header=True, index=False)
            logging.info("Raw Data Saved")

            logging.info("Train Test Split Initiated")
            train, test = train_test_split(df, test_size=0.2, random_state=42)
            
            train.to_csv(self.ingestion_config.train_data_path, index = False, header = True)
            test.to_csv(self.ingestion_config.test_data_path, index = False, header = True)

            logging.info("Data ingestion completed")

            return DataIngestionArtifact(self.ingestion_config.train_data_path, self.ingestion_config.test_data_path)

        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":

    data_ingestion_config = DataIngesetionConfig()
    data_ingestion = DataIngestion(data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    print(data_ingestion_artifact)
            
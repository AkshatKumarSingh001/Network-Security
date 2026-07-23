from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.entity.config_entity import DataIngestionConfig
from Network_Security.entity.config_entity import TrainingPipelineConfig
from push_data import push_data_to_mongodb
import sys
import os


if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Starting data ingestion process...")

        try:
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        except NetworkSecurityException as e:
            if "No records found in MongoDB database" not in str(e):
                raise

            logging.info("MongoDB collection is empty. Seeding data from CSV and retrying ingestion.")
            push_data_to_mongodb(
                database=data_ingestion_config.database_name,
                collection=data_ingestion_config.collection_name,
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        print(data_ingestion_artifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
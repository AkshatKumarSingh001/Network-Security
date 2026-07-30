from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.components.data_validation import DataValidation, DataValidationConfig
from Network_Security.components.data_transformation import DataTransformation
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
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
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(data_ingestion_artifact)
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("Initiate the data validation")
        data_validation.initiate_data_validation()
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed.")
        print(data_validation_artifact)
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        logging.info("Data Transformation Started.")
        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Data Transformation Completed.")


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
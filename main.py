
from src.components.data_ingestion import DataIngesetionConfig,  DataIngestionArtifact, DataIngestion
from src.components.data_transformation import DataTransformationConfig, DataTransformationArtifact, DataTransformation

if __name__ == "__main__":
    
    data_ingestion_config = DataIngesetionConfig()
    data_ingestion = DataIngestion(data_ingestion_config)
    data_ingestion_artifact: DataIngestionArtifact = data_ingestion.initiate_data_ingestion()
    print(data_ingestion_artifact)

    data_transformation_config = DataTransformationConfig()
    data_transformation = DataTransformation(data_transformation_config)
    data_transformation_artifact:DataTransformationArtifact = data_transformation.initiate_data_transformation(data_ingestion_artifact)
    print(data_transformation_artifact)    
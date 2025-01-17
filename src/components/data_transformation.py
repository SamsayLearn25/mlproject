from src.exception import CustomException
from src.logger import logging

import sys
import pandas as pd
import numpy as np
import os
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.components.data_ingestion import DataIngestionArtifact
from src.utils import save_object, save_data

from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path:str = os.path.join('artifacts', 'preprocessor.pkl')
    train_data_path:str = os.path.join('artifacts', 'transformed', 'train.csv')
    test_data_path:str = os.path.join('artifacts', 'transformed', 'test.csv')

@dataclass
class DataTransformationArtifact:
    preprocessor_obj_file_path:str
    train_data_path:str
    test_data_path:str


class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig):
        self.data_transformation_config = data_transformation_config
        

    def get_data_transformer_object(self):

        try:
            numerical_columns = ['writing_score', 'reading_score']
            categorical_columns = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            logging.info("Numerical Columns Standard scaling completed")

            cat_pipeline =Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    #("scaler", StandardScaler())
                ]
            )

            logging.info("Categorical Columns Encoding Completed")

            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline", numerical_pipeline,  numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact)->DataTransformationArtifact:
        
        try:
            data_transformer_obj = self.get_data_transformer_object()

            df_train = pd.read_csv(data_ingestion_artifact.train_data_path)
            df_test = pd.read_csv(data_ingestion_artifact.test_data_path)

            target_column = "math_score"
            numeric_columns = ["writing_score", "reading_score"]
            
            df_train_input = df_train.drop(target_column, axis=1)
            df_test_input = df_test.drop(target_column, axis=1)

            train_target = df_train[target_column]
            test_target = df_test[target_column]

            logging.info("Apply Preprocessing")
            logging.info(str(df_train_input.shape)+" "+str(df_test_input.shape))
            train_transformed = data_transformer_obj.fit_transform(df_train_input)
            test_transformed = data_transformer_obj.transform(df_test_input)
            logging.info(f"Preprocessing completed with shape {train_transformed.shape} {test_transformed.shape}")

            train_arr = np.c_[train_transformed, np.array(train_target)]
            test_arr = np.c_[test_transformed, np.array(test_transformed)]

            logging.info(str(train_arr.shape)+" "+str(test_arr.shape))

            logging.info("Saving Transformed data")
            save_data(self.data_transformation_config.train_data_path, train_arr)
            save_data(self.data_transformation_config.test_data_path, test_arr)

            logging.info("Saving preprocessed object")

            save_object(self.data_transformation_config.preprocessor_obj_file_path, data_transformer_obj)
            logging.info("Saved preprocessed object")
            return DataTransformationArtifact(
                preprocessor_obj_file_path= self.data_transformation_config.preprocessor_obj_file_path,
                train_data_path=self.data_transformation_config.train_data_path,
                test_data_path=self.data_transformation_config.test_data_path
            )


        except Exception as e:
            raise CustomException(e, sys)

        

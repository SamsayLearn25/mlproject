import os, sys 

from src.components.data_transformation import DataTransformationArtifact
from src.exception import CustomException
from src.logger import logging
from src.utils import *

from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from src.utils import *

from dataclasses import dataclass

@dataclass
class ModelTrainerConfig:
    model_path: str = os.path.join("artifacts", "trained_models", "model.pkl")
    model_score_path: str = os.path.join("artifacts", "trained_models", "model_score.txt")
    preprocessor_path: str = os.path.join("artifacts", "trained_models", "preprocessor.pkl")

@dataclass
class ModelScore:
    r2: float

@dataclass
class ModelTrainerArtifact:
    model_path: str
    model_score: ModelScore
    preprocessor_path: str

class ModelTrainer:

    def __init__(self, model_trainer_config: ModelTrainerConfig):

        self.model_trainer_config = model_trainer_config

    def get_models(self):

        models = {
            "AdaBoostRegressor": AdaBoostRegressor(),
            "GradientBoostingRegressor": GradientBoostingRegressor(),
            "RandomForestRegressor": RandomForestRegressor(),
            "LinearRegression": LinearRegression(),
            "DecisionTreeRegressor": DecisionTreeRegressor(),
            "KNeighborsRegressor": KNeighborsRegressor(),
        }

        return models
    
    def initiate_model_trainer(self, data_transformation_artifact: DataTransformationArtifact)->ModelTrainerArtifact:

        try:
            logging.info("Load Transformed Data")
            train = load_data(data_transformation_artifact.train_data_path)
            test = load_data(data_transformation_artifact.test_data_path)
            train_x, train_y = train[:, :-1], train[:, -1]
            test_x, test_y = test[:, :-1], test[:, -1]
            print(train_x.shape, train_y.shape, test_x.shape, test_y.shape)
            logging.info("Data Loaded Successfully")

            logging.info("Training Models")
            models = self.get_models()
            metrics = evaluate_models(models, train_x, train_y, test_x, test_y)

            best_model_score = sorted(list(metrics.values()))[-1]
            idx = list(metrics.values()).index(best_model_score)
            best_model_name = sorted(list(metrics.keys()))[idx]
            logging.info(f"Best Model found {best_model_name}: {best_model_score}")
            print(best_model_name, best_model_score)

            best_model = models[best_model_name]
            save_object(self.model_trainer_config.model_path, best_model)
            preprocessor = load_object(data_transformation_artifact.preprocessor_obj_file_path)
            save_object(self.model_trainer_config.preprocessor_path, preprocessor)
            logging.info("Model Training Completed")

            return ModelTrainerArtifact(    
                self.model_trainer_config.model_path,
                ModelScore(best_model_score),
                self.model_trainer_config.preprocessor_path
            )

        except Exception as e:
            raise CustomException(e, sys)

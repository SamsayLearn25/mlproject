
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import os, sys
from src.utils import load_object

class PredictionPipeline:

    def __init__(self):
        self.model = load_object(os.path.join("artifacts", "trained_models", "model.pkl"))
        self.preprocessor = load_object(os.path.join("artifacts", "trained_models", "preprocessor.pkl"))

    def predict(self, features):

        try:
            print(features)
            data = self.preprocessor.transform(features)
            pred = self.model.predict(data)
            return pred

        except Exception as e:
            raise CustomException(e, sys)
        

class CustomData:

    def __init__(self,
                 gender: str,
                 race_ethnicity: int,
                 parental_level_of_education,
                 lunch: str,
                 test_preparation_course: str,
                 reading_score: int,
                 writing_score: int
                 ):
        
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_dataframe(self):
        try:
            df = pd.DataFrame()
            df["gender"] = [self.gender]
            df["race_ethnicity"] = [self.race_ethnicity]
            df["parental_level_of_education"] = [self.parental_level_of_education]
            df["lunch"] = [self.lunch]
            df["test_preparation_course"] = [self.test_preparation_course]
            df["reading_score"] = [self.reading_score]
            df["writing_score"] = [self.writing_score]
            # print(self.gender, self.race_ethnicity, self.parental_level_of_education,
            #       self.lunch, self.test_preparation_course, self.reading_score, self.writing_score)
            # print(df)
            return df
        except Exception as e:
            raise CustomException(e, sys)
        
    




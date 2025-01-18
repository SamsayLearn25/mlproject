import numpy as np
import os, sys
from src.exception import CustomException
import pickle
import pandas as pd
import numpy as np


def save_object(file_name: str, obj: object):

    try:
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name, "wb") as f:
            pickle.dump(obj, f)

    except Exception as e:
        raise CustomException(e, sys)
    

def save_data(file_name: str, data: np.array):

    try:
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        
        np.save(file_name, data)
    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_name: str):

    try:
        
        with open(file_name, "rb") as f:
            return pickle.load(f)

    except Exception as e:
        raise CustomException(e, sys)
    

def load_data(file_name: str):

    try:
       
        return np.load(file_name)
    except Exception as e:
        raise CustomException(e, sys)
    
from sklearn.metrics import r2_score
    
def evaluate_models(models, train_x, train_y, test_x, test_y):

        metrics = {}
        for model_name , model in models.items():
            #print(model_name, model)

            model.fit(train_x, train_y)

            # Corrected line, only pass test_x to predict
            y_pred = model.predict(test_x)

            r2 = r2_score(y_pred=y_pred, y_true=test_y)

            metrics[model_name] = r2

        return metrics
    

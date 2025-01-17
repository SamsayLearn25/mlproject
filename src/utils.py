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
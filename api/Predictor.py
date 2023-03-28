import numpy as np
import pickle
from api import InputModel


def predict_diabetes(data: InputModel):
    with open("Data/model.pkl", "rb") as f:
        model = pickle.load(f)

    input_data = np.array([list(data.dict().values())])
    prediction = model.predict(input_data)
    return prediction.tolist()[0]

import pickle
import json
from pandas import json_normalize


# define your model loading function
def model_fn(model_dir):
    print("Loading model from: {}".format(model_dir))

    # load the model from the pickle file
    with open(f"{model_dir}/model.pickle", "rb") as f:
        model = pickle.load(f)
    return model


# define your input processing function
def input_fn(request_body, request_content_type):
    print("Processing request_body: {}".format(request_body))

    if request_content_type == "application/json":
        input_dict = json.loads(request_body)
        input_data = json_normalize(input_dict)
        return input_data
    else:
        raise ValueError(
            f"Request content type {request_content_type} not supported by this script."
        )


# define your output processing function
def output_fn(predictions, response_content_type):
    if response_content_type == "application/json":
        output_data = {"output": predictions.tolist()}
        return output_data
    else:
        raise ValueError(
            f"Response content type {response_content_type} not supported by this script."
        )


# define your prediction function
def predict_fn(input_data, model):
    print("Predicting with input_data: {}".format(input_data))

    # use predict_proba to make predictions
    predictions = model.predict_proba(input_data)
    return predictions

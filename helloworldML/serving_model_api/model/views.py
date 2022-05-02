import pickle
from os import abort
from flask import Blueprint, request, jsonify

from serving_model_api.model import models
from serving_model_api.config import FILE_NAME

models_blueprint = Blueprint('model', __name__)


@models_blueprint.route('/')
def home():
    return "Welcome to Inbar's hello world ML"


@models_blueprint.route('/predict', methods=['POST'])
def prediction():
    # We assuming the given data is correct and there is no need to validate it
    if not models.IrisModel.json_request_validation(request.json):
        abort(400)

    iris = models.IrisModel(request.json)

    with open(FILE_NAME, 'rb') as file:
        load_model = pickle.load(file)
        result = load_model.predict([[iris.sepal_length, iris.sepal_width, iris.petal_length, iris.petal_width]])
        return jsonify({'prediction': result[0]}), 200
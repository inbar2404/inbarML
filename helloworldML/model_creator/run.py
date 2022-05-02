from model_creator.service.models_creator import models_creator

if __name__ == "__main__":
    creator = models_creator("Iris", ['species'])
    creator.create('../serving_model_api/iris_model.sav')
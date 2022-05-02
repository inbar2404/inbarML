from flask import Flask

from serving_model_api.model.views import models_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(models_blueprint)
    return app
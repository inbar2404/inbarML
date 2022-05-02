import os
import pickle

import pandas as pd
from pip._vendor import requests

from model_creator.config import DATASETS


def percentage(part, whole):
  return 100 * float(part)/float(whole)


def save_pickle_file(model, file_location: str):
    pickle.dump(model, open(file_location, 'wb'))


def load_dataset_url(dataset_name: str):
    file_request = requests.head(DATASETS[dataset_name])
    if file_request.status_code == requests.codes.ok:
        return pd.read_csv(DATASETS[dataset_name])
    else:
        raise Exception("File not exist")
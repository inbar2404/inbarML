from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score

from model_creator.config import RANDOM_STATE_SEED, KFOLDS_SPLITS, EXEEDED_PRECENTAGE_OF_MISSING_DATA
from model_creator.service.models_factory import models_factory
from model_creator.utils import percentage, load_dataset_url, save_pickle_file


class models_creator:
    def __init__(self, dataset_name: str, dependent_variables):
        self.dataset = load_dataset_url(dataset_name)
        self.dependent_variables = dependent_variables

    def handle_missing_data(self):
        missing_data_amount: int = self.dataset.isnull().sum().sum()
        total_data_amount: int = self.dataset.value_counts().sum()
        percentage_of_missing_data: float = percentage(missing_data_amount, total_data_amount)

        if percentage_of_missing_data > EXEEDED_PRECENTAGE_OF_MISSING_DATA:
              raise Exception("Too much missing data")
        elif percentage_of_missing_data != 0:
              self.dataset.dropna()

    def find_best_model(self, dependent_variables_train, independent_variables_train):
        models = models_factory.create_models()
        best_model = None
        cv_best_result = None

        # Check the accuracy for each algorithm to find out which one is the best to use in this case
        for name, model in models:
            kfold = StratifiedKFold(n_splits=KFOLDS_SPLITS, random_state=RANDOM_STATE_SEED, shuffle=True)
            cv_results = cross_val_score(model, dependent_variables_train, independent_variables_train, cv=kfold,
                                         scoring='accuracy')

            if cv_best_result is None or cv_best_result < cv_results.mean():
                cv_best_result = cv_results.mean()
                best_model = model

        return best_model

    def create(self, pickle_file_location: str):
        self.handle_missing_data()

        dependent_variables_train, dependent_variables_test, independent_variables_train, independent_variables_test = \
            train_test_split(self.dataset.drop(self.dependent_variables, axis=1),
                             self.dataset.get(self.dependent_variables),
                             random_state=RANDOM_STATE_SEED)

        model = self.find_best_model(dependent_variables_train, independent_variables_train)
        model.fit(dependent_variables_train, independent_variables_train)  # Training our model

        # Here we check the predection according to the test data
        prediction = model.predict(dependent_variables_test)
        print(f'Test Accuracy: {accuracy_score(independent_variables_test, prediction)}')

        save_pickle_file(model, pickle_file_location)

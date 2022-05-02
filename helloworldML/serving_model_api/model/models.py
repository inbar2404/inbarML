class IrisModel():
    def __init__(self, json_request):
        self.sepal_length = json_request['sepal_length']
        self.sepal_width = json_request['sepal_width']
        self.petal_length = json_request['petal_length']
        self.petal_width = json_request['petal_width']

    def json_request_validation(json_request):
        if json_request:
            variables_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
            for var in variables_names:
                if var not in json_request:
                    return False
            return True
        return False
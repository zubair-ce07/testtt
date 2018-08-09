class CalculatedResult:
    __results = []

    def __init__(self):
        pass

    @staticmethod
    def get_data():
        return CalculatedResult.__results

    @staticmethod
    def save_results(type_, data):
        CalculatedResult.__results.append({'type': type_, 'data': data})

class CalculatedResult:
    results = []

    @staticmethod
    def get_data():
        return CalculatedResult.results

    @staticmethod
    def save_results(type_, data):
        CalculatedResult.results.append({'type': type_, 'data': data})

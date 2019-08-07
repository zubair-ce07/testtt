class Report:
    """ Report utility to print calculation's result """
    @staticmethod
    def print_report(result):
        print(
            f"Month           : {result.month}\n"
            f"Year            : {result.year}\n"
            f"Min-Temp (mean) : {result.min_temp}\n"
            f"Mean-Temp (mean) : {result.avg_temp}\n"
            f"Max-Temp (mean) : {result.max_temp}\n"
        )

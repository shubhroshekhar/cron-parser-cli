class CronResultPrinter:
    """
    A class to format and print the result of a cron job.
    """
    def __init__(self, result):
        self.result = result

    def format_result_14(self):
        for field, values in self.result.items():
            print(f"{field.ljust(14)}{' '.join(map(str, values))}")
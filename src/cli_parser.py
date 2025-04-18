from src.cron_field import CronField

class CronParser:
    """
    A class to parse a cron expression and expand its fields.
    The cron expression is expected to be in the format:
    minute hour day_of_month month day_of_week command
    where:
    - minute: 0-59
    - hour: 0-23
    - day_of_month: 1-31
    - month: 1-12
    - day_of_week: 0-6
    - command: The command to be executed
    """
    def __init__(self, cron_string):
        self.cron_string = cron_string
        self.fields = [
            ('minute', 0, 59),
            ('hour', 0, 23),
            ('day of month', 1, 31),
            ('month', 1, 12),
            ('day of week', 0, 6)
        ]

    def parse(self):
        parts = self.cron_string.strip().split()
        if len(parts) < 6:
            raise ValueError("Cron expression must have at least 6 fields")
        
        result = {}
        for i, (name, min_val, max_val) in enumerate(self.fields):
            field_expr = parts[i]
            field = CronField(name, field_expr, min_val, max_val)
            result[name] = field.expand()

        result["command"] = [' '.join(parts[5:])]
        return result
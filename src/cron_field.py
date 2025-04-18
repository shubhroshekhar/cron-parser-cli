class CronField:
    def __init__(self, name, expression, min_val, max_val):
        """
        Initialize a CronField object.
        :param name: Name of the field (e.g., minute, hour, day of month, etc.)
        :param expression: Cron expression for the field.
        :param min_val: Minimum valid value for the field.
        :param max_val: Maximum valid value for the field.
        """
        self.name = name
        self.expression = expression
        self.min_val = min_val
        self.max_val = max_val

    def expand(self):
        """
        Expand the cron expression into a list of valid values.
        :return: A sorted list of valid values based on the cron expression.
        :raises ValueError: If the expression is invalid or out of range.
        """
        result = set()
        for part in self.expression.split(','):
            result.update(self._parse_part(part.strip()))
        values = sorted(result)
        self.__validate(values)
        return values

    def _parse_part(self, part):
        # Handle */N or A-B/N
        if '/' in part:
            return self.__parse_step(part)

        # Handle * case
        elif part == '*':
            return self.__parse_asterisk()
        
        # Handle A-B range
        elif '-' in part:
            return self.__parse_range(part)

        # Single value
        else:
            return self.__parse_single_value(part)

    def __parse_asterisk(self):
        return range(self.min_val, self.max_val + 1)

    def __parse_range(self, part):
        start, end = map(int, part.split('-'))
        return range(start, end + 1)

    def __parse_single_value(self, part):
        return [int(part)]

    def __parse_step(self, part):
        base, step = part.split('/')
        step = int(step)

        # Case: */N
        if base == '*':
            start = self.min_val
            end = self.max_val
        # Case: A-B/N
        elif '-' in base:
            start, end = map(int, base.split('-'))
        # Case: N/M (rare, but be cautious)
        else:
            start = int(base)
            end = self.max_val

        return range(start, end + 1, step)
    
    def __validate(self, values) -> None:
        """
        Validate the expanded values against the field's min and max values.
        :param values: List of expanded values to validate.
        :raises ValueError: If any value is out of the field's range.
        """
        for value in values:
            if not (self.min_val <= value <= self.max_val):
                raise ValueError(f"Value {value} is out of range for this field")

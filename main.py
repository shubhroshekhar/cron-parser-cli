import sys
from src.cli_parser import CronParser
from src.cli_result_printer import CronResultPrinter

def main():
    """Main function to parse a cron expression from command line arguments.
    It expects the cron expression to be provided as the first argument.
    It will print the parsed fields and their expanded values.
    Usage:
        python main.py "*/5 * * * * /path/to/command"
    """
    if len(sys.argv) < 2:
        print("Error: No cron expression provided.")
        sys.exit(1)
    
    expression = sys.argv[1]
    try:
        parser = CronParser(expression)
        result = parser.parse()
        printer = CronResultPrinter(result)
        printer.format_result_14()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)







if __name__ == "__main__":
    main()
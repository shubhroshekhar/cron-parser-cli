# Cron Parser CLI

A command-line tool to parse and expand cron expressions into their individual components.

## Features

- Parses cron expressions into minute, hour, day of month, month, and day of week fields.
- Validates cron expressions for correctness.
- Supports ranges, steps, and lists in cron fields.
- Outputs the parsed fields in a human-readable format.

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:shubhroshekhar/cron-parser-cli.git
   ```

## Usage

Run the CLI tool with a cron expression as an argument:
```bash
python3 main.py "*/15 0 1,15 * 1-5 /usr/bin/find"
```


### Example Output
```plaintext
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
```

## Testing

Run the unit tests to ensure everything works as expected:
```bash
python3 -m unittest discover tests
```

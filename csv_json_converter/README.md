# CSV to JSON Converter

A small Python script that converts a CSV file with a header row into a formatted JSON array.

It uses only Python's standard library, so no third-party packages are required.

## Requirements

- Python 3.8 or newer
- A CSV file whose first row contains column headers

## Usage

1. Open `csv_json_converter.py`.
2. Update the `input_file` path in `main()` to point to your CSV file:

   ```python
   input_file = Path(r"C:\path\to\your-file.csv")
   ```

3. Run the script from the project directory:

   ```powershell
   python csv_json_converter.py
   ```

The JSON file is created alongside the source CSV using the same name. For example:

```text
data.csv  ->  data.json
```

## Input and output

Given this CSV:

```csv
name,age,city
Ada,31,London
Linus,55,Helsinki
```

The generated JSON will be:

```json
[
    {
        "name": "Ada",
        "age": "31",
        "city": "London"
    },
    {
        "name": "Linus",
        "age": "55",
        "city": "Helsinki"
    }
]
```

CSV values are preserved as strings. Unicode text is kept readable in the JSON output.

## Error handling

The script reports helpful messages when the input file is missing, permissions prevent access, the CSV is malformed, or the CSV has no header row.

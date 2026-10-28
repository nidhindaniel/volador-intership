
import csv
import json
from pathlib import Path


def read_csv(filename):
    
    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("The CSV file is empty or has no header row.")

        records = list(reader)

    return records


def write_json(filename, records):

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)


def convert_csv_to_json(input_file, output_file):

    try:
        records = read_csv(input_file)
        write_json(output_file, records)

        print("Conversion successful!")
        print(f"Input file:  {input_file}")
        print(f"Output file: {output_file}")
        print(f"Total records converted: {len(records)}")

    except FileNotFoundError:
        print(f"Error: Could not find the file '{input_file}'.")

    except PermissionError:
        print("Error: Permission denied while accessing a file.")

    except (csv.Error, ValueError) as error:
        print(f"Error reading CSV: {error}")

    except OSError as error:
        print(f"File operation failed: {error}")


def main():

    input_file = Path(
        r"D:\VSCODE PROJECTS\volador_internship\train_ctrUa4K.csv"
    )

    output_file = input_file.with_suffix(".json")

    convert_csv_to_json(input_file, output_file)


if __name__ == "__main__":
    main()

import csv
import json

# Path to the CSV file
csv_file_path = './m2.5 - Code Refactoring II - Sheet1.csv'

# The output JSON file
json_file_path = 'exported_data.json'

# Container for the processed data
data_to_export = []

# Open the CSV file and read rows into a dictionary, only including rows where "Refactored?" is "FAILED"
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # if row["Refactored?"] == "FAILED":  # Check if the "Refactored?" column is "FAILED"
        data_to_export.append({
            "path": row["file_path"],
            "deprecatedMethod": row["line_content"]
        })  # AI-GEN - CursorAI with GPT4

# Write the data to a JSON file
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(data_to_export, json_file, indent=4)

print(f"Data has been exported to '{json_file_path}'")

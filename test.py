import csv
import json

data=[]

with open(('./data/raw/salaries (2).csv'),'r') as csvf:
    csvreader=csv.DictReader(csvf)
    for row in csvreader:
        data.append(row)
with open('./data/raw/data.json', 'w') as json_file:
        # Use json.dumps() to convert the data to a JSON string with indentation
        json_file.write(json.dumps(data, indent=4))

print(f"CSV file '{'./data/raw/salaries (2).csv'}' has been converted to JSON file '{'./data/raw/data.json'}'")

# Example usa
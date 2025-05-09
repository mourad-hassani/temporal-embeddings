import json
import csv
import argparse

from tqdm import tqdm

def json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['sent0', 'sent1', 'score'])
        
        for item in tqdm(data, desc="Converting JSON to CSV"):
            item = [field.replace('\n', ' ') if isinstance(field, str) else field for field in item]
            writer.writerow(item)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert JSON to CSV.')
    parser.add_argument('json_file_path', type=str, help='Path to the input JSON file')
    parser.add_argument('csv_file_path', type=str, help='Path to the output CSV file')
    
    args = parser.parse_args()
    
    json_to_csv(args.json_file_path, args.csv_file_path)
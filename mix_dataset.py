import json
import random
import argparse

def mix_json_files(file1, file2, output_file):
    with open(file1, 'r') as f:
        data1 = json.load(f)
    
    with open(file2, 'r') as f:
        data2 = json.load(f)
    
    combined_data = data1 + data2
    
    random.shuffle(combined_data)
    
    with open(output_file, 'w') as f:
        json.dump(combined_data, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mix two JSON files and output the result to a new file.')
    parser.add_argument('file1', type=str, help='Path to the first JSON file')
    parser.add_argument('file2', type=str, help='Path to the second JSON file')
    parser.add_argument('output_file', type=str, help='Path to the output JSON file')
    
    args = parser.parse_args()
    
    mix_json_files(args.file1, args.file2, args.output_file)
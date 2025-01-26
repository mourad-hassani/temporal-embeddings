import pandas as pd
import argparse

from tqdm import tqdm

from temporal_embeddings.data_utils.utils.compute_similarity_expressions import compute_similarity_expressions
from temporal_embeddings.data_utils.utils.mappings.date_to_text import date_to_text

def create_training_dataset(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    new_rows = []
    
    for index, row in tqdm(df.iterrows()):

        sentences = eval(row["sentences"])
        values = eval(row["values"])
        current_dates = eval(row["current_dates"])

        first_value = values[0]
        first_current_date = current_dates[0]
        first_sentence = f"[CLS] {sentences[0]} [SEP] {date_to_text(first_current_date)} [SEP]"
        
        if len(sentences) > 1:
            second_value = values[1]
            second_current_date = current_dates[1]
            second_sentence = f"[CLS] {sentences[1]} [SEP] {date_to_text(second_current_date)} [SEP]"
        
            new_rows.append([first_sentence, second_sentence, compute_similarity_expressions(first_value, second_value, first_current_date, second_current_date)])
            
            for i in range(4):
                random_row = df.sample().iloc[0]
                
                random_value = eval(random_row["values"])[0]
                random_current_date = eval(random_row["current_dates"])[0]
                random_sentence = eval(random_row["sentences"])[0]
                random_sentence = f"[CLS] {random_sentence} [SEP] {date_to_text(random_current_date)} [SEP]"
                
                new_rows.append([first_sentence, random_sentence, compute_similarity_expressions(first_value, random_value, first_current_date, random_current_date)])
    
    new_df = pd.DataFrame(new_rows, columns=['First String', 'Second String', 'Similarity'])
    new_df.to_csv(output_csv, index=False)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create a training dataset from input CSV.')
    parser.add_argument('input_csv', type=str, help='Path to the input CSV file')
    parser.add_argument('output_csv', type=str, help='Path to the output CSV file')
    
    args = parser.parse_args()
    
    create_training_dataset(args.input_csv, args.output_csv)

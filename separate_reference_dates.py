import pandas as pd
import argparse

def separate_reference_dates(csv_file_path: str, output_file_path: str) -> None:
    df = pd.read_csv(csv_file_path, header=None, names=['sent0', 'sent1', 'score'])

    df = df[1:]
    
    def extract_date_and_clean_sent(sent):
        parts = sent.split('[SEP]')
        if len(parts) >= 3:
            date = parts[1].strip()
            cleaned_sent = parts[0].replace('[CLS]', '').strip()
            return date, cleaned_sent
        return None, sent
    
    df[['sent1_date', 'sent1']] = df['sent1'].apply(lambda x: pd.Series(extract_date_and_clean_sent(x)))
    df[['sent0_date', 'sent0']] = df['sent0'].apply(lambda x: pd.Series(extract_date_and_clean_sent(x)))

    df = df[['sent0', 'sent0_date', 'sent1', 'sent1_date', 'score']]
    
    df.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Separate reference dates from sentences in a CSV file.')
    parser.add_argument('csv_file_path', type=str, help='Path to the CSV file')
    parser.add_argument('output_file_path', type=str, help='Path to save the output CSV file')
    args = parser.parse_args()

    separate_reference_dates(args.csv_file_path, args.output_file_path)

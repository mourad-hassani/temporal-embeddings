import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])

def sum_of_string_lengths(column):
    total_length = 0
    for item in column:
        total_length += len(item)
    return total_length

# Assuming the second column is named 'column2'
total_length = sum_of_string_lengths(df.iloc[:, 1])
print(f'Total length of strings in the second column: {total_length}')
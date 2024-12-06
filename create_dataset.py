import argparse

from temporal_embeddings.data_utils.temporal_index.create_index import create_index

parser = argparse.ArgumentParser(description="Commnad line program to create the training dataset")

parser.add_argument("-n", "--num_rows", type=int)

args = parser.parse_args()

create_index(args.num_rows)
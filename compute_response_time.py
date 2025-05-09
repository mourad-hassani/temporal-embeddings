import argparse

from temporal_embeddings.inference.compute_response_time import evaluate_model

parser = argparse.ArgumentParser(description="Compute response time for a given model and sentence.")
parser.add_argument("model_name", type=str, help="The name of the model to use.")
parser.add_argument("sentence", type=str, help="The sentence to encode.")
args = parser.parse_args()

evaluate_model(args.model_name, args.sentence)
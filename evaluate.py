from temporal_embeddings.evaluation.evaluate import evaluate_model
import argparse

def main():
    parser = argparse.ArgumentParser(description="Evaluate a model")
    parser.add_argument("model_name", type=str, help="Name of the model to evaluate")
    args = parser.parse_args()

    evaluate_model(args.model_name)

if __name__ == "__main__":
    main()
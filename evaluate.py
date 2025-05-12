from temporal_embeddings.evaluation.evaluate import evaluate_model
import argparse

def main():
    parser = argparse.ArgumentParser(description="Evaluate a model")
    parser.add_argument("model_name", type=str, help="Name of the model to evaluate")
    parser.add_argument("model_path", type=str, help="Path to the model .pth file")
    args = parser.parse_args()

    evaluate_model(args.model_name, args.model_path)

if __name__ == "__main__":
    main()
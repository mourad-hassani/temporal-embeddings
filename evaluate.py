from temporal_embeddings.evaluation.evaluate import evaluate_model
import argparse

def main():
    parser = argparse.ArgumentParser(description="Evaluate a model")
    parser.add_argument("model_name", type=str, help="Name of the model to evaluate")
    parser.add_argument("model_path", type=str, help="Path to the model .pth file")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for evaluation")
    parser.add_argument("--max_seq_len", type=int, default=128, help="Maximum sequence length for evaluation")
    args = parser.parse_args()

    evaluate_model(args.model_name, args.model_path, args.batch_size, args.max_seq_len)

if __name__ == "__main__":
    main()
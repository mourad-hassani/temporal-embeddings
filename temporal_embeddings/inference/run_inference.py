from temporal_embeddings.inference.inference import Inference
import json

def run_inference():
    first_sentences = []
    second_sentences = []
    ground_truth = []

    with open("data/base_dataset/asymmetric_dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for element in data:
            first_sentences.append(element[0])
            second_sentences.append(element[1])
            ground_truth.append(element[2])

    inference: Inference = Inference(first_sentences, second_sentences, ground_truth)
    
    output = inference.evaluate()

    outputs = {}

    for sent1, sent2, similarity, ground_truth in zip(output["sent1"], output["sent2"], output["similarity"], output["ground_truth"]):
        outputs[similarity] = {"sent1": sent1, "sent2": sent2}

    outputs = {key: outputs[key] for key in sorted(outputs)}

    for k, v in outputs.items():
        print(f"similarity: {k} => {v["sent1"]}, {v["sent2"]}")

if __name__ == "__main__":
    run_inference()
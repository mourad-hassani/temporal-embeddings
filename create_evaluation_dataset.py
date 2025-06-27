import json
from pathlib import Path
import argparse
import random

def create_evaluation_dataset(dataset_name):
    if dataset_name.lower().startswith("menat_qa"):
        main_folder = Path("data/evaluation/menat_qa")
        input_path = main_folder / Path("MenatQA.json")
        
        if dataset_name.lower() == "menat_qa":
            output_file = main_folder / "processed_menat_qa.json"
        
        elif dataset_name.lower() == "menat_qa_granularity":
            output_file = main_folder / "processed_menat_qa_granularity.json"
        
        elif dataset_name.lower() == "menat_qa_counterfactual":
            output_file = main_folder / "processed_menat_qa_counterfactual.json"
        
        elif dataset_name.lower() == "menat_qa_expand":
            output_file = main_folder / "processed_menat_qa_expand.json"
        
        elif dataset_name.lower() == "menat_qa_narrow":
            output_file = main_folder / "processed_menat_qa_narrow.json"
        
        else:
            print(f"Dataset '{dataset_name}' is not supported.")
            return

        main_folder.mkdir(parents=True, exist_ok=True)

        with input_path.open("r", encoding="utf-8") as infile:
            menat_data = json.load(infile)

        processed_data = []
        
        for item in menat_data:
            if dataset_name.lower() == "menat_qa_granularity" and item.get("type") != "granularity":
                continue
            
            if dataset_name.lower() == "menat_qa_counterfactual" and item.get("type") != "counterfactual":
                continue
            
            if dataset_name.lower() == "menat_qa_expand" and item.get("type") != "expand":
                continue
            
            if dataset_name.lower() == "menat_qa_narrow" and item.get("type") != "narrow":
                continue

            question = item.get("question", "")
            
            paragraphs = [ctx["text"] for ctx in item["context"]]
            if len(paragraphs) <= 3:
                continue
            
            answer = item.get("annotated_para", "")
            answer_index = next((i for i, p in enumerate(paragraphs) if answer in p), -1)

            entry = {
                "question": question,
                "paragraphs": paragraphs,
                "answer": [answer_index] if answer_index >= 0 else [0]
            }
            
            processed_data.append(entry)

        with output_file.open("w", encoding="utf-8") as outfile:
            json.dump(processed_data, outfile, indent=2, ensure_ascii=False)

        if dataset_name.lower() == "menat_qa":
            print(f"Processed dataset saved to: {output_file}")
        
        else:
            print(f"Processed filtered dataset saved to: {output_file}")

    elif dataset_name.lower().startswith("ts_retriever"):
        base = Path("data/evaluation/ts_retriever")
        query_path = base / "query.json"
        doc_path = base / "doc.json"
        output_path = base / "processed_ts_retriever.json"

        with query_path.open("r", encoding="utf-8") as f:
            questions = json.load(f)

        with doc_path.open("r", encoding="utf-8") as f:
            paragraphs = json.load(f)

        output = []

        for _, q in enumerate(questions):
            answer_idx = []
            
            for positive_text in q["positive_text"]:
                answer_idx.append(paragraphs.index(positive_text))

            selected_paragraphs = [paragraphs[i] for i in answer_idx]

            other_indexes = [i for i in range(len(paragraphs)) if i not in answer_idx]

            sampled_indexes = random.sample(other_indexes, min(5, len(other_indexes)))
            selected_paragraphs += [paragraphs[i] for i in sampled_indexes]

            random.shuffle(selected_paragraphs)

            answer_idx = []
            for positive_text in q["positive_text"]:
                answer_idx.append(selected_paragraphs.index(positive_text))

            entry = {
                "question": q["query"],
                "paragraphs": selected_paragraphs,
                "answer": answer_idx,
            }

            output.append(entry)

        with output_path.open("w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"Processed dataset saved to: {output_path}")

    elif dataset_name.lower().startswith("human_annotated_test"):
        main_folder = Path("data/evaluation/time_sensitive_qa")
        input_path = main_folder / "human_annotated_test.json"
        output_file = main_folder / "processed_human_annotated_test.json"

        main_folder.mkdir(parents=True, exist_ok=True)

        with input_path.open("r", encoding="utf-8") as infile:
            data = json.load(infile)

        processed_data = []
        for item in data:
            paragraphs = item.get("paras", [])
            for q_pair in item.get("questions", []):
                question_text = q_pair[0]
                answers = q_pair[1]
                # If there are multiple answers, process each one
                for ans in answers:
                    para_idx = ans.get("para", 0)
                    entry = {
                        "question": question_text,
                        "paragraphs": paragraphs,
                        "answer": [para_idx]
                    }
                    processed_data.append(entry)

        with output_file.open("w", encoding="utf-8") as outfile:
            json.dump(processed_data, outfile, indent=2, ensure_ascii=False)

        print(f"Processed dataset saved to: {output_file}")

    else:
        print(f"Dataset '{dataset_name}' is not supported.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process evaluation dataset.")
    parser.add_argument("dataset_name", type=str, help="Name of the dataset to process")
    args = parser.parse_args()
    create_evaluation_dataset(args.dataset_name)
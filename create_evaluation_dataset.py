import json
from pathlib import Path
import argparse

def create_evaluation_dataset(dataset_name):
    if dataset_name.lower().startswith("menat_qa"):
        main_folder = Path("data/evaluation/menat_qa")
        input_path = main_folder / Path("MenatQA.json")
        
        if dataset_name.lower() == "menat_qa":
            output_file = main_folder / "processed_menatqa.json"
       
        elif dataset_name.lower() == "menat_qa_granularity":
            output_file = main_folder / "processed_menatqa_granularity.json"
        
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
            
            question = item.get("updated_question", item["question"])
            paragraphs = [ctx["text"] for ctx in item["context"]]
            answer = item.get("annotated_para", "")
            answer_index = next((i for i, p in enumerate(paragraphs) if answer in p), -1)

            entry = {
                "question": question,
                "paragraphs": paragraphs,
                "answer": answer_index if answer_index >= 0 else 0
            }
            
            processed_data.append(entry)

        with output_file.open("w", encoding="utf-8") as outfile:
            json.dump(processed_data, outfile, indent=2, ensure_ascii=False)

        if dataset_name.lower() == "menat_qa":
            print(f"Processed dataset saved to: {output_file}")
        
        else:
            print(f"Processed granularity dataset saved to: {output_file}")

    else:
        print(f"Dataset '{dataset_name}' is not supported.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process evaluation dataset.")
    parser.add_argument("dataset_name", type=str, help="Name of the dataset to process")
    args = parser.parse_args()
    create_evaluation_dataset(args.dataset_name)
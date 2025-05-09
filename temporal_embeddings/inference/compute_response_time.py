import time
import argparse

from sentence_transformers import SentenceTransformer
from mistralai import Mistral

from temporal_embeddings.evaluation.utils.evaluation.temporal_bert.inference import Inference

def evaluate_model(model_name: str, sentence: str):
    if model_name == "salesforce":
        model_name = "Salesforce/SFR-Embedding-Mistral"
        model = SentenceTransformer(model_name, trust_remote_code=True)
        start_time = time.time()
        _ = model.encode(sentence)
        end_time = time.time()
        print(f"Response time: {end_time - start_time} seconds")
    
    if model_name == "alibaba":
        model = SentenceTransformer("Alibaba-NLP/gte-Qwen2-7B-instruct", trust_remote_code=True)
        model.max_seq_length = 8192
        start_time = time.time()
        _ = model.encode(sentence)
        end_time = time.time()
        print(f"Response time: {end_time - start_time} seconds")

    if model_name == "mistral":
        api_key: str = "OeZfwmPee7UPF0QCeOXd1Q6g1ea78JIz"
        client: Mistral = Mistral(api_key)
        start_time = time.time()
        _ = client.embeddings.create(model="mistral-embed", inputs=sentence).data
        end_time = time.time()
        print(f"Response time: {end_time - start_time} seconds")

    if model_name == "bge":
        model = SentenceTransformer("BAAI/bge-large-en", trust_remote_code=True)
        start_time = time.time()
        _ = model.encode(sentence, convert_to_tensor=True, normalize_embeddings=True)
        end_time = time.time()
        print(f"Response time: {end_time - start_time} seconds")

    if model_name == "temporal_bert":
        inference: Inference = Inference()
        inference.set_sentences([sentence], ["09 august 2024"], [sentence], ["09 august 2024"], [0.0])
        model = SentenceTransformer("all-mpnet-base-v2", trust_remote_code=True)
        start_time = time.time()
        inference.evaluate()
        model.encode(sentence)
        end_time = time.time()
        print(f"Response time: {end_time - start_time} seconds")
from typing import List

import numpy as np

def compute_accuracy(first_list: List[int], second_list: List[List[float]], top_k: int) -> float:
    correct = 0
    
    for gt_idx, sim_scores in zip(first_list, second_list):
        top_k_indices = np.argsort(sim_scores)[-top_k:][::-1]

        correct += 1 if (len(set(gt_idx) & set(top_k_indices))) > 0 else 0
    
    return correct / len(first_list) if first_list else 0.0
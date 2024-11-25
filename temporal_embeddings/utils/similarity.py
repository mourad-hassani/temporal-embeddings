import torch
from torch import distributions

from temporal_embeddings.utils.math.tanh import tanh
from parameters import TEMPERATURE

def asymmetrical_kl_sim(mu1: torch.FloatTensor, std1: torch.FloatTensor, mu2: torch.FloatTensor, std2: torch.FloatTensor) -> torch.Tensor:
    """
    Computes the KL similarity between two normal distributions and returns a tensor with shape (batch_size)
    """

    p1 = distributions.normal.Normal(mu1, std1)
    p2 = distributions.normal.Normal(mu2, std2)

    distance = distributions.kl.kl_divergence(p1, p2).mean(dim=-1)
    
    similarity = 1 / (1 + distance)
    
    return similarity / TEMPERATURE
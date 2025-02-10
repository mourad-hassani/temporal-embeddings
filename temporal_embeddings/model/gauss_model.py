from dataclasses import dataclass
from datetime import datetime

import torch
import torch.nn as nn
from transformers import AutoModel, PreTrainedModel
from transformers.modeling_outputs import BaseModelOutput, ModelOutput

from temporal_embeddings.parameters.parameters import POSITIONAL_ENCODING_DIM

@dataclass
class GaussOutput(ModelOutput):
    mu: torch.FloatTensor = None
    std: torch.FloatTensor = None


class GaussModel(nn.Module):
    def __init__(self, model_name: str, gradient_checkpointing: bool = False) -> None:
        super().__init__()

        self.backbone: PreTrainedModel = AutoModel.from_pretrained(model_name)

        if gradient_checkpointing:
            self.backbone.gradient_checkpointing_enable()

        self.hidden_size: int = self.backbone.config.hidden_size

        self.w_mu = nn.Linear(self.hidden_size + POSITIONAL_ENCODING_DIM, self.hidden_size)
        self.w_var = nn.Linear(self.hidden_size + POSITIONAL_ENCODING_DIM, self.hidden_size)
        self.activation = nn.Tanh()

    def forward(self, input_ids, attention_mask, dates, **_) -> GaussOutput:
        outputs: BaseModelOutput = self.backbone(input_ids=input_ids, attention_mask=attention_mask)

        # emb = self.mean_pooling(outputs, attention_mask)
        emb = outputs.last_hidden_state[:, 0]
        pos_encoding = getPositionEncoding(dates, POSITIONAL_ENCODING_DIM).to(emb.device)
        emb = torch.cat((emb, pos_encoding), dim=-1)

        mu = self.w_mu(emb)
        mu = self.activation(mu)

        log_var = self.w_var(emb)
        std = torch.sqrt(log_var.exp())

        return GaussOutput(mu=mu, std=std)
    
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
def getPositionEncoding(dates, dim, n=10000) -> torch.Tensor:
    """
    Generates a positional encoding vector for a given dimension.
    Args:
        date (float): The date or time value to encode.
        dim (int): The dimension of the positional encoding.
        n (int, optional): A scaling factor for the positional encoding. Default is 10000.
    Returns:
        torch.Tensor: A tensor of shape (seq_len, d) containing the positional encoding.
    """
    P = torch.zeros(len(dates), dim)

    start_date: datetime = datetime(1889, 1, 1)
    
    for j in range(len(dates)):
        date: datetime = datetime.strptime(dates[j], "%d %B %Y")
        k = (date - start_date).days
        
        for i in torch.arange(int(dim/2)):
            denominator = torch.pow(n, 2*i/dim)
            
            P[j, 2*i] = torch.sin(k/denominator)
            P[j, 2*i+1] = torch.cos(k/denominator)
    
    return P

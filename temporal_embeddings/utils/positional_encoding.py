from datetime import datetime

import torch

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
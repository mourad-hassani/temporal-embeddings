import torch

def getPositionEncoding(seq_len, d, n=10000):
    P = torch.zeros(seq_len, d)

    for k in range(seq_len):
        for i in torch.arange(int(d/2)):
            denominator = torch.pow(n, 2*i/d)
            
            P[k, 2*i] = torch.sin(k/denominator)
            P[k, 2*i+1] = torch.cos(k/denominator)
    
    return P

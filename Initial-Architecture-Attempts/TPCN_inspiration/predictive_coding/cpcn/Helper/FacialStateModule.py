import torch
import torch.nn as nn

class FacialStateModule(nn.Module):
    def __init__(self, input_dim=128, embed_dim=32, n_emotions=6):
        super().__init__()
        self.input_dim = input_dim
        self.embed_dim = embed_dim
        self.n_emotions = n_emotions
        self.encoder = nn.Linear(input_dim, embed_dim)
        self.prototypes = nn.Parameter(torch.zeros(n_emotions, embed_dim))
        self.beta = 0.2  # error-driven update rate

    def forward(self, x, emotion_idx=0, quality: float = 1.0, anchor_agreement: float = 0.0, global_error: float = 0.0):
        # x: [input_dim] tensor
        z = self.encoder(x)
        pred = self.prototypes[emotion_idx]
        error = z - pred
        # Predictive coding: update state to minimize error (not in-place)
        state = pred + self.beta * error
        sims = self.match(x)
        gate = float(quality) > 0.2 and float(global_error) < 1.0
        return state, sims, bool(gate)

    def match(self, x):
        # Cosine similarity to emotion prototypes
        z = self.encoder(x)
        sims = torch.nn.functional.cosine_similarity(self.prototypes, z.unsqueeze(0), dim=1)
        return sims

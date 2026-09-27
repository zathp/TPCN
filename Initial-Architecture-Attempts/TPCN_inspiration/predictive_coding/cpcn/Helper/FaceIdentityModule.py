import torch
import torch.nn as nn

class FaceIdentityModule(nn.Module):
    def __init__(self, input_dim=128, embed_dim=64, n_identities=10):
        super().__init__()
        self.input_dim = input_dim
        self.embed_dim = embed_dim
        self.n_identities = n_identities
        self.encoder = nn.Linear(input_dim, embed_dim)
        self.prototypes = nn.Parameter(torch.zeros(n_identities, embed_dim))
        self.beta = 0.2  # error-driven update rate

    def forward(self, x, identity_idx=0, quality: float = 1.0, anchor_agreement: float = 0.0, global_error: float = 0.0):
        # x: [input_dim] tensor
        z = self.encoder(x)
        pred = self.prototypes[identity_idx]
        error = z - pred
        # Predictive coding: update state to minimize error (not in-place)
        state = pred + self.beta * error
        # Per-identity similarity scores for fusion
        sims = self.match(x)
        # Simple gating heuristic: open when sensory quality is reasonable
        gate = float(quality) > 0.2 and float(global_error) < 1.0
        return state, sims, bool(gate)

    def match(self, x):
        # Cosine similarity to prototypes
        z = self.encoder(x)
        sims = torch.nn.functional.cosine_similarity(self.prototypes, z.unsqueeze(0), dim=1)
        return sims

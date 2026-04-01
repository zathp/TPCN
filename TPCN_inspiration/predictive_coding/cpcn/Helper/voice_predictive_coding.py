import torch
import torch.nn as nn

class VoicePredictiveCodingModule(nn.Module):
	def __init__(self, input_dim=64, embed_dim=32, n_identities=10, hidden_dim=32):
		super().__init__()
		self.input_dim = input_dim
		self.embed_dim = embed_dim
		self.n_identities = n_identities
		self.hidden_dim = hidden_dim
		self.hidden = nn.Parameter(torch.zeros(n_identities, hidden_dim))
		self.encoder = nn.Linear(input_dim, embed_dim)
		self.projector = nn.Linear(embed_dim, hidden_dim)
		self.beta = 0.2  # error-driven update rate

	def forward(self, x, identity_idx=0):
		# x: [input_dim] tensor
		z = self.encoder(x)
		h = self.projector(z)
		pred = self.hidden[identity_idx]
		error = h - pred
		# Predictive coding: update state to minimize error (not in-place)
		state = pred + self.beta * error
		return state, error.norm()
import torch
import torch.nn as nn

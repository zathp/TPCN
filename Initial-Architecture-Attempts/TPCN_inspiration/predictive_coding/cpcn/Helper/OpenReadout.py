import torch
import sounddevice as sd

class OpenReadout(torch.nn.Module):
    def __init__(self, state_dim=648, output_dim=64, sample_rate=16000):
        super().__init__()
        self.state_dim = state_dim
        self.output_dim = output_dim
        self.sample_rate = sample_rate
        # Projection head: state_dim -> output_dim
        self.net = torch.nn.Sequential(
            torch.nn.Linear(state_dim, max(output_dim * 2, 32)),
            torch.nn.Tanh(),
            torch.nn.Linear(max(output_dim * 2, 32), output_dim),
            torch.nn.Tanh(),
        )
        self.alpha_head = torch.nn.Sequential(
            torch.nn.Linear(state_dim, 32),
            torch.nn.Tanh(),
            torch.nn.Linear(32, 1),
            torch.nn.Sigmoid(),
        )
        self._init_weights()

    def _init_weights(self):
        for layer in self.net:
            if isinstance(layer, torch.nn.Linear):
                torch.nn.init.orthogonal_(layer.weight, gain=0.7)
                torch.nn.init.zeros_(layer.bias)
        for layer in self.alpha_head:
            if isinstance(layer, torch.nn.Linear):
                torch.nn.init.orthogonal_(layer.weight, gain=0.7)
                torch.nn.init.zeros_(layer.bias)

    def forward(self, reservoir_state: torch.Tensor):
        """
        Args:
            reservoir_state : (state_dim,)
        Returns:
            world_output : (output_dim,)
            alpha        : scalar tensor in (0, 1)
        """
        world_out = self.net(reservoir_state)
        alpha = self.alpha_head(reservoir_state).squeeze(-1)
        return world_out, alpha

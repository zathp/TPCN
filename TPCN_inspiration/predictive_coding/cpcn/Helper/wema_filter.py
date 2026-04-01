import torch

def two_sided_tail_probability(
	x: torch.Tensor,
	mean: torch.Tensor,
	stddev: torch.Tensor,
	eps: float = 1e-6,
) -> torch.Tensor:
	"""Stable two-sided tail probability gate in [0, 1]."""
	den = torch.clamp(stddev, min=float(eps))
	z = (x - mean) / den
	cdf = 0.5 * (1.0 + torch.erf(z / float(2.0 ** 0.5)))
	tail2 = 2.0 * torch.minimum(cdf, 1.0 - cdf)
	return torch.clamp(tail2, min=0.0, max=1.0)

class WEMAFilter:
	"""Stateful weighted EMA with optional dynamic tail gating.

	Update rule:
	  alpha_eff = beta * (alpha + (1 - alpha) * tail_prob)
	  state <- (1 - alpha_eff) * state + alpha_eff * x

	The first step initializes state directly from x.
	"""

	def __init__(self, eps: float = 1e-6):
		self.eps = float(eps)
		self._state: torch.Tensor | None = None

	def reset(self) -> None:
		self._state = None

	@property
	def state(self) -> torch.Tensor | None:
		return self._state

	def step(
		self,
		x: torch.Tensor,
		alpha: torch.Tensor,
		beta: torch.Tensor | None = None,
		alpha_delta: torch.Tensor | None = None,
	) -> torch.Tensor:
		"""Apply one WEMA step and return the filtered state tensor."""
		if beta is None:
			beta = torch.ones_like(alpha)
		if alpha_delta is not None:
			alpha = alpha + alpha_delta

		alpha = torch.clamp(alpha.to(device=x.device, dtype=x.dtype), min=0.0, max=1.0)
		beta = torch.clamp(beta.to(device=x.device, dtype=x.dtype), min=0.0, max=1.0)

		if self._state is None or self._state.shape != x.shape or self._state.device != x.device:
			self._state = x
			return x

		std_prev = torch.sqrt((x - self._state).pow(2) + self.eps)
		tail = two_sided_tail_probability(x=x, mean=self._state, stddev=std_prev, eps=self.eps)
		alpha_eff = torch.clamp(beta * (alpha + (1.0 - alpha) * tail), min=0.0, max=1.0)
		self._state = (1.0 - alpha_eff) * self._state + alpha_eff * x
		return self._state

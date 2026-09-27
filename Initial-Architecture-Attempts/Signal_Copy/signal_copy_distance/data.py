from __future__ import annotations

import torch


def make_visual_grids(height: int, width: int, device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
    y = torch.linspace(-1.0, 1.0, steps=height, device=device)
    x = torch.linspace(-1.0, 1.0, steps=width, device=device)
    gy, gx = torch.meshgrid(y, x, indexing="ij")
    return gx, gy


def compute_loss_drop_pct(baseline_loss: float, current_loss: float) -> float:
    denom = max(abs(baseline_loss), 1e-12)
    return 100.0 * max(0.0, (baseline_loss - current_loss) / denom)


def sample_curriculum_visual_batch(
    stage: int,
    step_idx: int,
    batch_size: int,
    height: int,
    width: int,
    grid_x: torch.Tensor,
    grid_y: torch.Tensor,
    device: torch.device,
) -> torch.Tensor:
    if stage <= 0:
        flash = 1.0 if (step_idx % 2 == 0) else -1.0
        x_img = torch.full((batch_size, height, width), flash, device=device, dtype=torch.float32)
        return x_img.reshape(batch_size, height * width)

    if stage == 1:
        flash = 1.0 if (step_idx % 2 == 0) else -1.0
        x_img = torch.full((batch_size, height, width), flash * 0.5, device=device, dtype=torch.float32)
        for b in range(batch_size):
            row = int(torch.randint(0, height, size=(1,), device=device).item())
            col = int(torch.randint(0, width, size=(1,), device=device).item())
            amp_h = torch.empty(1, device=device).uniform_(0.6, 1.2).item()
            amp_v = torch.empty(1, device=device).uniform_(0.6, 1.2).item()
            x_img[b, row, :] += amp_h
            x_img[b, :, col] += amp_v
        x_img = torch.tanh(x_img)
        return x_img.reshape(batch_size, height * width)

    x_img = torch.zeros((batch_size, height, width), device=device, dtype=torch.float32)
    for b in range(batch_size):
        phase_x = torch.empty(1, device=device).uniform_(0.0, 6.28318).item()
        phase_y = torch.empty(1, device=device).uniform_(0.0, 6.28318).item()
        fx = torch.empty(1, device=device).uniform_(1.0, 4.0).item()
        fy = torch.empty(1, device=device).uniform_(1.0, 4.0).item()

        sin_x = torch.sin((fx * 3.14159) * grid_x + phase_x)
        sin_y = torch.sin((fy * 3.14159) * grid_y + phase_y)
        radial = torch.cos(6.0 * torch.sqrt(grid_x * grid_x + grid_y * grid_y) + phase_x)
        poly = (grid_x * grid_x) - (0.5 * grid_y * grid_y)

        mix = 0.40 * sin_x + 0.35 * sin_y + 0.20 * radial + 0.15 * poly

        if torch.rand(1, device=device).item() > 0.4:
            row = int(torch.randint(0, height, size=(1,), device=device).item())
            mix[row, :] += torch.empty(1, device=device).uniform_(0.4, 1.0).item()
        if torch.rand(1, device=device).item() > 0.4:
            col = int(torch.randint(0, width, size=(1,), device=device).item())
            mix[:, col] -= torch.empty(1, device=device).uniform_(0.4, 1.0).item()

        x_img[b] = torch.tanh(mix)

    return x_img.reshape(batch_size, height * width)


def generate_visual_pattern(
    step_idx: int,
    stage: int,
    height: int,
    width: int,
    grid_x: torch.Tensor,
    grid_y: torch.Tensor,
    device: torch.device,
) -> torch.Tensor:
    """Returns a single flat pattern tensor in [-1, 1] for visual inference loops."""
    return sample_curriculum_visual_batch(
        stage=stage,
        step_idx=step_idx,
        batch_size=1,
        height=height,
        width=width,
        grid_x=grid_x,
        grid_y=grid_y,
        device=device,
    )[0]
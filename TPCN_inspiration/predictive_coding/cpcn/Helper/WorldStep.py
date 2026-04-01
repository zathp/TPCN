import math
from typing import Optional

import torch
import numpy as np


class TorchWorldStep:
	def __init__(
		self,
		base_eddy: float = 0.7,
		damping: float = 0.02,
		dispersion: float = -0.5,
		particle_mass1: float = 1.0,
		particle_mass2: float = 1.0,
		particle_dispersion: int = 1,
		enable_particles: bool = True,
		point_mode: str = "static",
		particle_velocity_max: float = 5.0,
		density1_injection_strength_pos: float = 0.3,
		density1_injection_strength_neg: float = 0.3,
		nx: int = 50,
		ny: int = 50,
		nz: int = 50,
		lx: float = 4.0,
		ly: float = 4.0,
		lz: float = 4.0,
		k1_size: int = 3,
		k2_size: int = 2,
		k3_size: int = 3,
		k4_size: int = 2,
		k5_size: int = 2,
		seed: int = 0,
		float_dtype: torch.dtype = torch.float32,
		particle_layout: str = "grid",
		particle_propagation_axis: str = "x",
		particle_wavelength_cells: Optional[float] = None,
		particle_line_dense_step: Optional[int] = None,
		particle_line_sparse_step: Optional[int] = None,
		particle_antipoint_mode: str = "offset",
		particle_grating_delay_frac: float = 0.25,
		probe_wema_alpha: float = 0.15,
		device: Optional[torch.device] = None,
	):
		self.NX = int(nx)
		self.NY = int(ny)
		self.NZ = int(nz)
		self.LX = float(lx)
		self.LY = float(ly)
		self.LZ = float(lz)
		self.seed = int(seed)
		self.float_dtype = float_dtype
		self.device = device if device is not None else torch.device("cuda" if torch.cuda.is_available() else "cpu")

		self.base_eddy = float(base_eddy)
		self.dispersion = float(dispersion)
		self.damping = float(damping)

		self.enable_particles = bool(enable_particles)
		self.particle_mass1 = particle_mass1
		self.particle_mass2 = particle_mass2
		self.particle_dispersion = particle_dispersion
		self.particle_layout = str(particle_layout).lower()
		self.particle_propagation_axis = str(particle_propagation_axis).lower()
		self.particle_wavelength_cells = particle_wavelength_cells
		self.particle_line_dense_step = particle_line_dense_step
		self.particle_line_sparse_step = particle_line_sparse_step
		self.particle_antipoint_mode = str(particle_antipoint_mode).lower()
		self.particle_grating_delay_frac = float(particle_grating_delay_frac)
		self.probe_wema_alpha = float(probe_wema_alpha)
		self.point_mode = point_mode
		self.particle_velocity_max = particle_velocity_max
		self.density1_injection_strength_pos = density1_injection_strength_pos
		self.density1_injection_strength_neg = density1_injection_strength_neg

		if self.probe_wema_alpha <= 0.0 or self.probe_wema_alpha > 1.0:
			raise ValueError(f"probe_wema_alpha must be in (0, 1], got {self.probe_wema_alpha}")

		self._validate_particle_layout(self.particle_layout)
		self._validate_particle_axis(self.particle_propagation_axis)
		self._validate_particle_antipoint_mode(self.particle_antipoint_mode)

		self.k1_size = int(k1_size)
		self.k2_size = int(k2_size)
		self.k3_size = int(k3_size)
		self.k4_size = int(k4_size)
		self.k5_size = int(k5_size)

		self.init_kernels()

		self.curlfield = torch.zeros((self.NZ, self.NY, self.NX, 3), dtype=self.float_dtype, device=self.device)
		self.curlfield_prev = torch.zeros_like(self.curlfield)
		self.flowfield = torch.zeros_like(self.curlfield)
		self.flowfield_prev = torch.zeros_like(self.curlfield)
		self.densityfield = torch.zeros((self.NZ, self.NY, self.NX), dtype=self.float_dtype, device=self.device)

		self.num_particles = 0
		if self.enable_particles:
			self.particles = self._generate_initial_particles_torch(
				nx=self.NX,
				ny=self.NY,
				nz=self.NZ,
				origin=(-self.LX * self.NX / 2 + self.LX * 0.5, -self.LY * self.NY / 2 + self.LY * 0.5, -self.LZ * self.NZ / 2 + self.LZ * 0.5),
				spacing=(self.LX, self.LY, self.LZ),
				step=self.particle_dispersion,
				layout=self.particle_layout,
				propagation_axis=self.particle_propagation_axis,
				wavelength_cells=self.particle_wavelength_cells,
				dense_line_step=self.particle_line_dense_step,
				sparse_line_step=self.particle_line_sparse_step,
				role="primary",
			)
			self.particles2 = self._generate_initial_particles_torch(
				nx=self.NX,
				ny=self.NY,
				nz=self.NZ,
				origin=(-self.LX * self.NX / 2 + self.LX * 1.0, -self.LY * self.NY / 2 + self.LY * 1.0, -self.LZ * self.NZ / 2 + self.LZ * 0.5),
				spacing=(self.LX, self.LY, self.LZ),
				step=self.particle_dispersion,
				layout=self.particle_layout,
				propagation_axis=self.particle_propagation_axis,
				wavelength_cells=self.particle_wavelength_cells,
				dense_line_step=self.particle_line_dense_step,
				sparse_line_step=self.particle_line_sparse_step,
				antipoint_mode=self.particle_antipoint_mode,
				grating_delay_frac=self.particle_grating_delay_frac,
				role="secondary",
			)
			self.particles_vel = torch.zeros_like(self.particles)
			self.particles2_vel = torch.zeros_like(self.particles2)
			self.num_particles = int(self.particles.shape[0])
		else:
			self.particles = torch.zeros((0, 3), dtype=self.float_dtype, device=self.device)
			self.particles2 = torch.zeros((0, 3), dtype=self.float_dtype, device=self.device)
			self.particles_vel = torch.zeros((0, 3), dtype=self.float_dtype, device=self.device)
			self.particles2_vel = torch.zeros((0, 3), dtype=self.float_dtype, device=self.device)

		self.reservoir_probe_idx = None
		self.reservoir_include_particles = True
		self.reservoir_include_global_moments = True
		self.antipodal_inputs_attached = True
		self._uniform_probe_idx_cache: dict[int, torch.Tensor] = {}
		self._probe_wema_mean: Optional[torch.Tensor] = None
		self._probe_wema_second: Optional[torch.Tensor] = None
		self._probe_wema_square_mean: Optional[torch.Tensor] = None
		self._probe_wema_square_second: Optional[torch.Tensor] = None

		self.init_densityfield()
		self.init_flowfield(seed=self.seed, magnitude=2.0)

	def _validate_particle_layout(self, layout: str) -> None:
		if layout not in ("grid", "comb"):
			raise ValueError("particle_layout must be one of: 'grid', 'comb'")

	def _validate_particle_axis(self, axis: str) -> None:
		if axis not in ("x", "y", "z"):
			raise ValueError("particle_propagation_axis must be one of: 'x', 'y', 'z'")

	def _validate_particle_antipoint_mode(self, mode: str) -> None:
		if mode not in ("offset", "reflector", "grating"):
			raise ValueError("particle_antipoint_mode must be one of: 'offset', 'reflector', 'grating'")

	def _generate_initial_particles_torch(
		self,
		nx: int,
		ny: int,
		nz: int,
		origin=(0.0, 0.0, 0.0),
		spacing=(1.0, 1.0, 1.0),
		step: int = 1,
		layout: str = "grid",
		propagation_axis: str = "x",
		wavelength_cells: Optional[float] = None,
		dense_line_step: Optional[int] = None,
		sparse_line_step: Optional[int] = None,
		antipoint_mode: str = "offset",
		grating_delay_frac: float = 0.25,
		role: str = "primary",
	) -> torch.Tensor:
		ox, oy, oz = origin
		dx, dy, dz = spacing
		layout = str(layout).lower()
		propagation_axis = str(propagation_axis).lower()
		antipoint_mode = str(antipoint_mode).lower()
		TorchWorldStep._validate_particle_layout(self, layout)
		TorchWorldStep._validate_particle_axis(self, propagation_axis)
		TorchWorldStep._validate_particle_antipoint_mode(self, antipoint_mode)

		step = max(1, int(step))
		if layout == "grid":
			x = ox + dx * torch.arange(0, nx, step, device=self.device, dtype=self.float_dtype)
			y = oy + dy * torch.arange(0, ny, step, device=self.device, dtype=self.float_dtype)
			z = oz + dz * torch.arange(0, nz, step, device=self.device, dtype=self.float_dtype)
			X, Y, Z = torch.meshgrid(x, y, z, indexing="ij")
			return torch.stack((X, Y, Z), dim=-1).reshape(-1, 3)

		dims = (int(nx), int(ny), int(nz))
		axis_map = {"x": 0, "y": 1, "z": 2}
		axis_idx = axis_map[propagation_axis]
		trans_axes = [i for i in (0, 1, 2) if i != axis_idx]
		n_axis = max(1, dims[axis_idx])

		if wavelength_cells is None or float(wavelength_cells) <= 0.0:
			wavelength_cells = max(1.0, float(step) * 4.0)
		else:
			wavelength_cells = max(1.0, float(wavelength_cells))

		line_pitch = max(1, int(round(wavelength_cells / 4.0)))
		dense_step_val = max(1, int(step if dense_line_step is None else dense_line_step))
		sparse_default = max(dense_step_val + 1, dense_step_val * 2)
		sparse_step_val = max(1, int(sparse_default if sparse_line_step is None else sparse_line_step))

		line_indices = torch.arange(0, n_axis, step=line_pitch, device=self.device, dtype=torch.int64)
		strips = []
		for i, line_idx in enumerate(line_indices.tolist()):
			cross_step = dense_step_val if (i % 2 == 0) else sparse_step_val
			ib = torch.arange(0, dims[trans_axes[0]], step=cross_step, device=self.device, dtype=torch.int64)
			ic = torch.arange(0, dims[trans_axes[1]], step=cross_step, device=self.device, dtype=torch.int64)
			if ib.numel() == 0 or ic.numel() == 0:
				continue
			BB, CC = torch.meshgrid(ib, ic, indexing="ij")
			idx = [None, None, None]
			idx[axis_idx] = torch.full((BB.numel(),), int(line_idx), dtype=torch.int64, device=self.device)
			idx[trans_axes[0]] = BB.reshape(-1)
			idx[trans_axes[1]] = CC.reshape(-1)
			strips.append(torch.stack((idx[0], idx[1], idx[2]), dim=1))

		if not strips:
			return torch.zeros((0, 3), dtype=self.float_dtype, device=self.device)

		grid_idx = torch.cat(strips, dim=0)
		if role == "secondary":
			if antipoint_mode == "reflector":
				grid_idx[:, axis_idx] = (dims[axis_idx] - 1) - grid_idx[:, axis_idx]
			elif antipoint_mode == "grating":
				delay_cells = max(1, int(round(float(grating_delay_frac) * wavelength_cells)))
				grid_idx[:, axis_idx] = torch.remainder(grid_idx[:, axis_idx] + delay_cells, dims[axis_idx])

		pts = torch.empty((grid_idx.shape[0], 3), dtype=self.float_dtype, device=self.device)
		pts[:, 0] = ox + dx * grid_idx[:, 0].to(self.float_dtype)
		pts[:, 1] = oy + dy * grid_idx[:, 1].to(self.float_dtype)
		pts[:, 2] = oz + dz * grid_idx[:, 2].to(self.float_dtype)
		return pts

	def init_kernels(self) -> None:
		self.diffuse_weights = []
		self.diffuse_shifts = []
		ahat1 = 0.0
		half = round((self.k1_size - 1) / 2)
		for i in range(-half, half + 1):
			for j in range(-half, half + 1):
				for k in range(-half, half + 1):
					r = math.sqrt(i * i + j * j + k * k)
					w = math.exp(self.dispersion * r)
					ahat1 += w
					self.diffuse_weights.append(w)
					self.diffuse_shifts.append((i, j, k))
		self.diffuse_weights = [w / ahat1 for w in self.diffuse_weights]
		self.diffuse_weights_t = torch.tensor(self.diffuse_weights, dtype=self.float_dtype, device=self.device)

		self.curl_weights = []
		self.curl_shifts = []
		self.curl_rvecs = []
		for i in range(-half, half + 1):
			for j in range(-half, half + 1):
				for k in range(-half, half + 1):
					r = math.sqrt(i * i + j * j + k * k)
					w = math.exp(self.dispersion * r) / ahat1
					self.curl_weights.append(w)
					self.curl_shifts.append((i, j, k))
					self.curl_rvecs.append(torch.tensor([i, j, k], dtype=self.float_dtype, device=self.device))
				self.curl_weights_t = torch.tensor(self.curl_weights, dtype=self.float_dtype, device=self.device)

		self.gradient_weights = []
		self.gradient_shifts = []
		self.gradient_offsets = []
		ahat2 = 0.0
		for i in range(-self.k2_size, self.k2_size):
			for j in range(-self.k2_size, self.k2_size):
				for k in range(-self.k2_size, self.k2_size):
					r = math.sqrt((i + 0.5) ** 2 + (j + 0.5) ** 2 + (k + 0.5) ** 2)
					w = r / (1 + r * r)
					ahat2 += w
					self.gradient_weights.append(w)
					self.gradient_shifts.append((i, j, k))
					self.gradient_offsets.append((i + 0.5, j + 0.5, k + 0.5))
		self.gradient_weights = [w / ahat2 for w in self.gradient_weights]
		self.gradient_weights_t = torch.tensor(self.gradient_weights, dtype=self.float_dtype, device=self.device)
		self.gradient_offsets_t = torch.tensor(self.gradient_offsets, dtype=self.float_dtype, device=self.device)

		self.divergence_weights = []
		self.divergence_shifts = []
		self.divergence_offsets = []
		for i in range(-self.k2_size + 1, self.k2_size + 1):
			for j in range(-self.k2_size + 1, self.k2_size + 1):
				for k in range(-self.k2_size + 1, self.k2_size + 1):
					r = math.sqrt((i - 0.5) ** 2 + (j - 0.5) ** 2 + (k - 0.5) ** 2)
					w = r / (1 + r * r) / ahat2
					self.divergence_weights.append(w)
					self.divergence_shifts.append((i, j, k))
					self.divergence_offsets.append((i - 0.5, j - 0.5, k - 0.5))
				self.divergence_weights_t = torch.tensor(self.divergence_weights, dtype=self.float_dtype, device=self.device)
				self.divergence_offsets_t = torch.tensor(self.divergence_offsets, dtype=self.float_dtype, device=self.device)

		self.mean_weights = []
		self.mean_shifts = []
		ahat5 = 0.0
		for i in range(-self.k5_size, self.k5_size + 1):
			for j in range(-self.k5_size, self.k5_size + 1):
				for k in range(-self.k5_size, self.k5_size + 1):
					r = math.sqrt(i * i + j * j + k * k)
					w = 1 / (1 + r * r)
					ahat5 += w
					self.mean_weights.append(w)
					self.mean_shifts.append((i, j, k))
		self.mean_weights = [w / ahat5 for w in self.mean_weights]
		self.mean_weights_t = torch.tensor(self.mean_weights, dtype=self.float_dtype, device=self.device)

	def init_densityfield(self):
		g = torch.Generator(device=self.device)
		g.manual_seed(self.seed)
		self.densityfield = (2.0 * torch.rand((self.NZ, self.NY, self.NX), generator=g, device=self.device) - 1.0).to(self.float_dtype)
		return self.densityfield

	def init_flowfield(self, seed: Optional[int] = None, magnitude: Optional[float] = None):
		if seed is None:
			seed = self.seed
		mag = float(magnitude) if magnitude is not None else float(self.base_eddy)
		g = torch.Generator(device=self.device)
		g.manual_seed(int(seed))
		vecs = torch.randn((self.NZ, self.NY, self.NX, 3), generator=g, device=self.device, dtype=self.float_dtype)
		norms = torch.linalg.norm(vecs, dim=-1, keepdim=True).clamp_min(1e-9)
		self.flowfield = (vecs / norms) * mag
		return self.flowfield

	def set_reservoir_probe_indices(self, probe_idx):
		if probe_idx is None:
			self.reservoir_probe_idx = None
			self._probe_wema_mean = None
			self._probe_wema_second = None
			self._probe_wema_square_mean = None
			self._probe_wema_square_second = None
			return
		idx = torch.as_tensor(probe_idx, dtype=torch.int32, device=self.device)
		if idx.ndim != 2 or idx.shape[1] != 3:
			raise ValueError("probe_idx must have shape (N, 3) in (iz, iy, ix) order")
		idx[:, 0] = torch.remainder(idx[:, 0], self.NZ)
		idx[:, 1] = torch.remainder(idx[:, 1], self.NY)
		idx[:, 2] = torch.remainder(idx[:, 2], self.NX)
		self.reservoir_probe_idx = idx
		self._probe_wema_mean = None
		self._probe_wema_second = None
		self._probe_wema_square_mean = None
		self._probe_wema_square_second = None

	def _make_uniform_probe_indices(self, n_points: int):
		n_points = max(1, int(n_points))
		cached = self._uniform_probe_idx_cache.get(n_points)
		if cached is not None:
			return cached
		total = self.NZ * self.NY * self.NX
		if n_points >= total:
			flat = torch.arange(total, device=self.device, dtype=torch.long)
		else:
			flat = torch.linspace(0, total - 1, n_points, device=self.device).long()
		yz = self.NY * self.NX
		iz = flat // yz
		rem = flat % yz
		iy = rem // self.NX
		ix = rem % self.NX
		probe_idx = torch.stack((iz.int(), iy.int(), ix.int()), dim=1)
		self._uniform_probe_idx_cache[n_points] = probe_idx
		return probe_idx

	def apply_reservoir_input(self, input_vector, gain=1.0, mode="density1"):
		if input_vector is None:
			return
		u = torch.as_tensor(input_vector, dtype=self.float_dtype, device=self.device).reshape(-1)
		if u.numel() == 0:
			return
		probe_idx = self._make_uniform_probe_indices(int(u.numel()))
		iz, iy, ix = probe_idx[:, 0].long(), probe_idx[:, 1].long(), probe_idx[:, 2].long()
		scaled_u = u * float(gain)
		self.densityfield[iz, iy, ix] = self.densityfield[iz, iy, ix] + scaled_u

		if self.antipodal_inputs_attached:
			# Pair each injection with an equal-magnitude opposite-sign antipodal injection.
			iz_a = torch.remainder(iz + (self.NZ // 2), self.NZ)
			iy_a = torch.remainder(iy + (self.NY // 2), self.NY)
			ix_a = torch.remainder(ix + (self.NX // 2), self.NX)
			self.densityfield[iz_a, iy_a, ix_a] = self.densityfield[iz_a, iy_a, ix_a] - scaled_u

	def diffuse_field_kernal(self, field: torch.Tensor):
		out = torch.zeros_like(field)
		for i, shift in enumerate(self.diffuse_shifts):
			out = out + self.diffuse_weights_t[i] * torch.roll(field, shifts=shift, dims=(0, 1, 2))
		return out

	def fieldmean(self, field: torch.Tensor):
		out = torch.zeros_like(field)
		for i, shift in enumerate(self.mean_shifts):
			out = out + self.mean_weights_t[i] * torch.roll(field, shifts=shift, dims=(0, 1, 2))
		return out

	def calculate_gradientfield_kernal(self, field: torch.Tensor):
		grad = torch.zeros((self.NZ, self.NY, self.NX, 3), dtype=self.float_dtype, device=self.device)
		for i, shift in enumerate(self.gradient_shifts):
			shifted = torch.roll(field, shifts=shift, dims=(0, 1, 2))
			w = self.gradient_weights_t[i]
			off = self.gradient_offsets_t[i]
			grad[..., 0] = grad[..., 0] + w * shifted * off[0]
			grad[..., 1] = grad[..., 1] + w * shifted * off[1]
			grad[..., 2] = grad[..., 2] + w * shifted * off[2]
		return grad

	def calculate_divergence_from_flow_kernal(self, field: torch.Tensor):
		div = torch.zeros((self.NZ, self.NY, self.NX), dtype=self.float_dtype, device=self.device)
		for i, shift in enumerate(self.divergence_shifts):
			shifted = torch.roll(field, shifts=shift, dims=(0, 1, 2))
			w = self.divergence_weights_t[i]
			off = self.divergence_offsets_t[i]
			div = div + w * (shifted[..., 0] * off[0] + shifted[..., 1] * off[1] + shifted[..., 2] * off[2])
		return div

	def calculate_curlfield_kernal(self, field: torch.Tensor):
		curl = torch.zeros((self.NZ, self.NY, self.NX, 3), dtype=self.float_dtype, device=self.device)
		for i, (shift, r_vec) in enumerate(zip(self.curl_shifts, self.curl_rvecs)):
			shifted = torch.roll(field, shifts=shift, dims=(0, 1, 2))
			rv = r_vec.view(1, 1, 1, 3)
			curl = curl + self.curl_weights_t[i] * torch.cross(rv.expand_as(shifted), shifted, dim=-1)
		return curl

	def step_densityfield(self, dt=0.1, diffusion_rate=0.1):
		density_diffused = self.diffuse_field_kernal(self.densityfield)
		self.densityfield = (1 - diffusion_rate) * self.densityfield + diffusion_rate * density_diffused
		self.densityfield = self.densityfield + self.calculate_divergence_from_flow_kernal(self.flowfield) * dt
		self.densityfield = torch.clamp(self.densityfield, -1.0, 1.0)

	def step_flowfield(self, dt=0.1, flow_diffusion_rate=0.05):
		self.flowfield = self.flowfield + self.calculate_gradientfield_kernal(self.densityfield) * dt
		curl_change = self.curlfield - self.curlfield_prev
		eddyflow = self.calculate_curlfield_kernal(curl_change)
		self.flowfield = self.flowfield + eddyflow * dt * -0.5
		flow_diffused = self.diffuse_field_kernal(self.flowfield)
		self.flowfield = (1 - flow_diffusion_rate) * self.flowfield + flow_diffusion_rate * flow_diffused
		self.flowfield = self.flowfield * (1.0 - self.damping)

	def step_curlfield(self, dt=0.1, curl_diffusion_rate=0.1):
		self.curlfield_prev = self.curlfield.clone()
		self.curlfield = self.calculate_curlfield_kernal(self.flowfield)
		density_avg = self.fieldmean(self.densityfield)
		local_rate = curl_diffusion_rate * (2.0 / (1.0 + density_avg * density_avg) - 1.0)
		local_rate = local_rate.unsqueeze(-1)
		curl_diffused = self.diffuse_field_kernal(self.curlfield)
		self.curlfield = (1 - local_rate) * self.curlfield + local_rate * curl_diffused

	def step(self, dt=0.1, print_timings=False):
		with torch.no_grad():
			self.step_densityfield(dt)
			self.step_flowfield(dt)
			self.step_curlfield(dt)
		# Detach fields so the graph doesn't grow unboundedly across steps.
		self.densityfield = self.densityfield.detach()
		self.flowfield = self.flowfield.detach()
		self.curlfield = self.curlfield.detach()
		self.curlfield_prev = self.curlfield_prev.detach()

	def _extract_probe_scalar(self, idx: Optional[torch.Tensor]) -> torch.Tensor:
		if idx is None:
			return self.densityfield.reshape(-1)
		iz = torch.remainder(idx[:, 0], self.NZ).long()
		iy = torch.remainder(idx[:, 1], self.NY).long()
		ix = torch.remainder(idx[:, 2], self.NX).long()
		return self.densityfield[iz, iy, ix]

	def _wema_probe_features(self, probe_values: torch.Tensor) -> torch.Tensor:
		x = probe_values.to(dtype=torch.float32)
		x2 = x * x
		x4 = x2 * x2
		a = float(self.probe_wema_alpha)
		one_minus_a = 1.0 - a

		if self._probe_wema_mean is None or self._probe_wema_mean.shape != x.shape:
			self._probe_wema_mean = x.clone()
			self._probe_wema_second = x2.clone()
			self._probe_wema_square_mean = x2.clone()
			self._probe_wema_square_second = x4.clone()
		else:
			self._probe_wema_mean = (one_minus_a * self._probe_wema_mean + a * x).detach()
			self._probe_wema_second = (one_minus_a * self._probe_wema_second + a * x2).detach()
			self._probe_wema_square_mean = (one_minus_a * self._probe_wema_square_mean + a * x2).detach()
			self._probe_wema_square_second = (one_minus_a * self._probe_wema_square_second + a * x4).detach()

		var = torch.clamp(self._probe_wema_second - self._probe_wema_mean * self._probe_wema_mean, min=0.0)
		var_sq = torch.clamp(
			self._probe_wema_square_second - self._probe_wema_square_mean * self._probe_wema_square_mean,
			min=0.0,
		)
		std = torch.sqrt(var.clamp(min=1e-6))
		std_sq = torch.sqrt(var_sq.clamp(min=1e-6))
		packed = torch.stack((x, self._probe_wema_mean, std, self._probe_wema_square_mean, std_sq), dim=-1)
		return packed.reshape(-1).to(self.float_dtype)

	def _extract_grid_features(self, probe_idx=None):
		idx = self.reservoir_probe_idx if probe_idx is None else torch.as_tensor(probe_idx, dtype=torch.int32, device=self.device)
		return self._wema_probe_features(self._extract_probe_scalar(idx))

	def _extract_global_moment_features(self):
		d = self.densityfield.detach()
		f = self.flowfield.detach()
		c = self.curlfield.detach()
		flow_mag = torch.linalg.norm(f, dim=-1)
		curl_mag = torch.linalg.norm(c, dim=-1)
		return torch.stack(
			[
				torch.mean(d),
				torch.var(d),
				torch.mean(flow_mag),
				torch.var(flow_mag),
				torch.mean(curl_mag),
				torch.var(curl_mag),
				torch.sum(flow_mag * flow_mag),
				torch.sum(curl_mag),
			]
		).to(self.float_dtype)

	def _extract_particle_summary_features(self):
		if self.num_particles == 0:
			return torch.zeros((10,), dtype=self.float_dtype, device=self.device)
		speed1 = torch.linalg.norm(self.particles_vel, dim=-1)
		speed2 = torch.linalg.norm(self.particles2_vel, dim=-1)
		dist1 = torch.linalg.norm(self.particles, dim=-1)
		dist2 = torch.linalg.norm(self.particles2, dim=-1)
		return torch.stack(
			[
				self.particles_vel[:, 0].mean(),
				self.particles_vel[:, 1].mean(),
				self.particles_vel[:, 2].mean(),
				speed1.mean(),
				dist1.mean(),
				self.particles2_vel[:, 0].mean(),
				self.particles2_vel[:, 1].mean(),
				self.particles2_vel[:, 2].mean(),
				speed2.mean(),
				dist2.mean(),
			],
			dim=0,
		).to(self.float_dtype)

	def extract_reservoir_state(self, probe_idx=None, include_particles=None, include_global_moments=None, return_numpy=False):
		if include_particles is None:
			include_particles = self.reservoir_include_particles
		if include_global_moments is None:
			include_global_moments = self.reservoir_include_global_moments
		parts = [self._extract_grid_features(probe_idx=probe_idx)]
		if include_global_moments:
			parts.append(self._extract_global_moment_features())
		if include_particles:
			parts.append(self._extract_particle_summary_features())
		state = torch.cat(parts, dim=0).to(self.float_dtype)
		if return_numpy:
			return state.detach().cpu().numpy()
		return state

	def get_reservoir_state_size(self, probe_idx=None, include_particles=True, include_global_moments=True):
		idx = self.reservoir_probe_idx if probe_idx is None else torch.as_tensor(probe_idx)
		if idx is None:
			grid_size = self.NZ * self.NY * self.NX * 5
		else:
			grid_size = int(idx.shape[0]) * 5
		extra = 0
		if include_global_moments:
			extra += 8
		if include_particles:
			extra += 10
		return int(grid_size + extra)

	def reset_reservoir_state(self, seed=None, reset_particles=False):
		if seed is not None:
			self.seed = int(seed)
		self.init_densityfield()
		self.init_flowfield(seed=self.seed, magnitude=2.0)
		self.curlfield.zero_()
		self.curlfield_prev.zero_()
		self._probe_wema_mean = None
		self._probe_wema_second = None
		self._probe_wema_square_mean = None
		self._probe_wema_square_second = None
		if reset_particles and self.enable_particles:
			self.particles = self._generate_initial_particles_torch(
				nx=self.NX,
				ny=self.NY,
				nz=self.NZ,
				origin=(-self.LX * self.NX / 2 + self.LX * 0.5, -self.LY * self.NY / 2 + self.LY * 0.5, -self.LZ * self.NZ / 2 + self.LZ * 0.5),
				spacing=(self.LX, self.LY, self.LZ),
				step=self.particle_dispersion,
				layout=self.particle_layout,
				propagation_axis=self.particle_propagation_axis,
				wavelength_cells=self.particle_wavelength_cells,
				dense_line_step=self.particle_line_dense_step,
				sparse_line_step=self.particle_line_sparse_step,
				role="primary",
			)
			self.particles2 = self._generate_initial_particles_torch(
				nx=self.NX,
				ny=self.NY,
				nz=self.NZ,
				origin=(-self.LX * self.NX / 2 + self.LX * 1.0, -self.LY * self.NY / 2 + self.LY * 1.0, -self.LZ * self.NZ / 2 + self.LZ * 0.5),
				spacing=(self.LX, self.LY, self.LZ),
				step=self.particle_dispersion,
				layout=self.particle_layout,
				propagation_axis=self.particle_propagation_axis,
				wavelength_cells=self.particle_wavelength_cells,
				dense_line_step=self.particle_line_dense_step,
				sparse_line_step=self.particle_line_sparse_step,
				antipoint_mode=self.particle_antipoint_mode,
				grating_delay_frac=self.particle_grating_delay_frac,
				role="secondary",
			)
			self.particles_vel = torch.zeros_like(self.particles)
			self.particles2_vel = torch.zeros_like(self.particles2)
			self.num_particles = int(self.particles.shape[0])

	def reservoir_step(
		self,
		input_vector=None,
		dt=0.1,
		input_gain=1.0,
		input_mode="density1",
		controlled_points_set1=None,
		controlled_points_set2=None,
		probe_idx=None,
		include_particles=None,
		include_global_moments=None,
		return_numpy=False,
		print_timings=False,
	):
		if input_vector is not None:
			self.apply_reservoir_input(input_vector, gain=input_gain, mode=input_mode)
		self.step(dt=dt, print_timings=print_timings)
		return self.extract_reservoir_state(
			probe_idx=probe_idx,
			include_particles=include_particles,
			include_global_moments=include_global_moments,
			return_numpy=return_numpy,
		)


# ------------------------------------------------------------------
# HopfieldPCN and simple face feature extractor
# These are copied from main_test to satisfy demo imports.
# ------------------------------------------------------------------


class HopfieldPCN(torch.nn.Module):
	def __init__(self, input_dim=128, n_prototypes=10):
		super().__init__()
		self.input_dim = input_dim
		self.n_prototypes = n_prototypes
		self.register_buffer("memory", torch.zeros(n_prototypes, input_dim))
		self.W = torch.nn.Parameter(torch.zeros(input_dim, input_dim))
		self.beta = 0.2  # error-driven update rate

	def resize_prototypes(self, new_n_prototypes):
		if new_n_prototypes <= self.n_prototypes:
			return
		new_memory = torch.zeros(new_n_prototypes, self.input_dim, device=self.memory.device)
		new_memory[: self.n_prototypes] = self.memory
		self.memory = new_memory
		self.n_prototypes = new_n_prototypes

	def store(self, idx, x):
		if idx >= self.n_prototypes:
			self.resize_prototypes(idx + 1)
		self.memory[idx].copy_(x.detach())
		# Avoid in-place update for autograd safety
		with torch.no_grad():
			self.W += torch.ger(x.detach(), x.detach())

	def recall(self, x, steps=5):
		state = x.clone().detach()
		for _ in range(steps):
			pred = torch.matmul(self.W, state)
			error = x - pred
			state = state + self.beta * error
		return state, error

	def match(self, x):
		sims = torch.nn.functional.cosine_similarity(self.memory, x.unsqueeze(0), dim=1)
		return sims

	def forward(self, x, identity_idx: int = 0, quality: float = 1.0, anchor_agreement: float = 0.0, global_error: float = 0.0):
		"""Compatibility wrapper to behave like other identity modules.
		Returns (state, scores, gate_open).
		"""
		state, error = self.recall(x)
		scores = self.match(state)
		gate = float(quality) > 0.2 and float(global_error) < 1.0
		return state, scores, bool(gate)


def extract_face_features(face_roi_bgr, input_dim=128, device=None, cv2_mod=None):
	if cv2_mod is None:
		import cv2 as cv2_mod
	gray = cv2_mod.cvtColor(face_roi_bgr, cv2_mod.COLOR_BGR2GRAY)
	w = 16
	h = max(1, input_dim // w)
	if w * h != input_dim:
		h = int(np.sqrt(input_dim))
		w = max(1, input_dim // max(1, h))
		if w * h != input_dim:
			w = input_dim
			h = 1
	resized = cv2_mod.resize(gray, (w, h), interpolation=cv2_mod.INTER_AREA)
	x = resized.astype(np.float32).reshape(-1) / 255.0
	if x.shape[0] < input_dim:
		x = np.concatenate([x, np.zeros((input_dim - x.shape[0],), dtype=np.float32)], axis=0)
	elif x.shape[0] > input_dim:
		x = x[:input_dim]
	t = torch.from_numpy(x).to(device)
	t = (t - t.mean()) / (t.std().clamp(min=1e-6))
	return t


WorldStep = TorchWorldStep

__all__ = ["WorldStep", "TorchWorldStep", "BatchedTorchWorldStep"]


class BatchedTorchWorldStep:
	"""Batched variant of TorchWorldStep that runs B independent reservoir worlds
	in a single set of GPU kernel launches.

	All fields carry a leading batch dimension B:
	  densityfield : (B, NZ, NY, NX)
	  flowfield    : (B, NZ, NY, NX, 3)
	  curlfield    : (B, NZ, NY, NX, 3)

	``reservoir_step`` accepts input_vectors of shape (B, input_size) and returns
	state of shape (B, state_size), eliminating the Python loop over batch items
	that exists in the unbatched path.
	"""

	def __init__(
		self,
		batch_size: int,
		base_eddy: float = 0.7,
		damping: float = 0.02,
		dispersion: float = -0.5,
		enable_particles: bool = True,
		particle_dispersion: int = 1,
		nx: int = 50,
		ny: int = 50,
		nz: int = 50,
		lx: float = 4.0,
		ly: float = 4.0,
		lz: float = 4.0,
		k1_size: int = 3,
		k2_size: int = 2,
		k3_size: int = 3,
		k4_size: int = 2,
		k5_size: int = 2,
		seed: int = 0,
		float_dtype: torch.dtype = torch.float32,
		particle_layout: str = "grid",
		particle_propagation_axis: str = "x",
		particle_wavelength_cells: Optional[float] = None,
		particle_line_dense_step: Optional[int] = None,
		particle_line_sparse_step: Optional[int] = None,
		particle_antipoint_mode: str = "offset",
		particle_grating_delay_frac: float = 0.25,
		probe_wema_alpha: float = 0.15,
		device: Optional[torch.device] = None,
	):
		self.B = int(batch_size)
		self.NX = int(nx)
		self.NY = int(ny)
		self.NZ = int(nz)
		self.LX = float(lx)
		self.LY = float(ly)
		self.LZ = float(lz)
		self.seed = int(seed)
		self.float_dtype = float_dtype
		self.device = device if device is not None else torch.device("cuda" if torch.cuda.is_available() else "cpu")

		self.base_eddy = float(base_eddy)
		self.dispersion = float(dispersion)
		self.damping = float(damping)
		self.enable_particles = bool(enable_particles)
		self.particle_dispersion = int(particle_dispersion)
		self.particle_layout = str(particle_layout).lower()
		self.particle_propagation_axis = str(particle_propagation_axis).lower()
		self.particle_wavelength_cells = particle_wavelength_cells
		self.particle_line_dense_step = particle_line_dense_step
		self.particle_line_sparse_step = particle_line_sparse_step
		self.particle_antipoint_mode = str(particle_antipoint_mode).lower()
		self.particle_grating_delay_frac = float(particle_grating_delay_frac)
		self.probe_wema_alpha = float(probe_wema_alpha)

		if self.probe_wema_alpha <= 0.0 or self.probe_wema_alpha > 1.0:
			raise ValueError(f"probe_wema_alpha must be in (0, 1], got {self.probe_wema_alpha}")

		TorchWorldStep._validate_particle_layout(self, self.particle_layout)
		TorchWorldStep._validate_particle_axis(self, self.particle_propagation_axis)
		TorchWorldStep._validate_particle_antipoint_mode(self, self.particle_antipoint_mode)

		self.k1_size = int(k1_size)
		self.k2_size = int(k2_size)
		self.k3_size = int(k3_size)
		self.k4_size = int(k4_size)
		self.k5_size = int(k5_size)

		# Reuse kernel weight/shift computation — it only touches scalar/list attrs
		# and self.float_dtype / self.device which are already set above.
		TorchWorldStep.init_kernels(self)

		self.densityfield = torch.zeros((self.B, self.NZ, self.NY, self.NX), dtype=self.float_dtype, device=self.device)
		self.flowfield = torch.zeros((self.B, self.NZ, self.NY, self.NX, 3), dtype=self.float_dtype, device=self.device)
		self.curlfield = torch.zeros((self.B, self.NZ, self.NY, self.NX, 3), dtype=self.float_dtype, device=self.device)
		self.curlfield_prev = torch.zeros_like(self.curlfield)

		self.reservoir_probe_idx = None
		self.reservoir_include_particles = True
		self.reservoir_include_global_moments = True
		self.antipodal_inputs_attached = True
		self._uniform_probe_idx_cache: dict[int, torch.Tensor] = {}
		self._probe_wema_mean: Optional[torch.Tensor] = None
		self._probe_wema_second: Optional[torch.Tensor] = None
		self._probe_wema_square_mean: Optional[torch.Tensor] = None
		self._probe_wema_square_second: Optional[torch.Tensor] = None

		self.particles = torch.zeros((self.B, 0, 3), dtype=self.float_dtype, device=self.device)
		self.particles2 = torch.zeros((self.B, 0, 3), dtype=self.float_dtype, device=self.device)
		self.particles_vel = torch.zeros((self.B, 0, 3), dtype=self.float_dtype, device=self.device)
		self.particles2_vel = torch.zeros((self.B, 0, 3), dtype=self.float_dtype, device=self.device)
		self.num_particles = 0
		if self.enable_particles:
			self._init_particles()

		seeds = list(range(seed, seed + self.B))
		self._init_densityfield(seeds)
		self._init_flowfield(seeds)

		bytes_per_element = torch.finfo(self.float_dtype).bits // 8
		# densityfield + flowfield + curlfield + curlfield_prev
		n_elements = (
			self.B * self.NZ * self.NY * self.NX           # densityfield
			+ self.B * self.NZ * self.NY * self.NX * 3     # flowfield
			+ self.B * self.NZ * self.NY * self.NX * 3     # curlfield
			+ self.B * self.NZ * self.NY * self.NX * 3     # curlfield_prev
		)
		total_bytes = n_elements * bytes_per_element
		total_mb = total_bytes / (1024 ** 2)
		print(
			f"[BatchedTorchWorldStep] B={self.B} grid=({self.NZ}x{self.NY}x{self.NX}) "
			f"dtype={self.float_dtype} device={self.device} "
			f"field_memory={total_mb:.2f} MB"
		)

	# ------------------------------------------------------------------
	# Initialisation helpers
	# ------------------------------------------------------------------

	def _init_densityfield(self, seeds: list) -> None:
		slices = []
		for s in seeds:
			g = torch.Generator(device=self.device)
			g.manual_seed(int(s))
			slices.append(
				(2.0 * torch.rand((self.NZ, self.NY, self.NX), generator=g, device=self.device) - 1.0).to(self.float_dtype)
			)
		self.densityfield = torch.stack(slices, dim=0)  # (B, NZ, NY, NX)

	def _init_flowfield(self, seeds: list, magnitude: float = 2.0) -> None:
		slices = []
		for s in seeds:
			g = torch.Generator(device=self.device)
			g.manual_seed(int(s))
			vecs = torch.randn((self.NZ, self.NY, self.NX, 3), generator=g, device=self.device, dtype=self.float_dtype)
			norms = torch.linalg.norm(vecs, dim=-1, keepdim=True).clamp_min(1e-9)
			slices.append((vecs / norms) * magnitude)
		self.flowfield = torch.stack(slices, dim=0)  # (B, NZ, NY, NX, 3)

	def _init_particles(self) -> None:
		# Not required for basic demo; placeholder to keep API
		pass

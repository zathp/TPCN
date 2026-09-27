import glfw
import numpy as np
import OpenGL.GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import tempfile
import os

try:
	import cupy as cp
except Exception:
	cp = None

try:
	import torch
except Exception:
	torch = None

def _to_numpy(x):
	"""Convert torch/cupy/numpy-like arrays to host numpy arrays."""
	if x is None:
		return None
	if torch is not None and isinstance(x, torch.Tensor):
		return x.detach().float().cpu().numpy()
	if cp is not None and isinstance(x, cp.ndarray):
		return cp.asnumpy(x)
	return np.asarray(x)

def _first_world_field(field):
	"""If a field is batched, select batch index 0."""
	shape = getattr(field, "shape", None)
	if shape is None:
		return field
	rank = len(shape)
	if rank in (4, 5):
		return field[0]
	return field

POINTS_VERT = """
#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color_in;
layout(location = 2) in float size_in;
layout(location = 3) in float alpha_in;
uniform mat4 mvp;
uniform float min_size;
out vec3 color;
out float alpha;
void main() {
	gl_Position = mvp * vec4(position, 1.0);
	color = color_in;
	alpha = alpha_in;
	gl_PointSize = max(size_in, min_size);
}
"""

POINTS_FRAG = """
#version 330 core
in vec3 color;
in float alpha;
out vec4 out_col;
void main() {
	out_col = vec4(color, alpha);
}
"""

def _create_shader():
	return compileProgram(compileShader(POINTS_VERT, gl.GL_VERTEX_SHADER), compileShader(POINTS_FRAG, gl.GL_FRAGMENT_SHADER))

def _resolve_model_step_callback(step_callback=None, model_callbacks=None, selected_model=None):
	"""Resolve a single per-frame model callback.

	Priority:
	1) explicit step_callback
	2) selected item from model_callbacks
	"""
	if step_callback is not None:
		return step_callback, None

	if not model_callbacks:
		return None, None

	model_names = list(model_callbacks.keys())
	if len(model_names) == 0:
		return None, None

	chosen = selected_model
	if chosen is None:
		if len(model_names) == 1:
			chosen = model_names[0]
		else:
			print("Available models:")
			for idx, name in enumerate(model_names, 1):
				print(f"  [{idx}] {name}")
			raw = input("Select model by index or name: ").strip()
			if raw.isdigit():
				i = int(raw)
				if i < 1 or i > len(model_names):
					raise ValueError(f"Invalid model index {i}. Must be in [1, {len(model_names)}].")
				chosen = model_names[i - 1]
			else:
				chosen = raw

	if chosen not in model_callbacks:
		raise ValueError(f"Unknown model '{chosen}'. Available: {model_names}")

	print(f"Using model callback: {chosen}")
	return model_callbacks[chosen], chosen

def build_density_vertices(sim):
	"""Build vertex array for volumetric density field rendering.
	Returns (N, 8) array: [x, y, z, r, g, b, size, alpha]
	"""
	field = _first_world_field(sim.densityfield)
	field_np = _to_numpy(field)  # (NZ, NY, NX)

	x = np.linspace(-sim.LX * (sim.NX - 1) / 2, sim.LX * (sim.NX - 1) / 2, sim.NX)
	y = np.linspace(-sim.LY * (sim.NY - 1) / 2, sim.LY * (sim.NY - 1) / 2, sim.NY)
	z = np.linspace(-sim.LZ * (sim.NZ - 1) / 2, sim.LZ * (sim.NZ - 1) / 2, sim.NZ)

	X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
	positions = np.stack([X, Y, Z], axis=-1).reshape(-1, 3)

	density_values = field_np.T.flatten()

	colors = np.zeros((len(density_values), 3), dtype=np.float32)
	alphas = np.abs(density_values)
	alpha_max = np.percentile(alphas, 95) if alphas.max() > 0 else 1.0
	alphas = np.clip(alphas / (alpha_max + 1e-6), 0.0, 1.0)

	pos_mask = density_values > 0
	neg_mask = density_values < 0
	colors[pos_mask, 0] = 1.0
	colors[pos_mask, 1] = 0.3
	colors[pos_mask, 2] = 0.3
	colors[neg_mask, 0] = 0.3
	colors[neg_mask, 1] = 0.3
	colors[neg_mask, 2] = 1.0

	sizes = (5.0 + 15.0 * alphas).astype(np.float32)
	alphas = (alphas * 0.5).astype(np.float32)

	return np.column_stack([positions, colors, sizes, alphas]).astype(np.float32)


def _build_density_points(sim, n_probe=4096):
	"""Extract up to `n_probe` voxels from the density field as a float32 vertex array.

	Each vertex: [x, y, z, r, g, b, size, alpha]  (8 floats)
	  - Positive density → red, negative → blue
	  - Size and alpha proportional to |density|
	Returns: numpy float32 array of shape (N, 8)
	"""
	density = _first_world_field(sim.densityfield)   # (NZ, NY, NX)
	NZ, NY, NX = sim.NZ, sim.NY, sim.NX
	LX, LY, LZ = float(sim.LX), float(sim.LY), float(sim.LZ)

	total = NZ * NY * NX
	n = min(n_probe, total)
	flat_idx = np.linspace(0, total - 1, n, dtype=np.int64)

	iz = flat_idx // (NY * NX)
	rem = flat_idx % (NY * NX)
	iy = rem // NX
	ix = rem % NX

	d_np = _to_numpy(density)  # (NZ, NY, NX) float32

	x = (ix + 0.5) * LX / NX - LX * 0.5
	y = (iy + 0.5) * LY / NY - LY * 0.5
	z = (iz + 0.5) * LZ / NZ - LZ * 0.5
	d = d_np[iz, iy, ix].astype(np.float32)

	pos_d = np.clip(d, 0.0, 1.0)
	neg_d = np.clip(-d, 0.0, 1.0)

	r = pos_d
	g = np.zeros(n, dtype=np.float32)
	b = neg_d

	mag = np.abs(d)
	size = (2.0 + mag * 6.0).astype(np.float32)
	alpha = np.clip(0.15 + mag * 0.85, 0.0, 1.0).astype(np.float32)

	verts = np.stack(
		[x.astype(np.float32), y.astype(np.float32), z.astype(np.float32),
		 r, g, b, size, alpha], axis=1
	)
	return verts


def run_viewer(
		sim,
		width=1000,
		height=800,
		print_timings=False,
		step_callback=None,
		model_callbacks=None,
		selected_model=None,
		dt=0.05):
	if not glfw.init():
		raise RuntimeError("Failed to init GLFW")

	model_step_callback, _ = _resolve_model_step_callback(
		step_callback=step_callback,
		model_callbacks=model_callbacks,
		selected_model=selected_model,
	)

	glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
	glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
	glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

	window = glfw.create_window(width, height, "3D Points + Bounding Box", None, None)
	if not window:
		glfw.terminate()
		raise RuntimeError("Failed to create window")

	glfw.make_context_current(window)
	glfw.swap_interval(1)

	shader = _create_shader()
	gl.glUseProgram(shader)

	# Create buffers
	vao = gl.glGenVertexArrays(1)
	gl.glBindVertexArray(vao)

	vbo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
	max_points = int(getattr(sim, "num_particles", 0))
	if max_points <= 0:
		max_points = int(max(1, sim.NX * sim.NY * sim.NZ))
	float_size = 4
	vertex_stride = 8 * float_size  # position(3) + color(3) + size(1) + alpha(1)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, max_points * vertex_stride, None, gl.GL_DYNAMIC_DRAW)

	# position attribute
	gl.glEnableVertexAttribArray(0)
	gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, vertex_stride, gl.ctypes.c_void_p(0))
	# color attribute
	gl.glEnableVertexAttribArray(1)
	gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, vertex_stride, gl.ctypes.c_void_p(12))
	# size attribute
	gl.glEnableVertexAttribArray(2)
	gl.glVertexAttribPointer(2, 1, gl.GL_FLOAT, gl.GL_FALSE, vertex_stride, gl.ctypes.c_void_p(24))
	# alpha attribute
	gl.glEnableVertexAttribArray(3)
	gl.glVertexAttribPointer(3, 1, gl.GL_FLOAT, gl.GL_FALSE, vertex_stride, gl.ctypes.c_void_p(28))

	# Bounding box line setup (12 edges * 2 vertices)
	box_vao = gl.glGenVertexArrays(1)
	gl.glBindVertexArray(box_vao)
	box_vbo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, box_vbo)

	gl.glEnable(gl.GL_DEPTH_TEST)
	gl.glEnable(gl.GL_PROGRAM_POINT_SIZE)
	gl.glEnable(gl.GL_BLEND)
	gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

	# Camera / bounding box setup
	x_min = -sim.LX * (sim.NX - 1) / 2.0
	x_max =  sim.LX * (sim.NX - 1) / 2.0
	y_min = -sim.LY * (sim.NY - 1) / 2.0
	y_max =  sim.LY * (sim.NY - 1) / 2.0
	z_min = -sim.LZ * (sim.NZ - 1) / 2.0
	z_max =  sim.LZ * (sim.NZ - 1) / 2.0

	sim_extent = max(x_max - x_min, y_max - y_min, z_max - z_min)
	radius = sim_extent * 1.5

	up = np.array([0.0, 0.0, 1.0], dtype=np.float32)
	if sim.NZ <= 2:
		eye = np.array([0.0, 0.0, radius], dtype=np.float32)
	elif sim.NY <= 2:
		eye = np.array([0.0, radius, 0.0], dtype=np.float32)
	elif sim.NX <= 2:
		eye = np.array([radius, 0.0, 0.0], dtype=np.float32)
	else:
		eye = np.array([radius * 0.6, radius * 0.6, radius * 0.4], dtype=np.float32)

	center = np.array([0.0, 0.0, 0.0], dtype=np.float32)

	camera_radius = float(radius)
	dir_vec_init = eye - center
	dir_len = np.linalg.norm(dir_vec_init) + 1e-9
	dir_unit = dir_vec_init / dir_len
	initial_pitch = float(np.arcsin(np.clip(dir_unit[2], -1.0, 1.0)))
	initial_yaw   = float(np.arctan2(dir_unit[1], dir_unit[0]))
	yaw   = initial_yaw
	pitch = initial_pitch
	roll  = np.pi / 2

	cam_bounds_min = np.array([x_min * 2, y_min * 2, z_min * 2], dtype=np.float32)
	cam_bounds_max = np.array([x_max * 2, y_max * 2, z_max * 2], dtype=np.float32)
	cam_radius_min = 1.0
	cam_radius_max = 2000.0

	paused = False

	def key_cb(window, key, scancode, action, mods):
		nonlocal paused, camera_radius, center, yaw, pitch, roll
		if action == glfw.PRESS:
			if key == glfw.KEY_SPACE:
				paused = not paused
			elif key == glfw.KEY_KP_ADD or key == glfw.KEY_EQUAL:
				camera_radius *= 0.85
			elif key == glfw.KEY_KP_SUBTRACT or key == glfw.KEY_MINUS:
				camera_radius *= 1.15
			elif key == glfw.KEY_R:
				camera_radius = float(radius)
				center[:] = 0.0
				yaw   = initial_yaw
				pitch = initial_pitch
			elif key == glfw.KEY_D:
				try:
					dump_path = os.path.join(tempfile.gettempdir(), 'flowstep_dump.npz')
					flow_np    = _to_numpy(_first_world_field(sim.flowfield))
					curl_np    = _to_numpy(_first_world_field(sim.curlfield))
					density_np = _to_numpy(_first_world_field(sim.densityfield))
					np.savez(dump_path, flowfield=flow_np, curlfield=curl_np,
					         densityfield=density_np,
					         NX=sim.NX, NY=sim.NY, NZ=sim.NZ,
					         LX=sim.LX, LY=sim.LY, LZ=sim.LZ)
					print(f"Dumped to {dump_path}")
				except Exception as e:
					print(f"Error dumping: {e}")
			elif key == glfw.KEY_ESCAPE:
				glfw.set_window_should_close(window, True)
			# strafe / pan with IJKL + H
			elif key in (glfw.KEY_J, glfw.KEY_L, glfw.KEY_I, glfw.KEY_K, glfw.KEY_H):
				dir_vec = np.array([np.cos(pitch) * np.cos(yaw),
				                    np.cos(pitch) * np.sin(yaw),
				                    np.sin(pitch)], dtype=np.float32)
				eye_pos  = center + dir_vec * camera_radius
				forward  = center - eye_pos
				forward /= np.linalg.norm(forward) + 1e-9
				right    = np.array([-np.sin(roll), np.cos(roll), 0.0], dtype=np.float32)
				scale    = camera_radius * 0.02
				fwd_scale = camera_radius * 0.05
				if key == glfw.KEY_J:
					center += (-scale) * right
				elif key == glfw.KEY_L:
					center += scale * right
				elif key == glfw.KEY_I:
					center += fwd_scale * forward
				elif key == glfw.KEY_K:
					center -= fwd_scale * forward
				elif key == glfw.KEY_H:
					center += scale * up
				center = np.clip(center, cam_bounds_min, cam_bounds_max)
		camera_radius = float(np.clip(camera_radius, cam_radius_min, cam_radius_max))

	glfw.set_key_callback(window, key_cb)

	rotating = False
	rolling   = False
	panning   = False
	last_x = 0.0
	last_y = 0.0

	def scroll_cb(window, xoffset, yoffset):
		nonlocal camera_radius
		camera_radius = float(np.clip(camera_radius * (0.9 ** float(yoffset)),
		                              cam_radius_min, cam_radius_max))

	def mouse_button_cb(window, button, action, mods):
		nonlocal rotating, rolling, panning, last_x, last_y
		if button == glfw.MOUSE_BUTTON_LEFT:
			rotating = (action == glfw.PRESS)
			if rotating:
				last_x, last_y = glfw.get_cursor_pos(window)
		elif button == glfw.MOUSE_BUTTON_MIDDLE:
			rolling = (action == glfw.PRESS)
			if rolling:
				last_x, last_y = glfw.get_cursor_pos(window)
		elif button == glfw.MOUSE_BUTTON_RIGHT:
			panning = (action == glfw.PRESS)
			if panning:
				last_x, last_y = glfw.get_cursor_pos(window)

	def cursor_pos_cb(window, x, y):
		nonlocal last_x, last_y, yaw, pitch, roll, center
		dx = x - last_x
		dy = y - last_y
		last_x, last_y = x, y
		if rotating:
			yaw   += dx * 0.005
			pitch  = float(np.clip(pitch - dy * 0.005, -1.49, 1.49))
		elif rolling:
			roll  += dx * 0.005
		elif panning:
			dir_vec = np.array([np.cos(pitch) * np.cos(roll),
			                    np.cos(pitch) * np.sin(roll),
			                    np.sin(pitch)], dtype=np.float32)
			eye_pos  = center + dir_vec * camera_radius
			forward  = center - eye_pos
			forward /= np.linalg.norm(forward) + 1e-9
			right    = np.array([-np.sin(roll), np.cos(roll), 0.0], dtype=np.float32)
			up_cam   = np.cross(right, forward)
			scale    = camera_radius * 0.002
			center  += (-dx * scale) * right + (dy * scale) * up_cam
			center   = np.clip(center, cam_bounds_min, cam_bounds_max)

	glfw.set_scroll_callback(window, scroll_cb)
	glfw.set_mouse_button_callback(window, mouse_button_cb)
	glfw.set_cursor_pos_callback(window, cursor_pos_cb)

	fov    = 60.0
	aspect = width / height
	near   = 1.0
	far    = 5000.0
	proj   = pyrr.matrix44.create_perspective_projection_matrix(fov, aspect, near, far, dtype=np.float32)

	mvp_loc      = gl.glGetUniformLocation(shader, "mvp")
	min_size_loc = gl.glGetUniformLocation(shader, "min_size")

	# Bounding box
	corners = np.array([
		[x_min, y_min, z_min], [x_max, y_min, z_min],
		[x_max, y_max, z_min], [x_min, y_max, z_min],
		[x_min, y_min, z_max], [x_max, y_min, z_max],
		[x_max, y_max, z_max], [x_min, y_max, z_max],
	], dtype=np.float32)
	edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
	line_verts = np.empty((len(edges) * 2, 3), dtype=np.float32)
	for ei, (a, b) in enumerate(edges):
		line_verts[ei * 2]     = corners[a]
		line_verts[ei * 2 + 1] = corners[b]

	gl.glBindVertexArray(box_vao)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, box_vbo)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, line_verts.nbytes, line_verts, gl.GL_STATIC_DRAW)
	gl.glEnableVertexAttribArray(0)
	gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 12, gl.ctypes.c_void_p(0))

	frame    = 0
	vbo_size = max_points * vertex_stride

	while not glfw.window_should_close(window):
		w, h = glfw.get_framebuffer_size(window)
		gl.glViewport(0, 0, w, max(h, 1))
		gl.glClearColor(0.1, 0.1, 0.12, 1.0)
		gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

		if not paused:
			if model_step_callback is not None:
				try:
					model_step_callback()
				except Exception as e:
					print(f"[viz] step error: {e}")

		# Build vertices from density field
		verts = build_density_vertices(sim)

		# Upload
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
		size = verts.nbytes
		if size > vbo_size:
			gl.glBufferData(gl.GL_ARRAY_BUFFER, size, verts, gl.GL_DYNAMIC_DRAW)
			vbo_size = size
		else:
			gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, size, verts)

		# MVP
		dir_vec   = np.array([np.cos(pitch) * np.cos(roll),
		                      np.cos(pitch) * np.sin(roll),
		                      np.sin(pitch)], dtype=np.float32)
		eye_pos   = center + dir_vec * camera_radius
		right_vec = np.array([-np.sin(roll), np.cos(roll), 0.0], dtype=np.float32)
		view_dir  = center - eye_pos
		view_dir /= np.linalg.norm(view_dir) + 1e-9
		cam_up    = np.cross(right_vec, view_dir)
		cam_up   /= np.linalg.norm(cam_up) + 1e-9
		rolled_up = cam_up * np.cos(yaw) + right_vec * np.sin(yaw)
		view      = pyrr.matrix44.create_look_at(eye_pos, center, rolled_up, dtype=np.float32)
		mvp       = proj @ view
		mvp_T     = mvp.T.astype(np.float32)

		gl.glUseProgram(shader)
		gl.glUniformMatrix4fv(mvp_loc, 1, gl.GL_FALSE, mvp_T)
		gl.glUniform1f(min_size_loc, 3.0)

		# Draw density points
		gl.glBindVertexArray(vao)
		gl.glDrawArrays(gl.GL_POINTS, 0, verts.shape[0])

		# Draw bounding box
		gl.glBindVertexArray(box_vao)
		gl.glDisableVertexAttribArray(1)
		gl.glVertexAttrib3f(1, 1.0, 1.0, 1.0)
		gl.glDrawArrays(gl.GL_LINES, 0, line_verts.shape[0])
		gl.glEnableVertexAttribArray(1)
		gl.glBindVertexArray(0)

		glfw.swap_buffers(window)
		glfw.poll_events()
		frame += 1

	gl.glDeleteBuffers(1, [vbo])
	gl.glDeleteBuffers(1, [box_vbo])
	gl.glDeleteVertexArrays(1, [vao])
	gl.glDeleteVertexArrays(1, [box_vao])
	glfw.terminate()


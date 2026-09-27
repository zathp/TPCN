import torch
torch.autograd.set_detect_anomaly(True)

import sys
from pathlib import Path
WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from predictive_coding.reservoir.viz_points_3d import run_viewer
import torch

from predictive_coding.cpcn.cpcn import CPCN, CPCNConfig
from predictive_coding.cpcn.Helper.voice_predictive_coding import VoicePredictiveCodingModule
from predictive_coding.cpcn.Helper.WorldStep import HopfieldPCN, extract_face_features

import numpy as np
import importlib

# --- Load voice module ---
voice_ckpt_path = WORKSPACE_ROOT / "main_test" / "voice_predcode.pt"
voice_module = VoicePredictiveCodingModule(input_dim=64, embed_dim=32, n_identities=10, hidden_dim=32)
if voice_ckpt_path.exists():
    ckpt = torch.load(voice_ckpt_path, map_location="cpu")
    with torch.no_grad():
        voice_module.hidden.copy_(ckpt['hidden'])
        # Load state dict leniently: checkpoint may have a different architecture.
        try:
            voice_module.load_state_dict(ckpt['state_dict'], strict=False)
            print(f"Loaded voice module (lenient) from {voice_ckpt_path}")
        except Exception as exc:
            print(f"Warning: failed to load voice state_dict strictly: {exc}")
else:
    print(f"Voice checkpoint not found: {voice_ckpt_path}")

# --- Load face module ---
face_ckpt_path = WORKSPACE_ROOT / "main_test" / "hopfield_face.pt"
face_module = HopfieldPCN(input_dim=128, n_prototypes=10)
if face_ckpt_path.exists():
    ckpt = torch.load(face_ckpt_path, map_location="cpu")
    with torch.no_grad():
        face_module.memory.copy_(ckpt['memory'])
        face_module.W.data.copy_(ckpt['W'])
    print(f"Loaded face module from {face_ckpt_path}")
else:
    print(f"Face checkpoint not found: {face_ckpt_path}")

checkpoint_path = WORKSPACE_ROOT / "main_test" / "cpcn_epoch_10.pt"
cpcn = CPCN(cfg=CPCNConfig(), device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))
cpcn.voice_module = voice_module
cpcn.face_module = face_module
if checkpoint_path.exists():
    # Load leniently: checkpoint architecture may differ from current code.
    try:
        cpcn.load_state_dict(torch.load(checkpoint_path, map_location="cpu"), strict=False)
        print(f"Loaded CPCN checkpoint (lenient) from {checkpoint_path}")
    except Exception as exc:
        print(f"Warning: failed to load CPCN checkpoint strictly: {exc}")
else:
    print(f"CPCN checkpoint not found: {checkpoint_path}")

import time
import numpy as np
import sounddevice as sd
import cv2

step_counter = 0
training_paused = False

# Camera setup
cam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Microphone setup
mic_samplerate = 16000
mic_duration = 0.5  # seconds

def on_key(window, key, scancode, action, mods):
    global training_paused
    if action == 1:  # GLFW_PRESS
        if key == 32:  # Spacebar
            training_paused = not training_paused
            print(f"Training {'paused' if training_paused else 'resumed'} (spacebar)")

def get_live_face_feat():
    ok, frame = cam.read()
    if not ok or frame is None:
        return torch.randn(128)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))
    if len(faces) == 0:
        return torch.randn(128)
    x, y, w, h = [int(v) for v in max(faces, key=lambda f: int(f[2]) * int(f[3]))]
    face_roi = frame[y : y + h, x : x + w]
    # Use your existing extractor
    return extract_face_features(face_roi, input_dim=128, device=cpcn.device)

def get_live_voice_feat():
    try:
        audio = sd.rec(int(mic_samplerate * mic_duration), samplerate=mic_samplerate, channels=1, dtype='float32')
        sd.wait()
        audio = audio.flatten()
        # Simple feature: normalize and pad/truncate to 64
        audio = (audio - np.mean(audio)) / (np.std(audio) + 1e-6)
        if len(audio) < 64:
            audio = np.pad(audio, (0, 64 - len(audio)), mode='constant')
        elif len(audio) > 64:
            audio = audio[:64]
        return torch.from_numpy(audio).float().to(cpcn.device)
    except Exception:
        return torch.randn(64)

def debug_tensor_128_64(tensor, label):
    if isinstance(tensor, torch.Tensor) and tensor.shape == (128, 64):
        print(f"[DEBUG] {label}: shape={tensor.shape}, dtype={tensor.dtype}, device={tensor.device}, version={getattr(tensor, '_version', 'N/A')}, requires_grad={tensor.requires_grad}")

def live_train_step():
    global step_counter, training_paused
    if training_paused:
        time.sleep(0.01)
        return
    face_feat = get_live_face_feat()
    voice_feat = get_live_voice_feat()
    debug_tensor_128_64(face_feat, "face_feat (before step)")
    debug_tensor_128_64(voice_feat, "voice_feat (before step)")
    out = cpcn.step(face_features=face_feat, voice_features=voice_feat, train=True)
    # Print any [128, 64] tensors in output
    for k, v in out.__dict__.items():
        debug_tensor_128_64(v, f"out.{k} (after step)")
    step_counter += 1
    if step_counter % 20 == 0:
        print(f"Step {step_counter}: Global error={out.global_error:.4f}, Openness={out.openness:.3f}")
    time.sleep(0.01)

print("Launching live training + 3D neuron visualization for open reservoir...")
import glfw
glfw.set_key_callback = getattr(glfw, 'set_key_callback', None)
def run_viewer_with_pause(sim, **kwargs):
    window = None
    def _wrapped_step():
        live_train_step()
    # Run viewer and set key callback
    result = run_viewer(sim, step_callback=_wrapped_step, **kwargs)
    if glfw.set_key_callback:
        window = glfw.get_current_context()
        glfw.set_key_callback(window, on_key)
    return result

run_viewer_with_pause(cpcn._open, width=1000, height=800, dt=0.05)

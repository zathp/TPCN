import torch
import sounddevice as sd

class AnchorReadout:
    def __init__(self, text_dim=64, voice_dim=64, sample_rate=16000):
        self.text_dim = text_dim
        self.voice_dim = voice_dim
        self.sample_rate = sample_rate

    def live_text_output(self, input_tensor):
        # Print text output live
        if isinstance(input_tensor, torch.Tensor):
            text = f"Live Text Output: {input_tensor.tolist()}"
        else:
            text = str(input_tensor)
        print(text)
        return text

    def live_voice_output(self, input_tensor):
        # Play audio live using sounddevice
        if isinstance(input_tensor, torch.Tensor):
            audio = input_tensor.detach().cpu().numpy()
        else:
            audio = input_tensor
        if audio.ndim == 1:
            audio = audio.reshape(-1, 1)
        sd.play(audio, self.sample_rate, blocking=True)
        return audio

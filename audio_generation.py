import torch
from diffusers import DiffusionPipeline
from riffusion.spectrogram_image_converter import SpectrogramImageConverter
from riffusion.spectrogram_params import SpectrogramParams


def initialize_pipeline():
    """Initialize the DiffusionPipeline."""
    pipeline = DiffusionPipeline.from_pretrained("riffusion/riffusion-model-v1")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return pipeline.to(device)


def generate_audio(pipeline, prompt, negative_prompt):
    """Generate audio based on prompt using the pipeline."""
    params = SpectrogramParams()
    converter = SpectrogramImageConverter(params)
    spectrogram_image = pipeline(prompt, negative_prompt=negative_prompt, width=768).images[0]
    wav = converter.audio_from_spectrogram_image(image=spectrogram_image)
    wav.export('output.wav', format='wav')
    return 'output.wav', spectrogram_image

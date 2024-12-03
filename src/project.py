import pyaudio
import numpy as np
import pygame

# Our Constants
CHUNK = 1024               # Number of audio samples per frame
RATE = 44100               # Sampling rate in Hertz / Hz

# This is to set up the audio stream
def init_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    return stream, p

# This captures and processes audio data
def get_audio_data(stream):
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    volume = np.abs(data).mean()
    return volume


# Visualizer class to handle animations and rendering
class SoundVisualizer:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()


def draw_bars(self, volume):
        color_intensity = min(255, int(volume / 100))    # Normalize volume for color
        color = (color_intensity, 0, 255 - color_intensity)
        bar_width = int(self.width / 20)                 # Set number of bars
        for i in range(20):
            bar_height = int(volume / 1000)              # Scale the bar height with volume
            x = i * bar_width
            y = self.height - bar_height
            pygame.draw.rect(self.screen, color, (x, y, bar_width - 2, bar_height))
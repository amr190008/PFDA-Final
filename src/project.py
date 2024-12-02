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

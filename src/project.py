import wave
import os
import numpy as np
import pygame

# Constants
CHUNK = 1024
SAMPLE_RATE = 44100
SMOOTHING_FACTOR = 0.8  # Controls the smoothness of bar animation

# Function to list all WAV files in the directory
def list_audio_files(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith('.wav')]

# Read WAV file
def load_audio(file_path):
    try:
        wav = wave.open(file_path, 'rb')
        return wav
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

# Capture and process audio data using FFT
def get_frequency_data(wav):
    frames = wav.readframes(CHUNK)
    if not frames:
        return None
    data = np.frombuffer(frames, dtype=np.int16)
    if wav.getnchannels() == 2:
        data = data[::2]
    fft_data = np.fft.fft(data)
    magnitude = np.abs(fft_data[:CHUNK // 2])
    return magnitude

# Visualizer class to handle animations and rendering
class SoundVisualizer:
    def __init__(self, screen):
        self.screen = screen
        self.update_dimensions()
        self.smoothed_magnitudes = None
        self.bar_color = (255, 255, 255)  # Default color: white
        self.shape_mode = "bars"  # Default shape

    def update_dimensions(self):
        self.width, self.height = self.screen.get_size()

    def set_color(self, color):
        self.bar_color = color

    def set_shape_mode(self, mode):
        self.shape_mode = mode

    def draw_shapes(self, magnitude):
        num_bars = 60
        bar_width = self.width // num_bars
        max_height = self.height // 2

        # Smooth the magnitude values
        if self.smoothed_magnitudes is None:
            self.smoothed_magnitudes = np.zeros_like(magnitude)
        self.smoothed_magnitudes = (
            SMOOTHING_FACTOR * self.smoothed_magnitudes
            + (1 - SMOOTHING_FACTOR) * magnitude
        )

        # Normalize magnitude values
        normalized_magnitude = self.smoothed_magnitudes / self.smoothed_magnitudes.max()
        normalized_magnitude = np.clip(normalized_magnitude, 0, 1)

        for i in range(num_bars):
            if i >= len(normalized_magnitude):
                break
            bar_height = int(normalized_magnitude[i] * max_height)
            x = i * bar_width + bar_width // 2
            y = self.height // 2 - bar_height

            if self.shape_mode == "bars":
                pygame.draw.rect(self.screen, self.bar_color, (x - bar_width // 2, y, bar_width - 2, bar_height))
                pygame.draw.rect(self.screen, self.bar_color, (x - bar_width // 2, self.height // 2, bar_width - 2, bar_height))
            elif self.shape_mode == "circles":
                pygame.draw.circle(self.screen, self.bar_color, (x, y), bar_height // 4)
                pygame.draw.circle(self.screen, self.bar_color, (x, self.height // 2 + bar_height // 2), bar_height // 4)
            elif self.shape_mode == "diamonds":
                # Diamond shape (a rotated square)
                diamond_size = bar_width // 2
                points = [
                    (x, y - diamond_size),  # Top point
                    (x + diamond_size, y),  # Right point
                    (x, y + diamond_size),  # Bottom point
                    (x - diamond_size, y)   # Left point
                ]
                pygame.draw.polygon(self.screen, self.bar_color, points)
            elif self.shape_mode == "octagons":
                size = bar_height // 4
                points_up = [(x - size, y - size), (x + size, y - size), (x + 2 * size, y), (x + size, y + size),
                             (x - size, y + size), (x - 2 * size, y), (x - size, y - size)]
                pygame.draw.polygon(self.screen, self.bar_color, points_up)

def main():
    folder_path = r"C:\Users\anmir\OneDrive\Desktop\Programming for Digital Arts\Labs\PFDA-Final\src"

    audio_files = list_audio_files(folder_path)
    if not audio_files:
        print("No WAV files found in the folder.")
        return

    print("Available songs:")
    for idx, file in enumerate(audio_files, 1):
        print(f"{idx}. {file}")
    choice = int(input("Enter the number of the song you want to play: ")) - 1

    if choice < 0 or choice >= len(audio_files):
        print("Invalid choice. Exiting.")
        return

    file_path = os.path.join(folder_path, audio_files[choice])

    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Sound Visualizer")

    wav = load_audio(file_path)
    if wav is None:
        return

    visualizer = SoundVisualizer(screen)
    clock = pygame.time.Clock()
    running = True

    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                visualizer.update_dimensions()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    visualizer.set_color((255, 255, 255))  # White
                elif event.key == pygame.K_2:
                    visualizer.set_color((255, 165, 0))  # Orange
                elif event.key == pygame.K_3:
                    visualizer.set_color((255, 105, 180))  # Pink
                elif event.key == pygame.K_4:
                    visualizer.set_color((128, 0, 128))  # Purple
                elif event.key == pygame.K_5:
                    visualizer.set_color((255, 0, 0))  # Red
                elif event.key == pygame.K_6:
                    visualizer.set_shape_mode("circles")
                elif event.key == pygame.K_7:
                    visualizer.set_shape_mode("diamonds")
                elif event.key == pygame.K_8:
                    visualizer.set_shape_mode("octagons")
                elif event.key == pygame.K_9:
                    visualizer.set_shape_mode("bars")

        freq_data = get_frequency_data(wav)
        if freq_data is None:
            break

        screen.fill((0, 0, 0))
        visualizer.draw_shapes(freq_data)
        pygame.display.flip()
        clock.tick(30)

    wav.close()
    pygame.mixer.quit()
    pygame.quit()

if __name__ == "__main__":
    main()

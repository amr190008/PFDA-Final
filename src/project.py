import wave
import os
import numpy as np
import pygame

# Constants
CHUNK = 1024
SAMPLE_RATE = 44100
SMOOTHING_FACTOR = 0.8  # Controls the smoothness of animation


def list_audio_files():
    # List all WAV files in the same directory as the program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return [f for f in os.listdir(current_dir) if f.lower().endswith('.wav')]


def load_audio(file_path):
    # Read and load the selected WAV file
    try:
        return wave.open(file_path, 'rb')
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None


def get_frequency_data(wav):
    # Capture and process audio data using FFT
    frames = wav.readframes(CHUNK)
    if not frames:
        return None
    data = np.frombuffer(frames, dtype=np.int16)
    if wav.getnchannels() == 2:
        data = data[::2]
    fft_data = np.fft.fft(data)
    return np.abs(fft_data[:CHUNK // 2])


def select_song():
    # Prompt user to select a song from the same directory as the program
    audio_files = list_audio_files()
    if not audio_files:
        print("Error: No WAV files found in the current directory.")
        return None, None

    print("Available songs:")
    for idx, file in enumerate(audio_files, 1):
        print(f"{idx}. {file}")

    choice = input("Enter the number of the song you want to play: ")
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(audio_files):
        print("Error: Invalid choice.")
        return None, None

    selected_file = audio_files[int(choice) - 1]
    return selected_file, os.path.join(os.path.dirname(os.path.abspath(__file__)), selected_file)


class SoundVisualizer:
    def __init__(self, screen):
        self.screen = screen
        self.update_dimensions()
        self.smoothed_magnitudes = None
        self.bar_color = (255, 255, 255)  # Default color: white
        self.shape_mode = "bars"  # Default shape

    def update_dimensions(self):
        # This is to update the screen dimensions for resizing
        self.width, self.height = self.screen.get_size()

    def set_color(self, color):
        # This sets the color of visualizer shapes
        self.bar_color = color

    def set_shape_mode(self, mode):
        # Set the shape mode (bars, circles, diamonds, etc.)
        self.shape_mode = mode

    def draw_shapes(self, magnitude):
        # This draws the visualizer shapes based on the selected mode
        num_bars = 60
        bar_width = self.width // num_bars
        max_height = self.height // 2

        if self.smoothed_magnitudes is None:
            self.smoothed_magnitudes = np.zeros_like(magnitude)
        self.smoothed_magnitudes = (
            SMOOTHING_FACTOR * self.smoothed_magnitudes
            + (1 - SMOOTHING_FACTOR) * magnitude
        )

        normalized_magnitude = self.smoothed_magnitudes / self.smoothed_magnitudes.max()
        normalized_magnitude = np.clip(normalized_magnitude, 0, 1)

        for i in range(num_bars):
            if i >= len(normalized_magnitude):
                break
            bar_height = int(normalized_magnitude[i] * max_height)
            x = i * bar_width + bar_width // 2
            y = self.height // 2 - bar_height

            if self.shape_mode == "bars": # This is the regular shape of the visualizer
                pygame.draw.rect(self.screen, self.bar_color, (x - bar_width // 2, y, bar_width - 2, bar_height))
                pygame.draw.rect(self.screen, self.bar_color, (x - bar_width // 2, self.height // 2, bar_width - 2, bar_height))
            elif self.shape_mode == "circles": # This changes the shape of the visualizer to circles
                pygame.draw.circle(self.screen, self.bar_color, (x, y), bar_height // 4)
                pygame.draw.circle(self.screen, self.bar_color, (x, self.height // 2 + bar_height // 2), bar_height // 4)
            elif self.shape_mode == "diamonds": # This changes the shape of the visualizer to diamonds
                diamond_size = bar_width // 2
                points = [
                    (x, y - diamond_size),  # Top point
                    (x + diamond_size, y),  # Right point
                    (x, y + diamond_size),  # Bottom point
                    (x - diamond_size, y)   # Left point
                ]
                pygame.draw.polygon(self.screen, self.bar_color, points)
            elif self.shape_mode == "octagons": # This changes the shape of the visualizer to octagons
                size = bar_height // 4
                points_up = [(x - size, y - size), (x + size, y - size), (x + 2 * size, y), (x + size, y + size),
                             (x - size, y + size), (x - 2 * size, y), (x - size, y - size)]
                pygame.draw.polygon(self.screen, self.bar_color, points_up)


def main():
    # Main function to initialize and run the program
    file_name, file_path = select_song()
    if not file_path:
        return

    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Sound Visualizer")

    wav = load_audio(file_path)
    if wav is None:
        return

    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    visualizer = SoundVisualizer(screen)
    clock = pygame.time.Clock()
    running = True
    paused = False  # This tracks the pause state, meaning to tell if the track is paused or not due to the boolean

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                visualizer.update_dimensions()
            elif event.type == pygame.KEYDOWN:
                # This allows the program to pause and unpause both music and visualizer
                if event.key == pygame.K_p:
                    if paused:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                    paused = not paused

                # This changes the bar color
                color_map = {
                    pygame.K_1: (255, 255, 255),  # White
                    pygame.K_2: (255, 165, 0),    # Orange
                    pygame.K_3: (255, 105, 180),  # Pink
                    pygame.K_4: (128, 0, 128),    # Purple
                    pygame.K_5: (255, 0, 0)       # Red
                }
                if event.key in color_map:
                    visualizer.set_color(color_map[event.key])

                # This changes the shape of the visualizer
                shape_map = {
                    pygame.K_6: "circles",
                    pygame.K_7: "diamonds",
                    pygame.K_8: "octagons",
                    pygame.K_9: "bars"
                }
                if event.key in shape_map:
                    visualizer.set_shape_mode(shape_map[event.key])

        if not paused:
            freq_data = get_frequency_data(wav)
            if freq_data is None:
                break

            screen.fill((0, 0, 0))
            visualizer.draw_shapes(freq_data)
            pygame.display.flip()
        else:
            # The visualizer is paused, display a pause messag
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 74)
            text = font.render("Paused", True, (255, 255, 255))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2,
                               screen.get_height() // 2 - text.get_height() // 2))
            pygame.display.flip()

        clock.tick(30)

    wav.close()
    pygame.mixer.quit()
    pygame.quit()


if __name__ == "__main__":
    main()

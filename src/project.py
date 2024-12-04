import wave
import os
import numpy as np
import pygame
import random

# Constants
CHUNK = 1024
SAMPLE_RATE = 44100
SMOOTHING_FACTOR = 0.8  # Controls the smoothness of animation
PARTICLE_LIFESPAN = 50  # Lifespan of particles in frames
PARTICLE_SPAWN_RATE = 10  # Number of particles spawned per frame

# Helper functions
def list_audio_files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return [f for f in os.listdir(current_dir) if f.lower().endswith('.wav')]

def load_audio(file_path):
    try:
        return wave.open(file_path, 'rb')
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None

def get_frequency_data(wav):
    frames = wav.readframes(CHUNK)
    if not frames:
        return None
    data = np.frombuffer(frames, dtype=np.int16)
    if wav.getnchannels() == 2:
        data = data[::2]
    fft_data = np.fft.fft(data)
    return np.abs(fft_data[:CHUNK // 2])

def select_song():
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

# Particle Class
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-5, -1)
        self.color = color
        self.lifespan = PARTICLE_LIFESPAN

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= 1

    def is_alive(self):
        return self.lifespan > 0

    def draw(self, screen):
        alpha = max(0, 255 * (self.lifespan / PARTICLE_LIFESPAN))
        surface = pygame.Surface((5, 5), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*self.color, int(alpha)), (2, 2), 2)
        screen.blit(surface, (self.x, self.y))

# Visualizer Class
class SoundVisualizer:
    def __init__(self, screen):
        self.screen = screen
        self.update_dimensions()
        self.smoothed_magnitudes = None
        self.bar_color = (255, 255, 255)
        self.shape_mode = "bars"
        self.particles = []
        self.trail_effect = False  # Trail effect is initially off

    def update_dimensions(self):
        self.width, self.height = self.screen.get_size()

    def set_color(self, color):
        self.bar_color = color

    def set_shape_mode(self, mode):
        self.shape_mode = mode

    def toggle_trail(self, state):
        self.trail_effect = state

    def spawn_particles(self, magnitude):
        intensity = np.mean(magnitude) / 50000
        num_particles = int(intensity * PARTICLE_SPAWN_RATE)
        for _ in range(num_particles):
            x = random.randint(0, self.width)
            y = self.height // 2
            self.particles.append(Particle(x, y, self.bar_color))

    def update_particles(self):
        for particle in self.particles:
            particle.move()
        self.particles = [p for p in self.particles if p.is_alive()]

    def draw_particles(self):
        for particle in self.particles:
            particle.draw(self.screen)

    def draw_shapes(self, magnitude):
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

            if self.shape_mode == "bars":
                pygame.draw.rect(self.screen, self.bar_color, (x - bar_width // 2, y, bar_width - 2, bar_height))
                pygame.draw.rect(self.screen, self.bar_color, (x - bar_width // 2, self.height // 2, bar_width - 2, bar_height))
            elif self.shape_mode == "circles":
                pygame.draw.circle(self.screen, self.bar_color, (x, y), bar_height // 4)
                pygame.draw.circle(self.screen, self.bar_color, (x, self.height // 2 + bar_height // 2), bar_height // 4)
            elif self.shape_mode == "diamonds":
                diamond_size = bar_width // 2
                points = [
                    (x, y - diamond_size),
                    (x + diamond_size, y),
                    (x, y + diamond_size),
                    (x - diamond_size, y)
                ]
                pygame.draw.polygon(self.screen, self.bar_color, points)

# Main program function
def main():
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
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                visualizer.update_dimensions()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if paused:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                    paused = not paused

                color_map = {
                    pygame.K_1: (255, 255, 255),
                    pygame.K_2: (255, 165, 0),
                    pygame.K_3: (255, 105, 180),
                    pygame.K_4: (128, 0, 128),
                    pygame.K_5: (255, 0, 0)
                }
                if event.key in color_map:
                    visualizer.set_color(color_map[event.key])

                shape_map = {
                    pygame.K_6: "bars",
                    pygame.K_7: "circles",
                    pygame.K_8: "diamonds"
                }
                if event.key in shape_map:
                    visualizer.set_shape_mode(shape_map[event.key])

                if event.key == pygame.K_9:
                    visualizer.toggle_trail(True)  # Enable trail effect
                elif event.key == pygame.K_0:
                    visualizer.toggle_trail(False)  # Disable trail effect

        if not paused:
            freq_data = get_frequency_data(wav)
            if freq_data is None:
                break

            visualizer.spawn_particles(freq_data)
            visualizer.update_particles()

            if visualizer.trail_effect:
                trail_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                trail_surface.fill((0, 0, 0, 50))  # Semi-transparent black
                screen.blit(trail_surface, (0, 0))
            else:
                screen.fill((0, 0, 0))

            visualizer.draw_particles()
            visualizer.draw_shapes(freq_data)
            pygame.display.flip()
        else:
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 74)
            text = font.render("Paused", True, (255, 255, 255))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2,
                               screen.get_height() // 2 - text.get_height() // 2))
            pygame.display.flip()

        clock.tick(30)

    wav.close()

if __name__ == "__main__":
    main()

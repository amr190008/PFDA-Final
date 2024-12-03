import wave
import os
import numpy as np
import pygame

# Constants
CHUNK = 1024  # Number of audio samples per frame

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

# Capture and process audio data
def get_audio_data(wav):
    frames = wav.readframes(CHUNK)
    if not frames:
        return None  # End of file
    data = np.frombuffer(frames, dtype=np.int16)
    volume = np.abs(data).mean()
    return volume

# Visualizer class to handle animations and rendering
class SoundVisualizer:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

    def draw_bars(self, volume):
        color_intensity = min(255, int(volume / 100))  # Normalize volume for color
        color = (color_intensity, 0, 255 - color_intensity)
        bar_width = int(self.width / 20)  # Set number of bars
        for i in range(20):
            bar_height = int(volume / 20)  # Scale the bar height with volume
            x = i * bar_width
            y = self.height - bar_height
            pygame.draw.rect(self.screen, color, (x, y, bar_width - 2, bar_height))

def main():
    # Directory where the songs are located
    folder_path = r"C:\Users\anmir\OneDrive\Desktop\Programming for Digital Arts\Labs\PFDA-Final\src"

    # List all WAV files
    audio_files = list_audio_files(folder_path)
    if not audio_files:
        print("No WAV files found in the folder.")
        return

    # Display files and let the user choose
    print("Available songs:")
    for idx, file in enumerate(audio_files, 1):
        print(f"{idx}. {file}")
    choice = int(input("Enter the number of the song you want to play: ")) - 1

    if choice < 0 or choice >= len(audio_files):
        print("Invalid choice. Exiting.")
        return

    # Selected file
    file_path = os.path.join(folder_path, audio_files[choice])

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Sound Visualizer")

    # Load audio file
    wav = load_audio(file_path)
    if wav is None:
        return  # Exit if file not found

    visualizer = SoundVisualizer(screen)
    clock = pygame.time.Clock()
    running = True

    # Play audio file
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get volume data
        volume = get_audio_data(wav)
        if volume is None:  # End of audio
            break

        # Update and draw visualizer
        screen.fill((0, 0, 0))  # Black background
        visualizer.draw_bars(volume)
        pygame.display.flip()
        clock.tick(30)  # 30 FPS

    # Cleanup
    wav.close()
    pygame.mixer.quit()
    pygame.quit()

if __name__ == "__main__":
    main()

# PFDA-Final
This is my final for PFDA which is Audio visualizer

# Title

Python Audio Visualizer

# Demo

Demo Video: https://youtu.be/6SsUfIcZjvk

## Repository

<Link to your project's public GitHub repository>

https://github.com/amr190008/PFDA-Final.git

## Description

The program represents digital art due to the audio visuals that will be captured from real-time audio input. My main inspiration is the EDM audio visualizers from YouTube that showcase the bass/flow of the song. It will also show us how our computer receives the audio and interprets it, while displaying it before us.

## Features

- **Feature 1**  
	- Capture audio and analyze the frequencies/volumes within it. I want it to capture the frequencies from an audio file first and hopefully implement live audio such as microphone. if 
  
- **Feature 2**  
	- Play visual effects from captured audio. I plan to have the visual effects correspond to the frequencies of the audio. For example, if the audio is really loud (peaking), I can play a specific color/shape to represent the audio is loud or vice versa. I could also use waveforms or particles that can potentially dance with the music. 
  
- **Feature 3**  
	- This is the innovation portion of my project in which I want to allow the user to customize the visuals based on either keyboard press or mouse click. Allow changing of color schemes, effects/patterns, or even sensitivity adjustment. I want to implement a recording and playback feature which will capture the audio then maybe create an animation file on playback.

## Challenges

- I will first need to install and learn PyAudio or wave which will help us capture the audio for visualization.
- Learn NumPy because when audio is captured from PyAudio, we then convert it to a NumPy array which allows us to analyze and process audio data.
- Learning the different animations/shapes and colors Pygame will allow me to effectively show off my audio visualizer as well as how to change animations based on certain frequencies/inputs.

## Outcomes

- **Ideal Outcome:**  
	The user will execute the program, and it will take in live audio which Pygame will capture. It will play animations/colors/shapes based on how the frequencies are. Meaning, if the audio is peaking, an animation/color will indicate this, or if it is soft. I took inspiration from EDM visualizers that show the bass and flow of EDM songs on YouTube. The user will be able to customize the visualizer as much as possible and implement animations based on both keyboard press and mouse clicking.

- **Minimal Viable Outcome:**  
	The visualizer will capture audio and play certain animations based on the frequencies. Not much customization or plain animations for capturing audio in the program. However, the goal is to allow customization from the user to make it interesting and exciting.

## Milestones

- **Week 1**
  1. Learning PyAudio/wave and how it allows us to capture the audio within Python.
  2. Capturing audio and being able to see waveforms/frequencies in real time.

- **Week 2**
  1. Implementing the first visualizations based on frequency data.
  2. Testing visualizer responsiveness to different types of audio input.

- **Week 3 (Final)**
  1. Enhancing customization options and polishing animations.
  2. Final testing and project submission.


- **Description of functions and effects used for visualizers**
  1. Implemented audio capture from WAV file
  2. Implemented animation of bars 
  3. Separated frequencies from bars into Bass, midrange, and treble
  4. Keyboard press 1 changes color of visualizer to white
  5. Keyboard press 2 changes color of visualizer to Orange
  6. Keyboard press 3 changes color of visualizer to Pink
  7. Keyboard press 4 changes color of visualizer to Purple
  8. Keyboard press 5 changes color of visualizer to Red
  9. Keyboard press 6 changes shape of visualizer to Default bars
 10. Keyboard press 7 changes shape of visualizer to circles 
 11. Keyboard press 8 changes shape of visualizer tov diamonds
 12. Keyboard press 9 turns on trail effect that gives the visualizer a bit of an after image effect on it
 13. Keyboard press 0 turns off trail effect
 14. Keyboard press P pauses and unpauses music and visualizer
 15. Visualizer has a particle effect on it and shows the amount of particles based on the frequencies of the song. For example if the song is slow the particles will barely
     show up. However in the second song the particles are abundant and are very prominent in the demo.

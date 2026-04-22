import pygame
import os

class MusicPlayer:
    def __init__(self, path):
        self.playlist = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp3')]
        self.current = 0
        self.playing = False

    def play(self):
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current])
            pygame.mixer.music.play()
            self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next(self):
        self.current = (self.current + 1) % len(self.playlist)
        self.play()

    def prev(self):
        self.current = (self.current - 1) % len(self.playlist)
        self.play()
import os
import time
import pygame
from typing import Optional, Callable

class AudioPlayer:
    def __init__(self, on_song_end: Optional[Callable[[], None]] = None):
        self.is_initialized = False
        self.is_playing = False
        self.is_paused = False
        self.current_file = ""
        self.volume = 0.7
        self.start_time = 0.0
        self.pause_offset = 0.0
        self.seek_offset = 0.0
        self.song_duration = 0
        self.on_song_end = on_song_end

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            pygame.mixer.music.set_volume(self.volume)
            self.is_initialized = True
        except Exception as e:
            print(f"[AudioPlayer] Mixer initialization error ({e}). Running in simulated audio mode.")

    def play(self, file_path: str, duration: int = 180, start_offset: float = 0.0):
        self.current_file = file_path
        self.song_duration = max(1, duration)
        self.start_time = time.time()
        self.pause_offset = 0.0
        self.seek_offset = max(0.0, start_offset)
        self.is_paused = False
        self.is_playing = True

        if self.is_initialized and file_path and os.path.exists(file_path):
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.set_volume(self.volume)
                if self.seek_offset > 0.0:
                    pygame.mixer.music.play(start=self.seek_offset)
                else:
                    pygame.mixer.music.play()
                return True
            except Exception as e:
                print(f"[AudioPlayer] Could not play file: {file_path} ({e})")
                return False
        return True

    def pause(self):
        if self.is_playing and not self.is_paused:
            if self.is_initialized and self.current_file and os.path.exists(self.current_file):
                try:
                    pygame.mixer.music.pause()
                except Exception:
                    pass
            self.pause_offset += (time.time() - self.start_time)
            self.is_paused = True

    def unpause(self):
        if self.is_playing and self.is_paused:
            if self.is_initialized and self.current_file and os.path.exists(self.current_file):
                try:
                    pygame.mixer.music.unpause()
                except Exception:
                    pass
            self.start_time = time.time()
            self.is_paused = False

    def toggle_play_pause(self):
        if not self.is_playing:
            return
        if self.is_paused:
            self.unpause()
        else:
            self.pause()

    def seek(self, seconds: float):
        if not self.is_playing:
            return
        seconds = max(0.0, min(float(self.song_duration), seconds))
        self.seek_offset = seconds
        self.start_time = time.time()
        self.pause_offset = 0.0

        if self.is_initialized and self.current_file and os.path.exists(self.current_file):
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.current_file)
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play(start=seconds)
                if self.is_paused:
                    pygame.mixer.music.pause()
            except Exception as e:
                print(f"[AudioPlayer] Seek error ({e})")

    def stop(self):
        if self.is_initialized:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
        self.is_playing = False
        self.is_paused = False
        self.current_file = ""
        self.pause_offset = 0.0
        self.seek_offset = 0.0

    def set_volume(self, val: float):
        """val: 0.0 to 1.0"""
        self.volume = max(0.0, min(1.0, val))
        if self.is_initialized:
            try:
                pygame.mixer.music.set_volume(self.volume)
            except Exception:
                pass

    def get_progress(self) -> float:
        """Returns elapsed seconds accurately."""
        if not self.is_playing:
            return 0.0
        if self.is_paused:
            return min(float(self.song_duration), self.seek_offset + self.pause_offset)

        elapsed = self.seek_offset + self.pause_offset + (time.time() - self.start_time)
        return min(float(self.song_duration), elapsed)

    def check_events(self):
        """Checks if song has finished playing without requiring pygame video events."""
        if not self.is_playing or self.is_paused:
            return

        elapsed = self.get_progress()
        if self.song_duration > 0 and elapsed >= self.song_duration:
            self.is_playing = False
            if self.on_song_end:
                self.on_song_end()
        elif self.is_initialized and self.current_file and os.path.exists(self.current_file):
            # Check if mixer finished playing
            if (time.time() - self.start_time) > 1.0 and not pygame.mixer.music.get_busy():
                self.is_playing = False
                if self.on_song_end:
                    self.on_song_end()

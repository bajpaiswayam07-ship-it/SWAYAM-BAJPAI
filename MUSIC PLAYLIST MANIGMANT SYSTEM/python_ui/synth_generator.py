import math
import struct
import wave
import os

def generate_track(filename: str, duration_sec: int = 15, chord_progression=None, base_freq: float = 220.0, tempo_bpm: int = 120):
    """
    Generates a high-quality melodic ambient/synth wave audio track using pure python wave module.
    Produces soothing chords and arpeggios so the music player plays real audio out-of-the-box.
    """
    sample_rate = 44100
    total_samples = int(sample_rate * duration_sec)
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if chord_progression is None:
        # Frequencies for pleasant chord progression (A minor, F major, C major, G major)
        chord_progression = [
            [220.0, 261.63, 329.63],       # Am (A3, C4, E4)
            [174.61, 220.0, 261.63],       # F  (F3, A3, C4)
            [261.63, 329.63, 392.0],       # C  (C4, E4, G4)
            [196.0, 246.94, 293.66],       # G  (G3, B3, D4)
        ]

    chord_duration = (60.0 / tempo_bpm) * 4.0 # 4 beats per chord
    max_amplitude = 12000.0

    samples = []
    for i in range(total_samples):
        t = i / sample_rate
        chord_idx = int(t / chord_duration) % len(chord_progression)
        chord = chord_progression[chord_idx]

        # Synth pad sound (sum of sine waves with gentle envelope)
        sample_val = 0.0
        for freq in chord:
            # Main wave + subtle octave harmonic + detune
            wave1 = math.sin(2.0 * math.pi * freq * t)
            wave2 = 0.3 * math.sin(2.0 * math.pi * (freq * 2.0) * t)
            wave3 = 0.2 * math.sin(2.0 * math.pi * (freq * 1.005) * t)
            sample_val += (wave1 + wave2 + wave3)

        # Arpeggiator note
        arp_speed = 8.0 # 8 notes per second
        arp_idx = int(t * arp_speed) % len(chord)
        arp_freq = chord[arp_idx] * 2.0
        arp_env = math.exp(-6.0 * ((t * arp_speed) - int(t * arp_speed)))
        sample_val += 0.8 * math.sin(2.0 * math.pi * arp_freq * t) * arp_env

        # Bass pulse on beat
        beat_t = (t * (tempo_bpm / 60.0)) % 1.0
        bass_env = math.exp(-4.0 * beat_t)
        bass_freq = chord[0] * 0.5
        sample_val += 0.9 * math.sin(2.0 * math.pi * bass_freq * t) * bass_env

        # Overall fade-in and fade-out
        fade_in = min(1.0, t / 0.8)
        fade_out = min(1.0, (duration_sec - t) / 1.0)
        envelope = fade_in * fade_out

        final_val = int(sample_val * (max_amplitude / (len(chord) + 1.5)) * envelope)
        final_val = max(-32767, min(32767, final_val))
        samples.append(final_val)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)      # Mono
        wav_file.setsampwidth(2)      # 16-bit
        wav_file.setframerate(sample_rate)
        raw_data = struct.pack(f'<{len(samples)}h', *samples)
        wav_file.writeframes(raw_data)

def generate_default_sample_tracks(audio_dir: str = "data/audio"):
    os.makedirs(audio_dir, exist_ok=True)
    tracks = [
        ("neon_nights.wav", 18, [[220, 261, 329], [174, 220, 261], [261, 329, 392], [196, 246, 293]], 128),
        ("chill_lofi_study.wav", 20, [[293, 349, 440], [220, 261, 329], [196, 246, 293], [174, 220, 261]], 85),
        ("cyber_pulse.wav", 16, [[130, 164, 196], [146, 174, 220], [164, 196, 246], [130, 164, 196]], 135),
        ("acoustic_breeze.wav", 18, [[261, 329, 392], [196, 246, 293], [220, 261, 329], [174, 220, 261]], 105),
        ("midnight_drift.wav", 22, [[220, 277, 329], [185, 220, 277], [164, 207, 246], [220, 277, 329]], 118),
    ]

    generated_paths = {}
    for fname, dur, chords, bpm in tracks:
        path = os.path.join(audio_dir, fname)
        if not os.path.exists(path):
            print(f"Generating sample audio track: {fname}...")
            generate_track(path, duration_sec=dur, chord_progression=chords, tempo_bpm=bpm)
        generated_paths[fname] = path
    return generated_paths

if __name__ == "__main__":
    generate_default_sample_tracks()
    print("All sample tracks generated successfully.")

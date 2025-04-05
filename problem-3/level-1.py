import librosa
import numpy as np
import argparse
import os

def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None, mono=True)
    return y, sr

def compute_spectral_flux(y, sr, hop_length=512):
    stft = np.abs(librosa.stft(y, hop_length=hop_length))
    flux = np.sqrt(np.sum(np.diff(stft, axis=1)**2, axis=0))
    flux = np.concatenate(([0], flux))  # match length
    times = librosa.frames_to_time(np.arange(len(flux)), sr=sr, hop_length=hop_length)
    return flux, times

def detect_peaks(flux, times, threshold_multiplier=1.3):
    mean_flux = np.mean(flux)
    threshold = threshold_multiplier * mean_flux

    peaks = []
    for i in range(1, len(flux)-1):
        if flux[i] > threshold and flux[i] > flux[i-1] and flux[i] > flux[i+1]:
            peaks.append(times[i])
    return peaks

def filter_beats(beat_times, min_interval=0.25):
    filtered = []
    last_time = -min_interval
    for t in beat_times:
        if t - last_time >= min_interval:
            filtered.append(round(t, 3))
            last_time = t
    return filtered

def main(audio_path):
    if not os.path.exists(audio_path):
        print("File does not exist.")
        return

    print(f"Analyzing (FFT-based): {audio_path}")
    y, sr = load_audio(audio_path)
    flux, times = compute_spectral_flux(y, sr)
    raw_peaks = detect_peaks(flux, times)
    beats = filter_beats(raw_peaks)

    print("\nDetected Beat Timestamps (seconds):")
    for t in beats:
        print(t)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FFT-based Beat Detector")
    parser.add_argument("file", help="Input .wav or .mp3 audio file")
    args = parser.parse_args()
    main(args.file)

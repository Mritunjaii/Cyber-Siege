import librosa
import numpy as np
import argparse
import os
from datetime import timedelta

def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None, mono=True)
    return y, sr

def compute_spectral_flux(y, sr, hop_length=512):
    stft = np.abs(librosa.stft(y, hop_length=hop_length))
    flux = np.sqrt(np.sum(np.diff(stft, axis=1)**2, axis=0))
    flux = np.concatenate(([0], flux))  # Align sizes
    times = librosa.frames_to_time(np.arange(len(flux)), sr=sr, hop_length=hop_length)
    return flux, times

def detect_peaks(flux, times, threshold_multiplier):
    mean_flux = np.mean(flux)
    threshold = threshold_multiplier * mean_flux

    peaks = []
    for i in range(1, len(flux) - 1):
        if flux[i] > threshold and flux[i] > flux[i - 1] and flux[i] > flux[i + 1]:
            peaks.append(times[i])
    return peaks

def filter_cut_markers(peak_times, min_cut_gap):
    filtered = []
    last_time = -min_cut_gap
    for t in peak_times:
        if t - last_time >= min_cut_gap:
            filtered.append(t)
            last_time = t
    return filtered

def skip_silent_sections(y, sr, cut_times, rms_threshold=0.01):
    rms = librosa.feature.rms(y=y)[0]
    rms_times = librosa.frames_to_time(np.arange(len(rms)), sr=sr)

    valid_times = []
    for t in cut_times:
        idx = np.searchsorted(rms_times, t)
        if idx < len(rms) and rms[idx] > rms_threshold:
            valid_times.append(t)
    return valid_times

def format_timestamp(seconds):
    td = timedelta(seconds=seconds)
    return str(td)[:11].zfill(12)  # Format: HH:MM:SS.MS

def main(audio_path, sensitivity=1.3, min_gap=0.5, rms_skip=0.01):
    if not os.path.exists(audio_path):
        print("❌ File not found.")
        return

    y, sr = load_audio(audio_path)
    flux, times = compute_spectral_flux(y, sr)
    peaks = detect_peaks(flux, times, threshold_multiplier=sensitivity)
    filtered_peaks = filter_cut_markers(peaks, min_cut_gap=min_gap)
    final_cuts = skip_silent_sections(y, sr, filtered_peaks, rms_threshold=rms_skip)

    formatted = [format_timestamp(t) for t in final_cuts]
    print("\n🎯 Cut Marker Timestamps (HH:MM:SS.MS):")
    for ts in formatted:
        print(ts)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio Cut Marker Generator (FFT-based)")
    parser.add_argument("file", help="Input .mp3 or .wav file")
    parser.add_argument("--sensitivity", type=float, default=1.3, help="Beat sensitivity (default: 1.3)")
    parser.add_argument("--min_gap", type=float, default=0.5, help="Minimum gap between cut points in seconds (default: 0.5)")
    parser.add_argument("--rms_skip", type=float, default=0.01, help="RMS threshold to skip low-energy segments (default: 0.01)")
    
    args = parser.parse_args()
    main(args.file, args.sensitivity, args.min_gap, args.rms_skip)

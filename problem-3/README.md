# FFT-Based Beat Detector

A Python tool for detecting beats in audio files using spectral flux analysis with FFT.

## Features

- Detects musical beats using spectral flux analysis
- Works with common audio formats (WAV, MP3, etc.)
- Configurable detection parameters
- Lightweight and fast processing

## Requirements

- Python 3.6+
- librosa
- numpy

## Installation


1. Install the required dependencies:
   ```bash
    pip install librosa numpy soundfile pydub
   ```

## Usage

Run the beat detector on an audio file:
```bash
python fft_beat_detector.py your_audio_file.mp3
```

### Output
The script will display detected beat timestamps in seconds:
```
Analyzing (FFT-based): your_audio_file.wav

Detected Beat Timestamps (seconds):
0.456
1.023
1.567
...
```

## Parameters

You can adjust the following parameters in the code:
- `hop_length`: FFT window hop size (default: 512)
- `threshold_multiplier`: Sensitivity for peak detection (default: 1.3)
- `min_interval`: Minimum time between beats in seconds (default: 0.25)

## Limitations

- Works best with music that has clear rhythmic patterns
- May produce false positives on complex audio with many transients
- Not optimized for real-time processing





## level2

# FFT-Based Audio Cut Marker Generator

A sophisticated Python tool for detecting optimal cut points in audio files using spectral analysis, with advanced filtering capabilities.

## Features

- **Precision Detection**: Uses spectral flux analysis with FFT for accurate beat detection
- **Smart Filtering**:
  - Minimum gap enforcement between cuts
  - Silent section skipping using RMS energy threshold
- **Customizable Parameters**: Adjust sensitivity, cut spacing, and silence thresholds
- **Professional Output**: Clean timestamp formatting (HH:MM:SS.MS)
- **Format Support**: Works with WAV, MP3, and other common audio formats

## Requirements

- Python 3.6+
- Librosa 0.8+
- NumPy



## Usage

Basic command:
```bash
python level-2.py audio_file.wav
```

Advanced options:
```bash
python level-2.py song.mp3 \
    --sensitivity 1.5 \
    --min_gap 0.3 \
    --rms_skip 0.02
```

### Output Example
```
🎯 Cut Marker Timestamps (HH:MM:SS.MS):
00:00:01.234
00:00:03.456
00:00:06.789
...
```

## Parameters

| Argument | Description | Default |
|----------|-------------|---------|
| `file` | Input audio file path | Required |
| `--sensitivity` | Detection sensitivity (higher = more cuts) | 1.3 |
| `--min_gap` | Minimum time between cuts (seconds) | 0.5 |
| `--rms_skip` | RMS threshold to skip silent sections | 0.01 |

## Advanced Configuration

For developers:
1. **Hop Length**: Adjust FFT window size in `compute_spectral_flux()`
2. **Peak Detection**: Modify threshold logic in `detect_peaks()`
3. **Timestamp Formatting**: Customize output in `format_timestamp()`

## Use Cases

- Video editing (automatic scene cuts)
- Podcast editing (remove silent sections)
- Music production (beat mapping)
- Audio analysis workflows

## Performance Notes

- Processing time scales with audio length
- 3-minute MP3 ≈ 2-3 seconds on modern hardware
- Memory usage remains low for most files


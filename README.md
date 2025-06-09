# Black Frame Detection

A simple Python script that scans videos for periods of pure black (or flash) frames. Automatically detecting these segments can help:

- **Quality Control**: Identify unwanted flashes or blank screens in your footage before final delivery.
- **Editing Efficiency**: Quickly locate and trim problematic sections.
- **Automation**: Integrate into CI/CD or batch-processing pipelines for large media libraries.

## How it Works

1. The script uses FFmpeg (and ffprobe) to analyze each video file for black frames.
2. Detected timecodes are converted into human-friendly `HH:MM:SS:FF` format, based on the video’s frame rate.
3. Results are printed to the console for easy review.

## Prerequisites

- **FFmpeg & ffprobe** must be installed and available on your PATH.
- After cloning, add your video files into the `media` folder at the project root (e.g. `media/Test_Video.mp4`).

## Usage

```bash
python framedetection.py media
```

This will scan every `*.mp4` file inside `media` and output black-frame timecodes in `HH:MM:SS:FF` format.

## Credits

This tool was coded with the help of ChatGPT — I just guided the process! 🤖
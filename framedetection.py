import subprocess
import re
import sys

mediaDir = "media"

import os
import glob

def detect_black_frames(video_path, duration_threshold=0.1):
    """
    Uses ffmpeg to detect black frames in a video.

    Args:
        video_path (str): Path to the video file.
        duration_threshold (float): Minimum black frame duration to be considered (in seconds).

    Returns:
        List of dicts with start, end, and duration of each black frame.
    """
    cmd = [
        'ffmpeg',
        '-hide_banner',
        '-i', video_path,
        '-vf', f'blackdetect=d={duration_threshold}:pic_th=0.98',
        '-an',  # Disable audio processing
        '-f', 'null',
        '-'
    ]

    result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    matches = re.findall(r'black_start:(\d+\.?\d*)\s+black_end:(\d+\.?\d*)\s+black_duration:(\d+\.?\d*)', result.stderr)

    black_frames = []
    for match in matches:
        black_frames.append({
            'start': float(match[0]),
            'end': float(match[1]),
            'duration': float(match[2]),
        })

    return black_frames

if __name__ == "__main__":
    if not os.path.isdir(mediaDir):
        print(f"Media directory '{mediaDir}' does not exist.")
        sys.exit(1)

    video_files = glob.glob(os.path.join(mediaDir, "*.mp4"))

    if not video_files:
        print(f"No MP4 files found in '{mediaDir}'.")
        sys.exit(1)

    for video_file in video_files:
        print(f"\nAnalyzing: {video_file}")
        results = detect_black_frames(video_file)

        if not results:
            print("No black frames detected.")
        else:
            print("Detected black frames:")
            for i, bf in enumerate(results, 1):
                print(f"{i}: Start={bf['start']}s, End={bf['end']}s, Duration={bf['duration']}s")
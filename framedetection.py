import subprocess
import re
import sys

mediaDir = "media"

import os
import glob

def get_fps(video_path):
    """
    Retrieve the frame rate of the given video using ffprobe.
    """
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=r_frame_rate',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    rate = result.stdout.strip()
    nums = rate.split('/')
    if len(nums) == 2 and nums[1] != '0':
        return float(nums[0]) / float(nums[1])
    try:
        return float(rate)
    except ValueError:
        return 0.0

def format_timecode(seconds, fps):
    """
    Convert a time in seconds to HH:MM:SS:FF timecode.
    """
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    f = int((seconds - int(seconds)) * fps)
    return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"

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

    fps = 0
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
        fps = get_fps(video_file)
        results = detect_black_frames(video_file)

        if not results:
            print("No black frames detected.")
        else:
            print("Detected black frames (HH:MM:SS:FF):")
            for i, bf in enumerate(results, 1):
                start_tc = format_timecode(bf['start'], fps)
                end_tc = format_timecode(bf['end'], fps)
                duration_tc = format_timecode(bf['duration'], fps)
                print(f"{i}: Start={start_tc}, End={end_tc}, Duration={duration_tc}")
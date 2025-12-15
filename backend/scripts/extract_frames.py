"""Download a video (YouTube etc.) and extract N evenly spaced frames.

Requires `yt-dlp` and `opencv-python`.

Usage:
  python extract_frames.py <video_url> <out_dir> [--frames N]
"""
import sys
from pathlib import Path
import subprocess
import tempfile
import shutil
import math
import os
import cv2


def download_video(url: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(".tmp.mp4")
    cmd = [
        "yt-dlp",
        "-f",
        "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4/best",
        "-o",
        str(tmp),
        url,
    ]
    subprocess.check_call(cmd)
    tmp.rename(out_path)
    return out_path


def extract_frames(video_path: Path, out_dir: Path, n_frames: int = 8):
    out_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError("cannot open video")
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count <= 0:
        frame_count = 1
    indices = [math.floor(i * frame_count / n_frames) for i in range(n_frames)]
    saved = 0
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        out_file = out_dir / f"frame_{saved:03d}.jpg"
        cv2.imwrite(str(out_file), frame)
        saved += 1
    cap.release()
    return saved


def main():
    if len(sys.argv) < 3:
        print("usage: extract_frames.py <video_url> <out_dir> [--frames N]")
        sys.exit(2)
    url = sys.argv[1]
    out_dir = Path(sys.argv[2])
    n = 8
    if len(sys.argv) > 3 and sys.argv[3].isdigit():
        n = int(sys.argv[3])

    with tempfile.TemporaryDirectory() as tmpdir:
        vfile = Path(tmpdir) / "video.mp4"
        print("downloading...", url)
        download_video(url, vfile)
        print("extracting frames to", out_dir)
        cnt = extract_frames(vfile, out_dir, n_frames=n)
        print("extracted", cnt, "frames")


if __name__ == "__main__":
    main()

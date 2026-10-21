"""Inspect actual video metadata and decode the entire delivered file."""
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import json
import math
import os
import shutil
import subprocess


def find_tool(explicit, name):
    candidate = explicit or os.environ.get(f'{name.upper()}_BINARY') or shutil.which(name)
    if not candidate:
        raise ValueError(f'{name} not found. Supply --{name} or {name.upper()}_BINARY.')
    return candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--ffmpeg')
    parser.add_argument('--ffprobe')
    parser.add_argument('--max-seconds', type=float)
    parser.add_argument('--width', type=int)
    parser.add_argument('--height', type=int)
    parser.add_argument('--fps', type=float)
    parser.add_argument('--expected-frames', type=int)
    parser.add_argument('--allow-silent', action='store_true')
    args = parser.parse_args()
    if not args.video.is_file():
        parser.error('Video file does not exist.')
    if args.report.resolve() == args.video.resolve():
        parser.error('Report cannot overwrite the video.')
    for field in ['max_seconds', 'width', 'height', 'fps', 'expected_frames']:
        value = getattr(args, field)
        if value is not None and (not math.isfinite(value) or value <= 0):
            parser.error(f'{field} must be a finite positive number.')
    try:
        ffprobe = find_tool(args.ffprobe, 'ffprobe')
        ffmpeg = find_tool(args.ffmpeg, 'ffmpeg')
        result = subprocess.run([ffprobe, '-v', 'error', '-show_entries',
          'format=duration,size:stream=codec_name,codec_type,width,height,r_frame_rate,nb_frames,sample_rate,channels,duration',
          '-of', 'json', str(args.video)], capture_output=True, text=True, check=True)
        metadata = json.loads(result.stdout)
        video = next((s for s in metadata['streams'] if s['codec_type'] == 'video'), None)
        audio = [s for s in metadata['streams'] if s['codec_type'] == 'audio']
        if video is None:
            raise ValueError('No video stream.')
        if not audio and not args.allow_silent:
            raise ValueError('No audio stream; use --allow-silent only for a silent brief.')
        container_seconds = float(metadata['format']['duration'])
        visual_seconds = float(video.get('duration', container_seconds))
        if not math.isfinite(container_seconds) or not math.isfinite(visual_seconds) or visual_seconds <= 0:
            raise ValueError('Missing or invalid duration.')
        if args.max_seconds and (visual_seconds > args.max_seconds + 1e-6 or container_seconds > args.max_seconds + .05):
            raise ValueError(f'Too long: video {visual_seconds}s, container {container_seconds}s; limit {args.max_seconds}s.')
        for key in ['width', 'height']:
            expected = getattr(args, key)
            if expected and int(video[key]) != expected:
                raise ValueError(f'{key} mismatch: {video[key]} vs {expected}.')
        fps = float(Fraction(video['r_frame_rate']))
        if args.fps and abs(fps - args.fps) > .0001:
            raise ValueError(f'FPS mismatch: {fps} vs {args.fps}.')
        if args.expected_frames and int(video.get('nb_frames', -1)) != args.expected_frames:
            raise ValueError('Frame count missing or different from storyboard.')
        result = subprocess.run([ffmpeg, '-v', 'error', '-threads', '3', '-i', str(args.video), '-f', 'null', '-'],
          capture_output=True, text=True)
        if result.returncode or result.stderr.strip():
            raise ValueError(f'Full decode failed: {result.returncode}: {result.stderr[-3000:]}')
        with args.video.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        report = {
          'video': str(args.video.resolve()), 'bytes': args.video.stat().st_size, 'sha256': digest,
          'metadata': metadata, 'visual_seconds': visual_seconds, 'container_seconds': container_seconds,
          'constraints': {key: getattr(args, key) for key in ['max_seconds', 'width', 'height', 'fps', 'expected_frames', 'allow_silent']},
          'full_decode': {'exit_code': 0, 'error_output': ''}, 'technical_checks': 'passed',
          'visual_review': 'Requires actual frame / motion inspection; not certified by this script.',
          'factual_review': 'Requires source verification; not certified by this script.',
        }
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'technical_checks': 'passed', 'visual_seconds': visual_seconds,
                          'container_seconds': container_seconds, 'report': str(args.report.resolve())}, ensure_ascii=False))
    except (ValueError, OSError, subprocess.CalledProcessError, KeyError) as error:
        parser.exit(1, f'Verification failed: {error}\n')


if __name__ == '__main__':
    main()

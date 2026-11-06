#!/usr/bin/env python3
"""Inspect a local still/animated image or video; never infer continuous motion.

Requires Python 3.10+ and Pillow; videos also require ffprobe and ffmpeg on PATH.
Output: lossless PNG samples, contact-sheet.jpg, and a timestamped manifest.json.
"""
import argparse
import bisect
import json
import math
import re
import shutil
import subprocess
import sys
import warnings
from fractions import Fraction
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageOps, UnidentifiedImageError
except ImportError:
    sys.exit("Missing Pillow. Install it in your Python environment: pip install Pillow")

warnings.simplefilter("error", Image.DecompressionBombWarning)


def number(value, default=None):
    try:
        result = float(Fraction(str(value)))
        return result if math.isfinite(result) else default
    except (ValueError, TypeError, ZeroDivisionError):
        return default


def run(args, timeout=60):
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise ValueError(f"{Path(args[0]).name} exceeded {timeout}s; try a shorter/local clip.") from exc
    if result.returncode:
        raise ValueError(f"{Path(args[0]).name} failed: {result.stderr[-1800:].strip()}")
    return result


def window(args, duration):
    end = duration if args.end is None else args.end
    if not (0 <= args.start < end <= duration + 1e-6):
        raise ValueError(f"Require 0 <= start < end <= duration ({duration:.6f}s).")
    return args.start, min(end, duration)


def targets(start, end, count, fps):
    # Include the opening and last decodable vicinity, never seek to EOF itself.
    margin = min(1 / fps if fps and fps > 0 else 0.04, (end - start) / 2)
    return [start + (end - margin - start) * i / (count - 1) for i in range(count)]


def image_reference(src, out, args, notes):
    try:
        im = Image.open(src)
    except UnidentifiedImageError:
        return None
    with im:
        animated = bool(getattr(im, "is_animated", False))
        count = getattr(im, "n_frames", 1) if animated else 1
        if count > 10000:
            raise ValueError("Animated image exceeds 10,000 frames; trim it first.")
        meta = {"kind": "animated_image" if animated else "image", "format": im.format,
                "coded_width": im.width, "coded_height": im.height, "frame_count": count,
                "audio_present": False, "duration_seconds": None, "fps": None,
                "exif_orientation_applied": True}
        starts, durations, elapsed = [], [], 0.0
        if animated:
            for i in range(count):
                im.seek(i)
                duration = number(im.info.get("duration"))
                if duration is None or duration <= 0:
                    duration = 100.0
                    notes.append("Missing/zero image frame duration interpreted as 100 ms; timing is approximate.")
                starts.append(elapsed)
                durations.append(duration / 1000)
                elapsed += duration / 1000
            meta.update(duration_seconds=elapsed, fps=count / elapsed,
                        fps_basis="average over one cycle", variable_frame_timing=len(set(durations)) > 1)
            start, end = window(args, elapsed)
            selected = {}
            for t in targets(start, end, args.max_frames, meta["fps"]):
                selected.setdefault(max(0, bisect.bisect_right(starts, t) - 1), t)
        else:
            if args.start != 0 or args.end is not None:
                raise ValueError("--start/--end apply only to animated images or video.")
            start, end, selected = 0.0, None, {0: 0.0}
            notes.append("A still image does not establish motion, timing, camera movement, or hidden content.")
        samples = []
        for i, (frame, requested) in enumerate(selected.items(), 1):
            im.seek(frame)
            oriented = ImageOps.exif_transpose(im).convert("RGBA")
            file = f"frames/frame-{i:03d}.png"
            oriented.save(out / file)
            meta.update(width=oriented.width, height=oriented.height)
            samples.append({"file": file, "frame_index": frame,
                            "requested_time_seconds": requested,
                            "time_seconds": starts[frame] if animated else None,
                            "timestamp_basis": "frame onset in one cycle" if animated else "still image"})
        return meta, samples, {"start": start, "end": end}


def video_reference(src, out, args, notes):
    for executable in ("ffprobe", "ffmpeg"):
        if not shutil.which(executable):
            raise ValueError(f"Unsupported image or video: install {executable} and add it to PATH.")
    probe = json.loads(run(["ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe",
                            "-show_streams", "-show_format", "-of", "json", str(src)]).stdout)
    streams = probe.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"
                  and not s.get("disposition", {}).get("attached_pic")), None)
    if video is None:
        raise ValueError("Input has no video stream (audio-only media is not a visual reference).")
    container = probe.get("format", {})
    duration = number(video.get("duration")) or number(container.get("duration"))
    if not duration or duration <= 0:
        raise ValueError("Cannot determine a positive video duration; remux/trim the clip first.")
    fps = number(video.get("avg_frame_rate")) or number(video.get("r_frame_rate"))
    rotation = number(video.get("tags", {}).get("rotate"), 0)
    for side in video.get("side_data_list", []):
        rotation = number(side.get("rotation"), rotation)
    origin = number(container.get("start_time"), number(video.get("start_time"), 0))
    meta = {"kind": "video", "format": container.get("format_name"),
            "coded_width": video.get("width"), "coded_height": video.get("height"),
            "duration_seconds": duration, "fps": fps, "fps_basis": "reported average or nominal",
            "frame_count": number(video.get("nb_frames")), "source_start_time_seconds": origin,
            "audio_present": any(s.get("codec_type") == "audio" for s in streams),
            "rotation_degrees": rotation, "rotation_handling": "ffmpeg default autorotation"}
    start, end = window(args, duration)
    samples = []
    for i, t in enumerate(targets(start, end, args.max_frames, fps), 1):
        file = f"frames/frame-{i:03d}.png"
        result = run(["ffmpeg", "-hide_banner", "-loglevel", "info", "-nostdin", "-n",
                      "-protocol_whitelist", "file,pipe", "-ss", f"{t:.9f}", "-copyts",
                      "-i", str(src), "-map", f"0:{video['index']}", "-an", "-sn", "-dn",
                      "-vf", "showinfo", "-frames:v", "1", "-fps_mode", "passthrough",
                      "-threads", "1", str(out / file)])
        if not (out / file).is_file():
            raise ValueError(f"No frame decoded near {t:.6f}s; shorten --end or remux the clip.")
        match = re.search(r"\bn:\s*0\s+pts:\s*\S+\s+pts_time:([-+\d.eE]+)", result.stderr)
        pts = number(match.group(1)) if match else None
        with Image.open(out / file) as frame:
            meta.update(width=frame.width, height=frame.height)
        samples.append({"file": file, "requested_time_seconds": t,
                        "source_pts_seconds": pts, "time_seconds": pts - origin if pts is not None else t,
                        "timestamp_basis": "decoded PTS minus source start" if pts is not None else "requested seek (approximate)"})
    notes.append("Video timestamps identify sampled frames; seeking and variable frame rates can shift requested times.")
    notes.append("Color/HDR conversion is ffmpeg's default; samples are not a color-managed mastering reference.")
    return meta, samples, {"start": start, "end": end}


def contact_sheet(out, samples):
    columns, tile_w, tile_h, pad = min(4, len(samples)), 320, 212, 12
    rows = math.ceil(len(samples) / columns)
    sheet = Image.new("RGB", (columns * (tile_w + pad) + pad, rows * (tile_h + pad) + pad + 30), "#181b22")
    draw = ImageDraw.Draw(sheet)
    draw.text((pad, 10), "REFERENCE SAMPLES - motion/audio need review", fill="white")
    for i, sample in enumerate(samples):
        x, y = pad + (i % columns) * (tile_w + pad), 38 + (i // columns) * (tile_h + pad)
        with Image.open(out / sample["file"]) as frame:
            thumb = ImageOps.contain(frame.convert("RGBA"), (tile_w, tile_h - 24))
            # Neutral checkerboard reveals both dark and light transparent artwork.
            matte = Image.new("RGB", thumb.size, "#d8dce2")
            checker = ImageDraw.Draw(matte)
            for cy in range(0, thumb.height, 16):
                for cx in range(0, thumb.width, 16):
                    if (cx // 16 + cy // 16) % 2:
                        checker.rectangle((cx, cy, cx + 15, cy + 15), fill="#b0b6c0")
            matte.paste(thumb, (0, 0), thumb)
            sheet.paste(matte, (x + (tile_w - thumb.width) // 2, y))
        timestamp = sample["time_seconds"]
        label = "Still image" if timestamp is None else f"{timestamp:.3f} s"
        if "approximate" in sample["timestamp_basis"]:
            label += " (approx.)"
        draw.text((x, y + tile_h - 18), f"{i + 1:02d}  |  {label}", fill="white")
    sheet.save(out / "contact-sheet.jpg", quality=92)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Local image/GIF/video file; URLs are not fetched")
    parser.add_argument("--out", required=True, help="New or empty dedicated output directory")
    parser.add_argument("--max-frames", type=int, default=12, choices=range(3, 25), metavar="3..24")
    parser.add_argument("--start", type=float, default=0.0, help="Start in seconds (inclusive)")
    parser.add_argument("--end", type=float, help="End in seconds (exclusive)")
    args = parser.parse_args()
    try:
        if not math.isfinite(args.start) or args.start < 0 or (args.end is not None and not math.isfinite(args.end)):
            raise ValueError("Time bounds must be finite; --start must be non-negative.")
        src = Path(args.input).expanduser().resolve(strict=True)
        if not src.is_file():
            raise ValueError("Input must be a local regular file.")
        destination = Path(args.out).expanduser()
        if destination.is_symlink():
            raise ValueError("Output directory must not be a symbolic link.")
        out = destination.resolve()
        if out.exists() and (not out.is_dir() or any(out.iterdir())):
            raise ValueError(f"Output must be a new or empty directory; refusing to overwrite: {out}")
        out.mkdir(parents=True, exist_ok=True)
        (out / "frames").mkdir()
        notes = ["Sampled still frames do not prove continuous playback, transition quality, loop continuity, or audio quality.",
                 "Audio presence is metadata only; this helper neither plays nor listens to audio."]
        result = image_reference(src, out, args, notes)
        if result is None:
            result = video_reference(src, out, args, notes)
        meta, samples, bounds = result
        contact_sheet(out, samples)
        manifest = {"schema_version": 1, "source": str(src), "metadata": meta,
                    "window_seconds": bounds, "samples": samples, "sample_count": len(samples),
                    "contact_sheet": "contact-sheet.jpg", "limitations": list(dict.fromkeys(notes))}
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
        print(json.dumps({"manifest": str(out / "manifest.json"), "kind": meta["kind"], "samples": len(samples)}))
        return 0
    except (OSError, ValueError, EOFError, Image.DecompressionBombWarning, Image.DecompressionBombError) as exc:
        print(f"Error: {exc}\nPartial outputs, if any, are retained; retry with a new empty --out directory.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

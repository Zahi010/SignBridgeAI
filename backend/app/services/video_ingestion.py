"""
SignBridge AI - Human Sign Language Video Ingestion Pipeline.
Handles validation, metadata extraction via ffprobe, thumbnail generation via ffmpeg,
secure storage, and database persistence with strict provenance tracking.
"""

import json
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models.entities import SignRecord, SignVideo, ValidationStatus

MAX_VIDEO_SIZE_BYTES = 50 * 1024 * 1024 # 50 MB
ALLOWED_VIDEO_EXTS = {".mp4", ".webm", ".mov"}

def extract_video_metadata(file_path: Path) -> Dict[str, Any]:
    """
    Executes ffprobe to extract exact duration, resolution, codec, and frame rate.
    """
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(file_path)
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        probe_data = json.loads(result.stdout)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to probe video file headers: {str(e)}"
        )

    video_stream = next((s for s in probe_data.get("streams", []) if s.get("codec_type") == "video"), None)
    if not video_stream:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded media file does not contain a valid video stream."
        )

    width = int(video_stream.get("width", 0))
    height = int(video_stream.get("height", 0))
    duration_str = probe_data.get("format", {}).get("duration") or video_stream.get("duration", "0")
    duration = float(duration_str)
    codec = video_stream.get("codec_name", "unknown")
    
    # Calculate FPS
    r_frame_rate = video_stream.get("r_frame_rate", "25/1")
    try:
        num, den = r_frame_rate.split("/")
        fps = round(float(num) / float(den), 2)
    except Exception:
        fps = 25.0

    # Resolution label
    if height >= 1080:
        res_label = "1080p (FHD)"
    elif height >= 720:
        res_label = "720p (HD)"
    elif height >= 480:
        res_label = "480p (SD)"
    else:
        res_label = f"{width}x{height}"

    return {
        "width": width,
        "height": height,
        "resolution": res_label,
        "duration_seconds": round(duration, 2),
        "codec": codec,
        "fps": fps
    }

def generate_video_thumbnail(video_path: Path, thumbnail_path: Path, seek_seconds: float = 1.0) -> bool:
    """
    Generates a high-clarity JPEG thumbnail from the video using ffmpeg.
    """
    thumbnail_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-ss", str(seek_seconds),
        "-i", str(video_path),
        "-vframes", "1",
        "-q:v", "2",
        str(thumbnail_path)
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return thumbnail_path.exists()
    except Exception:
        # Fallback to frame 0
        cmd[2] = "0.1"
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return thumbnail_path.exists()
        except Exception:
            return False

def ingest_sign_video(
    file: UploadFile,
    sign_record_id: int,
    title: str,
    signer_name: Optional[str],
    source_attribution: str,
    license_type: str,
    is_native_signer: bool,
    notes: Optional[str],
    db: Session
) -> SignVideo:
    """
    Securely ingests, validates, processes, and persists an authentic sign video asset.
    """
    # 1. Verify SignRecord exists
    sign_record = db.query(SignRecord).filter(SignRecord.id == sign_record_id).first()
    if not sign_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sign record with ID {sign_record_id} does not exist."
        )

    # 2. Validate file extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_VIDEO_EXTS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported video format '{ext}'. Allowed: {', '.join(ALLOWED_VIDEO_EXTS)}"
        )

    # 3. Create target directory
    videos_dir = settings.DATA_DIR / "sign_videos"
    thumbs_dir = videos_dir / "thumbnails"
    videos_dir.mkdir(parents=True, exist_ok=True)
    thumbs_dir.mkdir(parents=True, exist_ok=True)

    # 4. Generate clean sanitized filename
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    safe_slug = sign_record.concept.slug if sign_record.concept else f"sign_{sign_record_id}"
    filename = f"{safe_slug}_{timestamp}{ext}"
    target_video_path = videos_dir / filename

    # 5. Save video to disk with size check
    total_bytes = 0
    with open(target_video_path, "wb") as f_out:
        while True:
            chunk = file.file.read(1024 * 64)
            if not chunk:
                break
            total_bytes += len(chunk)
            if total_bytes > MAX_VIDEO_SIZE_BYTES:
                target_video_path.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"Video exceeds maximum allowed size of {MAX_VIDEO_SIZE_BYTES // (1024*1024)} MB."
                )
            f_out.write(chunk)

    if total_bytes == 0:
        target_video_path.unlink(missing_ok=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded video file is empty.")

    # 6. Extract exact technical metadata
    meta = extract_video_metadata(target_video_path)

    # 7. Generate thumbnail
    thumb_filename = f"{safe_slug}_{timestamp}_thumb.jpg"
    thumb_path = thumbs_dir / thumb_filename
    seek_time = min(1.0, meta["duration_seconds"] / 2.0)
    has_thumb = generate_video_thumbnail(target_video_path, thumb_path, seek_seconds=seek_time)

    # 8. Web-accessible relative URLs
    rel_video_url = f"/data/sign_videos/{filename}"
    rel_thumb_url = f"/data/sign_videos/thumbnails/{thumb_filename}" if has_thumb else None

    # 9. Create DB entity (Defaults to NEEDS_REVIEW as per policy)
    sign_video = SignVideo(
        sign_record_id=sign_record.id,
        title=title,
        video_path=rel_video_url,
        thumbnail_path=rel_thumb_url,
        signer_name=signer_name or "Verified Deaf Contributor",
        is_native_signer=is_native_signer,
        duration_seconds=meta["duration_seconds"],
        resolution=f"{meta['resolution']} ({meta['fps']} fps, {meta['codec']})",
        source_attribution=source_attribution,
        license=license_type,
        validation_status=ValidationStatus.NEEDS_REVIEW,
        notes=notes
    )

    db.add(sign_video)
    db.commit()
    db.refresh(sign_video)

    return sign_video

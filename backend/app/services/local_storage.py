import base64
import mimetypes
import uuid
from pathlib import Path

import httpx

from app.config import BASE_DIR


MEDIA_DIR = BASE_DIR / "media"
IMAGE_DIR = MEDIA_DIR / "images"
VIDEO_DIR = MEDIA_DIR / "videos"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)


def save_image(data: bytes, ext: str = "png") -> dict:
    ext = ext.lower().lstrip(".")
    if ext not in {"png", "jpg", "jpeg", "webp", "gif"}:
        ext = "png"
    name = f"{uuid.uuid4().hex}.{ext}"
    path = IMAGE_DIR / name
    path.write_bytes(data)
    return {"key": f"images/{name}", "url": f"/media/images/{name}", "size": len(data)}


def image_data_url(data: bytes, ext: str = "png") -> str:
    mime = mimetypes.types_map.get(f".{ext.lower().lstrip('.')}", "image/png")
    return f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"


def save_image_from_url(source_url: str) -> dict:
    with httpx.Client(timeout=120, trust_env=False) as client:
        response = client.get(source_url)
        response.raise_for_status()
    content_type = response.headers.get("content-type", "")
    ext = "jpg" if "jpeg" in content_type or source_url.lower().endswith((".jpg", ".jpeg")) else "webp" if "webp" in content_type else "png"
    return save_image(response.content, ext)


def save_video(data: bytes, ext: str = "mp4") -> dict:
    ext = ext.lower().lstrip(".")
    if ext not in {"mp4", "webm", "mov", "m4v"}:
        ext = "mp4"
    name = f"{uuid.uuid4().hex}.{ext}"
    path = VIDEO_DIR / name
    path.write_bytes(data)
    return {"key": f"videos/{name}", "url": f"/media/videos/{name}", "size": len(data)}


def save_video_from_url(source_url: str) -> dict:
    with httpx.Client(timeout=300, trust_env=False) as client:
        response = client.get(source_url)
        response.raise_for_status()
    content_type = response.headers.get("content-type", "")
    ext = "webm" if "webm" in content_type else "mp4"
    return save_video(response.content, ext)

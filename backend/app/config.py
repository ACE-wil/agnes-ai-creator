import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
load_dotenv(BASE_DIR / ".env")

DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "database" / "aimodel.db"))

TEXT_MODELS = ["agnes-2.0-flash", "agnes-1.5-flash"]
IMAGE_MODELS = ["agnes-image-2.0-flash", "agnes-image-2.1-flash"]
VIDEO_MODELS = ["agnes-video-v2.0"]

IMAGE_SIZES = ["1024x768", "1024x1024", "768x1024", "768x768", "1280x720", "720x1280"]


def validate_config():
    pass

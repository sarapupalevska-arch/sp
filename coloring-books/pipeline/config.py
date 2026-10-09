"""Settings shared by every pipeline stage."""
from dataclasses import dataclass

# KDP interior for an 8.5 x 11 in paperback, no bleed, 300 dpi.
DPI = 300
PAGE_W_IN, PAGE_H_IN = 8.5, 11.0
PAGE_W_PX, PAGE_H_PX = int(PAGE_W_IN * DPI), int(PAGE_H_IN * DPI)
MARGIN_PX = int(0.5 * DPI)  # keep art inside a 0.5 in safe margin

KDP_MIN_PAGES = 24


@dataclass
class BookSpec:
    theme: str = "friendly dinosaurs"
    age_range: str = "3-5"
    pages: int = 30
    style: str = (
        "simple children's coloring page, thick clean black outlines, "
        "large open shapes, no shading, no gray, no text, white background, "
        "one clear subject, cartoon style, original characters"
    )
    image_model: str = "gpt-image-1"
    text_model: str = "gpt-4o-mini"

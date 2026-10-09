"""Stage 2: generate one raw line-art image per idea."""
import base64
import io
import os
import random
import time
from pathlib import Path

from PIL import Image, ImageDraw

from .config import BookSpec


def _dry_run_image(idea: str, seed: int) -> Image.Image:
    """Placeholder line art so the rest of the pipeline can be tested offline."""
    rnd = random.Random(seed)
    img = Image.new("L", (1024, 1536), 255)
    d = ImageDraw.Draw(img)
    for _ in range(4):
        x, y = rnd.randint(150, 600), rnd.randint(200, 1000)
        w, h = rnd.randint(200, 400), rnd.randint(200, 400)
        d.ellipse([x, y, x + w, y + h], outline=0, width=14)
    return img


def generate_pages(spec: BookSpec, ideas: list[str], out_dir: Path,
                   dry_run: bool = False) -> list[Path]:
    raw_dir = out_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    client = None
    if not dry_run:
        from openai import OpenAI
        client = OpenAI()

    paths = []
    for i, idea in enumerate(ideas, 1):
        path = raw_dir / f"page_{i:02d}.png"
        if path.exists():  # resumable: skip pages already generated
            paths.append(path)
            continue
        if dry_run:
            _dry_run_image(idea, i).save(path)
        else:
            prompt = f"{idea}. {spec.style}"
            for attempt in range(3):
                try:
                    r = client.images.generate(
                        model=spec.image_model, prompt=prompt,
                        size="1024x1536", n=1,
                    )
                    data = base64.b64decode(r.data[0].b64_json)
                    Image.open(io.BytesIO(data)).save(path)
                    break
                except Exception as e:  # noqa: BLE001 - retry any API error
                    if attempt == 2:
                        raise
                    time.sleep(2 ** (attempt + 1))
        paths.append(path)
    return paths

"""Stage 3: turn raw images into print-ready pure black/white pages and
reject the ones KDP is likely to reject.

Checks per page:
  * gray    - too many mid-gray pixels (shading) before thresholding
  * empty   - almost no ink (blank/near-blank page)
  * dense   - too much ink (hard to color, usually a failed generation)
  * edge    - ink touching the source image border (subject is cut off)
  * dup     - near-duplicate of an earlier page
"""
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

from .config import MARGIN_PX, PAGE_H_PX, PAGE_W_PX

GRAY_MAX = 0.06     # fraction of pixels allowed to be mid-gray
INK_MIN = 0.008     # fraction of black pixels
INK_MAX = 0.30
DUP_CORRELATION = 0.93  # ink-layout correlation above this = near-duplicate


@dataclass
class PageResult:
    index: int
    raw: Path
    final: Path | None = None
    problems: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems


def _density_map(bw: np.ndarray, n: int = 24) -> np.ndarray:
    """Ink density on an n x n grid, zero-mean and unit-norm for correlation."""
    ink = (bw == 0).astype(np.float32)
    h, w = ink.shape
    ink = ink[: h // n * n, : w // n * n]
    grid = ink.reshape(n, ink.shape[0] // n, n, ink.shape[1] // n).mean(axis=(1, 3))
    grid = grid - grid.mean()
    norm = np.linalg.norm(grid)
    return grid / norm if norm else grid


def _fit_to_page(img: Image.Image) -> Image.Image:
    """Scale to fit inside the safe area, centered on a white page."""
    box_w, box_h = PAGE_W_PX - 2 * MARGIN_PX, PAGE_H_PX - 2 * MARGIN_PX
    img = ImageOps.contain(img.convert("L"), (box_w, box_h), Image.LANCZOS)
    page = Image.new("L", (PAGE_W_PX, PAGE_H_PX), 255)
    page.paste(img, ((PAGE_W_PX - img.width) // 2, (PAGE_H_PX - img.height) // 2))
    return page


def run_qa(raw_paths: list[Path], out_dir: Path) -> list[PageResult]:
    final_dir = out_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    results, hashes = [], []

    for i, raw in enumerate(raw_paths, 1):
        res = PageResult(i, raw)
        page = _fit_to_page(Image.open(raw))
        arr = np.asarray(page)

        mid_gray = np.mean((arr > 60) & (arr < 195))
        if mid_gray > GRAY_MAX:
            res.problems.append(f"gray shading ({mid_gray:.0%} mid-gray)")

        bw = (arr > 140).astype(np.uint8) * 255   # hard threshold
        ink = np.mean(bw == 0)
        if ink < INK_MIN:
            res.problems.append(f"almost empty ({ink:.1%} ink)")
        if ink > INK_MAX:
            res.problems.append(f"too dense ({ink:.0%} ink)")

        src = np.asarray(Image.open(raw).convert("L"))
        e = 6  # px strip along the source image border
        edge_ink = np.concatenate([src[:e].ravel(), src[-e:].ravel(),
                                   src[:, :e].ravel(), src[:, -e:].ravel()])
        if np.mean(edge_ink < 100) > 0.01:
            res.problems.append("drawing touches the edge (cut off)")

        dm = _density_map(bw)
        for j, other in enumerate(hashes, 1):
            if float(np.sum(dm * other)) >= DUP_CORRELATION:
                res.problems.append(f"near-duplicate of page {j}")
                break
        hashes.append(dm)

        final = final_dir / f"page_{i:02d}.png"
        Image.fromarray(bw).convert("1").save(final, dpi=(300, 300))
        res.final = final
        results.append(res)
    return results

"""Stage 4: review sheet, KDP interior PDF and listing text."""
from pathlib import Path

from PIL import Image, ImageDraw
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from .config import KDP_MIN_PAGES, PAGE_H_IN, PAGE_W_IN, BookSpec
from .qa import PageResult


def review_sheet(results: list[PageResult], out_dir: Path, cols: int = 6) -> Path:
    """One image with every page, rejected ones outlined in red."""
    thumb_w, thumb_h = 220, 285
    rows = (len(results) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb_w + 12) + 12,
                              rows * (thumb_h + 28) + 12), "white")
    d = ImageDraw.Draw(sheet)
    for n, r in enumerate(results):
        x = 12 + (n % cols) * (thumb_w + 12)
        y = 12 + (n // cols) * (thumb_h + 28)
        t = Image.open(r.final).convert("RGB").resize((thumb_w, thumb_h))
        sheet.paste(t, (x, y))
        d.rectangle([x, y, x + thumb_w, y + thumb_h],
                    outline="red" if not r.ok else "#999", width=3)
        d.text((x, y + thumb_h + 6),
               f"{r.index}" + ("" if r.ok else f"  REJECT: {'; '.join(r.problems)[:34]}"),
               fill="red" if not r.ok else "black")
    path = out_dir / "review_sheet.png"
    sheet.save(path)
    return path


def build_interior(spec: BookSpec, results: list[PageResult], out_dir: Path) -> Path:
    """Interior PDF: title page, then each approved page followed by a blank
    back so colors don't bleed through to the next picture."""
    good = [r for r in results if r.ok]
    path = out_dir / "interior.pdf"
    w, h = PAGE_W_IN * inch, PAGE_H_IN * inch
    c = canvas.Canvas(str(path), pagesize=(w, h))

    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(w / 2, h * 0.62, spec.theme.title())
    c.setFont("Helvetica", 24)
    c.drawCentredString(w / 2, h * 0.55, f"Coloring Book for Ages {spec.age_range}")
    c.showPage()
    c.showPage()  # blank back of title page

    for r in good:
        c.drawImage(str(r.final), 0, 0, width=w, height=h)
        c.showPage()
        c.showPage()  # blank back
    c.save()
    return path


def page_count(n_good: int) -> int:
    return 2 + 2 * n_good


def write_listing(spec: BookSpec, results: list[PageResult], out_dir: Path) -> Path:
    n_good = sum(r.ok for r in results)
    pages = page_count(n_good)
    theme = spec.theme.title()
    text = f"""KDP LISTING (copy into the KDP title setup)

Title:      {theme} Coloring Book for Kids Ages {spec.age_range}
Subtitle:   {n_good} Simple, Fun Pages to Color for Toddlers and Preschoolers
Author:     (your author / publisher name)
Language:   English
Format:     Paperback, 8.5 x 11 in, black & white interior, white paper, matte cover
Page count: {pages} (KDP minimum is {KDP_MIN_PAGES})

AI content:  Answer YES to "AI-generated images" in KDP title setup.

Description:
{n_good} original {spec.theme} coloring pages made for little hands. Thick,
clear outlines and big open shapes make coloring easy and fun for ages
{spec.age_range}. Every picture is printed on its own page, with a blank
page behind it so markers will not bleed through.

Great for rainy days, quiet time, car trips and gifts.

Keywords (7):
{spec.theme} coloring book
coloring book for toddlers
preschool coloring pages
kids activity book ages {spec.age_range}
easy coloring book for kids
animal coloring book for children
gift for toddlers

Categories: Children's Activity Books > Coloring Books; Juvenile Nonfiction > Dinosaurs
"""
    path = out_dir / "listing.txt"
    path.write_text(text)
    return path

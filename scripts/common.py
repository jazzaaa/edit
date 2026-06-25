import os
import json
from PIL import Image, ImageOps, ImageDraw, ImageFont
import pillow_avif

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_font(size):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def find_photo(index):
    exts = ["jpg", "jpeg", "png", "webp", "avif"]
    for ext in exts:
        path = f"photos/photo{index}.{ext}"
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"Missing photos/photo{index}.jpg, .png, .webp, or .avif")

def fit_image(path, size):
    img = Image.open(path).convert("RGB")
    return ImageOps.fit(img, size, method=Image.Resampling.LANCZOS)

def wrap_text(text, font, max_width, stroke_width=5):
    draw = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    lines = []
    for paragraph in text.split("\n"):
        if paragraph.strip() == "":
            lines.append("")
            continue
        words = paragraph.split()
        current = ""
        for word in words:
            test = word if not current else current + " " + word
            bbox = draw.textbbox((0, 0), test, font=font, stroke_width=stroke_width)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines

def draw_text(img, text, position, font_size, box_width, centered=False):
    draw = ImageDraw.Draw(img)
    font = get_font(font_size)
    stroke = 5
    lines = wrap_text(text, font, box_width, stroke_width=stroke)
    x, y = position
    line_gap = int(font_size * 0.35)

    for line in lines:
        if line == "":
            y += int(font_size * 0.75)
            continue
        if centered:
            bbox = draw.textbbox((0, 0), line, font=font, stroke_width=stroke)
            x_draw = (img.width - (bbox[2] - bbox[0])) // 2
        else:
            x_draw = x
        draw.text((x_draw, y), line, font=font, fill="white",
                  stroke_width=stroke, stroke_fill="black")
        bbox = draw.textbbox((x_draw, y), line, font=font, stroke_width=stroke)
        y += (bbox[3] - bbox[1]) + line_gap
    return img

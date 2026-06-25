from PIL import Image, ImageDraw
from common import load_json, find_photo, fit_image, draw_text

settings = load_json("settings.json")
texts = load_json("texts.json")

W = settings["width"]
H = settings["height"]
PANEL_H = H // 4
OUTPUT = "LGP_Poster_Output.png"

if len(texts) != 4:
    raise ValueError("texts.json must contain exactly 4 text items.")

poster = Image.new("RGB", (W, H), "white")
draw = ImageDraw.Draw(poster)

poster_positions = [(55, 90), (55, 90), (55, 90), (0, 230)]
poster_font_sizes = [62, 62, 62, 54]
poster_box_widths = [850, 850, 850, 880]

for i in range(4):
    photo_path = find_photo(i + 1)
    print(f"Rendering poster panel {i+1}: {photo_path}")
    panel = fit_image(photo_path, (W, PANEL_H))
    y_offset = i * PANEL_H
    poster.paste(panel, (0, y_offset))

    if i > 0:
        draw.rectangle((0, y_offset - 6, W, y_offset + 6), fill="white")

    x, y = poster_positions[i]
    draw_text(
        poster,
        texts[i],
        (x, y_offset + y),
        poster_font_sizes[i],
        poster_box_widths[i],
        centered=(i == 3),
    )

poster.save(OUTPUT, quality=95)
print(f"Saved {OUTPUT}")

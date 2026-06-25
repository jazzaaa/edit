import numpy as np
import imageio.v2 as imageio
from common import load_json, find_photo, fit_image, draw_text

settings = load_json("settings.json")
texts = load_json("texts.json")

W = settings["width"]
H = settings["height"]
FPS = settings["fps"]
SECONDS = settings["seconds_per_photo"]
ZOOM = settings["zoom_amount"]
OUTPUT = "LGP_Reel_Output.mp4"

if len(texts) != 4:
    raise ValueError("texts.json must contain exactly 4 text items.")

def ken_burns(base_img, progress):
    zoom = 1 + ZOOM * progress
    new_w = int(W * zoom)
    new_h = int(H * zoom)
    zoomed = base_img.resize((new_w, new_h))
    left = (new_w - W) // 2
    top = (new_h - H) // 2
    return zoomed.crop((left, top, left + W, top + H))

frames_per_photo = int(SECONDS * FPS)

writer = imageio.get_writer(
    OUTPUT,
    fps=FPS,
    codec="libx264",
    macro_block_size=None,
    ffmpeg_params=["-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20"],
)

try:
    for i in range(4):
        photo_path = find_photo(i + 1)
        print(f"Rendering video slide {i+1}: {photo_path}")
        base = fit_image(photo_path, (W, H))
        pos = tuple(settings["text_positions"][i])
        font_size = settings["font_sizes"][i]
        box_width = settings["text_box_widths"][i]
        centered = True if i == 3 else False

        for frame_index in range(frames_per_photo):
            progress = frame_index / max(1, frames_per_photo - 1)
            frame = ken_burns(base, progress)
            frame = draw_text(frame, texts[i], pos, font_size, box_width, centered=centered)
            writer.append_data(np.array(frame))
finally:
    writer.close()

print(f"Saved {OUTPUT}")

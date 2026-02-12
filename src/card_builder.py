"""
Individual card builder for print-ready vehicle cards.
Generates 5cm × 7cm cards at 300 DPI (590 × 830 pixels).
"""

import logging
from pathlib import Path

from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

from .models import Vehicle

logger = logging.getLogger(__name__)

# Card dimensions for 5cm × 7cm at 300 DPI
CARD_WIDTH = 590
CARD_HEIGHT = 830
DPI = 300

# Layout
PADDING = 20
TEXT_AREA_TOP = 60
TEXT_AREA_BOTTOM = 60


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Get a font that supports Hebrew and Russian characters."""
    font_paths = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/tahoma.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]

    if bold:
        font_paths = [
            p.replace(".ttf", "bd.ttf") if "bd" not in p else p for p in font_paths
        ]

    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except (IOError, OSError):
            continue

    return ImageFont.load_default()


def load_vehicle_image(
    vehicle: Vehicle,
    images_dir: Path,
    target_width: int,
    target_height: int,
) -> Image.Image:
    """Load and resize vehicle image to fit target dimensions."""
    image_path = images_dir / vehicle.image_filename

    if image_path.exists():
        try:
            img = Image.open(image_path)
            img = img.convert("RGBA")

            # Scale to fit within target area (use 95% for padding)
            target_size = int(min(target_width, target_height) * 0.95)
            img_ratio = img.width / img.height

            if img_ratio > 1:  # wider than tall
                new_width = target_size
                new_height = int(target_size / img_ratio)
            else:  # taller than wide
                new_height = target_size
                new_width = int(target_size * img_ratio)

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Create transparent canvas and center the image
            canvas = Image.new("RGBA", (target_width, target_height), (255, 255, 255, 0))
            x = (target_width - new_width) // 2
            y = (target_height - new_height) // 2
            canvas.paste(img, (x, y), img if img.mode == "RGBA" else None)

            return canvas
        except Exception as e:
            logger.warning(f"Error loading {image_path}: {e}")

    # Return empty canvas if image not found
    logger.warning(f"Image not found: {image_path}")
    return Image.new("RGBA", (target_width, target_height), (255, 255, 255, 0))


def create_vehicle_card(
    vehicle: Vehicle,
    images_dir: Path,
) -> Image.Image:
    """
    Create a single print-ready vehicle card.

    Args:
        vehicle: Vehicle object.
        images_dir: Directory containing vehicle images.

    Returns:
        PIL Image object (590 × 830 pixels, 300 DPI).
    """
    # Create card with white background
    card = Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), "white")
    draw = ImageDraw.Draw(card)

    # Add rounded rectangle border with vehicle color
    draw.rounded_rectangle(
        [(8, 8), (CARD_WIDTH - 8, CARD_HEIGHT - 8)],
        radius=20,
        outline=vehicle.color,
        width=4,
    )

    # Load vehicle image
    image_area_height = CARD_HEIGHT - TEXT_AREA_TOP - TEXT_AREA_BOTTOM - PADDING * 2
    image_area_width = CARD_WIDTH - PADDING * 2
    vehicle_img = load_vehicle_image(vehicle, images_dir, image_area_width, image_area_height)

    # Paste vehicle image
    img_x = PADDING
    img_y = TEXT_AREA_TOP + PADDING
    card.paste(vehicle_img, (img_x, img_y), vehicle_img if vehicle_img.mode == "RGBA" else None)

    # Get fonts
    hebrew_font = get_font(32, bold=True)
    russian_font = get_font(26)

    # Draw Hebrew text (top)
    hebrew_rtl = get_display(vehicle.hebrew)
    hebrew_bbox = draw.textbbox((0, 0), hebrew_rtl, font=hebrew_font)
    hebrew_width = hebrew_bbox[2] - hebrew_bbox[0]
    hebrew_x = (CARD_WIDTH - hebrew_width) // 2
    draw.text((hebrew_x, 20), hebrew_rtl, fill="#333333", font=hebrew_font)

    # Draw Russian text (bottom)
    russian_bbox = draw.textbbox((0, 0), vehicle.russian, font=russian_font)
    russian_width = russian_bbox[2] - russian_bbox[0]
    russian_x = (CARD_WIDTH - russian_width) // 2
    draw.text((russian_x, CARD_HEIGHT - 50), vehicle.russian, fill="#555555", font=russian_font)

    return card


def create_all_cards(
    vehicles: list[Vehicle],
    images_dir: Path,
    output_dir: Path,
) -> list[Path]:
    """
    Create individual print-ready cards for all vehicles.

    Args:
        vehicles: List of Vehicle objects.
        images_dir: Directory containing vehicle images.
        output_dir: Directory to save card images.

    Returns:
        List of paths to created card images.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    created_files = []

    for vehicle in vehicles:
        card = create_vehicle_card(vehicle, images_dir)

        # Save with 300 DPI metadata
        output_path = output_dir / f"card_{vehicle.id}.png"
        card.save(output_path, "PNG", dpi=(DPI, DPI))

        logger.info(f"Created card: {output_path}")
        created_files.append(output_path)

    logger.info(f"Created {len(created_files)} cards in {output_dir}")
    return created_files

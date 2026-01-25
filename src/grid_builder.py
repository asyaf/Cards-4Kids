"""
Grid image builder for creating multilingual vehicle cards.
"""

import logging
from pathlib import Path

from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

from .models import Vehicle

logger = logging.getLogger(__name__)


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """
    Get a font that supports Hebrew and Russian characters.

    Args:
        size: Font size in points.
        bold: Whether to use bold variant.

    Returns:
        ImageFont object.
    """
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


def create_placeholder_image(
    color: str, width: int, height: int, text: str = ""
) -> Image.Image:
    """
    Create a colored placeholder image with optional text.

    Args:
        color: Background color (hex).
        width: Image width.
        height: Image height.
        text: Optional text to display.

    Returns:
        PIL Image object.
    """
    img = Image.new("RGBA", (width, height), color)
    draw = ImageDraw.Draw(img)

    if text:
        font = get_font(24)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        draw.text((x, y), text, fill="white", font=font)

    return img


def load_vehicle_image(
    vehicle: Vehicle,
    images_dir: Path,
    canvas_width: int,
    canvas_height: int,
) -> Image.Image:
    """
    Load a vehicle image from file or create placeholder.

    Args:
        vehicle: Vehicle object.
        images_dir: Directory containing vehicle images.
        canvas_width: Target canvas width.
        canvas_height: Target canvas height.

    Returns:
        PIL Image object (centered on transparent canvas).
    """
    image_path = images_dir / vehicle.image_filename

    if image_path.exists():
        try:
            img = Image.open(image_path)
            img = img.convert("RGBA")

            # Scale to fit within canvas (use 95% for padding)
            target_size = int(min(canvas_width, canvas_height) * 0.95)
            img_ratio = img.width / img.height

            if img_ratio > 1:  # wider than tall
                new_width = target_size
                new_height = int(target_size / img_ratio)
            else:  # taller than wide
                new_height = target_size
                new_width = int(target_size * img_ratio)

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Create transparent canvas and center the image
            canvas = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))
            x = (canvas_width - new_width) // 2
            y = (canvas_height - new_height) // 2
            canvas.paste(img, (x, y), img if img.mode == "RGBA" else None)

            return canvas
        except Exception as e:
            logger.warning(f"Error loading {image_path}: {e}")

    # Create placeholder with vehicle color
    logger.info(f"Using placeholder for {vehicle.id}")
    return create_placeholder_image(vehicle.color, canvas_width, canvas_height, vehicle.english)


def create_vehicle_cell(
    vehicle: Vehicle,
    images_dir: Path,
    cell_width: int,
    cell_height: int,
    padding: int,
    text_area_height: int,
) -> Image.Image:
    """
    Create a single cell with vehicle image and labels.

    Args:
        vehicle: Vehicle object.
        images_dir: Directory containing vehicle images.
        cell_width: Cell width in pixels.
        cell_height: Cell height in pixels.
        padding: Padding around content.
        text_area_height: Height reserved for text.

    Returns:
        PIL Image object.
    """
    cell = Image.new("RGBA", (cell_width, cell_height), "white")
    draw = ImageDraw.Draw(cell)

    # Add rounded rectangle border with vehicle color
    draw.rounded_rectangle(
        [(5, 5), (cell_width - 5, cell_height - 5)],
        radius=15,
        outline=vehicle.color,
        width=3,
    )

    # Load or create vehicle image
    canvas_width = cell_width - 2 * padding
    canvas_height = cell_height - 2 * text_area_height - 2 * padding
    vehicle_img = load_vehicle_image(vehicle, images_dir, canvas_width, canvas_height)

    # Center the vehicle image
    img_x = (cell_width - vehicle_img.width) // 2
    img_y = text_area_height + (cell_height - 2 * text_area_height - vehicle_img.height) // 2
    cell.paste(vehicle_img, (img_x, img_y), vehicle_img if vehicle_img.mode == "RGBA" else None)

    # Get fonts
    hebrew_font = get_font(28, bold=True)
    russian_font = get_font(24)

    # Draw Hebrew text (above image) - Right to Left
    hebrew_rtl = get_display(vehicle.hebrew)
    hebrew_bbox = draw.textbbox((0, 0), hebrew_rtl, font=hebrew_font)
    hebrew_width = hebrew_bbox[2] - hebrew_bbox[0]
    hebrew_x = (cell_width - hebrew_width) // 2
    draw.text((hebrew_x, 25), hebrew_rtl, fill="#333333", font=hebrew_font)

    # Draw Russian text (below image)
    russian_bbox = draw.textbbox((0, 0), vehicle.russian, font=russian_font)
    russian_width = russian_bbox[2] - russian_bbox[0]
    russian_x = (cell_width - russian_width) // 2
    draw.text((russian_x, cell_height - 50), vehicle.russian, fill="#555555", font=russian_font)

    return cell


def create_grid_image(
    vehicles: list[Vehicle],
    images_dir: Path,
    output_path: Path,
    cols: int = 3,
    cell_width: int = 400,
    cell_height: int = 450,
    padding: int = 20,
    text_area_height: int = 80,
    background_color: str = "#F0F8FF",
    title_hebrew: str = "רכבי עבודה",
    title_russian: str = "Рабочие машины",
) -> Path:
    """
    Create the full grid image with all vehicles.

    Args:
        vehicles: List of Vehicle objects.
        images_dir: Directory containing vehicle images.
        output_path: Path to save the grid image.
        cols: Number of columns.
        cell_width: Width of each cell.
        cell_height: Height of each cell.
        padding: Padding between cells.
        text_area_height: Height for text in each cell.
        background_color: Background color (hex).
        title_hebrew: Hebrew title text.
        title_russian: Russian title text.

    Returns:
        Path to the saved grid image.
    """
    rows = (len(vehicles) + cols - 1) // cols

    # Calculate total dimensions
    total_width = cols * cell_width + (cols + 1) * padding
    total_height = rows * cell_height + (rows + 1) * padding + 80  # Extra for title

    # Create main image
    main_image = Image.new("RGBA", (total_width, total_height), background_color)
    draw = ImageDraw.Draw(main_image)

    # Add title
    title_font = get_font(36, bold=True)
    title = get_display(title_hebrew) + " / " + title_russian
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (total_width - title_width) // 2
    draw.text((title_x, 20), title, fill="#333333", font=title_font)

    # Create and place each cell
    for i, vehicle in enumerate(vehicles):
        row = i // cols
        col = i % cols

        cell = create_vehicle_cell(
            vehicle=vehicle,
            images_dir=images_dir,
            cell_width=cell_width,
            cell_height=cell_height,
            padding=padding,
            text_area_height=text_area_height,
        )

        x = padding + col * (cell_width + padding)
        y = 80 + padding + row * (cell_height + padding)

        main_image.paste(cell, (x, y))

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the image
    main_image.save(output_path, "PNG")
    logger.info(f"Grid image saved to: {output_path}")

    return output_path

"""
Gemini image generation for vehicle images.
"""

import io
import logging
import time
from dataclasses import dataclass
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

from .models import Vehicle

logger = logging.getLogger(__name__)


@dataclass
class GenerationResult:
    """Result of an image generation attempt."""

    vehicle_id: str
    success: bool
    output_path: Path | None = None
    error_message: str | None = None


def generate_vehicle_image(
    client: genai.Client,
    vehicle: Vehicle,
    output_dir: Path,
    style_prompt: str,
    model: str = "gemini-2.0-flash-exp",
) -> GenerationResult:
    """
    Generate a single vehicle image using Gemini.

    Args:
        client: Configured Gemini client.
        vehicle: Vehicle to generate image for.
        output_dir: Directory to save the image.
        style_prompt: The style prompt template (must contain {vehicle}).
        model: Gemini model to use.

    Returns:
        GenerationResult with success status and path or error.
    """
    output_path = output_dir / vehicle.image_filename
    # Use description if provided, otherwise use display name
    vehicle_desc = vehicle.description if vehicle.description else vehicle.display_name
    prompt = style_prompt.format(vehicle=vehicle_desc)

    logger.info(f"Generating image for {vehicle.display_name}...")

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["image", "text"],
            ),
        )

        # Extract image from response
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                image = Image.open(io.BytesIO(image_data))
                image.save(output_path, "PNG")
                logger.info(f"Saved: {output_path}")
                return GenerationResult(
                    vehicle_id=vehicle.id,
                    success=True,
                    output_path=output_path,
                )

        logger.warning(f"No image in response for {vehicle.id}")
        return GenerationResult(
            vehicle_id=vehicle.id,
            success=False,
            error_message="No image in response",
        )

    except Exception as e:
        logger.error(f"Error generating {vehicle.id}: {e}")
        return GenerationResult(
            vehicle_id=vehicle.id,
            success=False,
            error_message=str(e),
        )


def generate_all_vehicles(
    vehicles: list[Vehicle],
    output_dir: Path,
    api_key: str,
    style_prompt: str,
    model: str = "gemini-2.0-flash-exp",
    delay: float = 2.0,
    vehicle_ids: list[str] | None = None,
) -> dict[str, GenerationResult]:
    """
    Generate images for multiple vehicles.

    Args:
        vehicles: List of vehicles to generate.
        output_dir: Directory to save images.
        api_key: Gemini API key.
        style_prompt: Style prompt template.
        model: Gemini model to use.
        delay: Delay between generations (seconds).
        vehicle_ids: Optional list of specific vehicle IDs to generate.
                     If None, generates all vehicles.

    Returns:
        Dictionary mapping vehicle_id to GenerationResult.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=api_key)
    results = {}

    # Filter vehicles if specific IDs requested
    if vehicle_ids:
        vehicles = [v for v in vehicles if v.id in vehicle_ids]

    for i, vehicle in enumerate(vehicles):
        # Backup existing image
        output_path = output_dir / vehicle.image_filename
        backup_path = output_dir / f"{vehicle.id}_backup.png"

        if output_path.exists() and not backup_path.exists():
            output_path.rename(backup_path)
            logger.info(f"Backed up existing {vehicle.image_filename}")

        result = generate_vehicle_image(
            client=client,
            vehicle=vehicle,
            output_dir=output_dir,
            style_prompt=style_prompt,
            model=model,
        )
        results[vehicle.id] = result

        # Restore backup if generation failed
        if not result.success and backup_path.exists() and not output_path.exists():
            backup_path.rename(output_path)
            logger.info(f"Restored backup for {vehicle.id}")

        # Delay between generations (except for last one)
        if i < len(vehicles) - 1:
            time.sleep(delay)

    return results

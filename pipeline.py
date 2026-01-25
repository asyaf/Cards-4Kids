#!/usr/bin/env python3
"""
Vehicle Card Pipeline - Main Entry Point

Usage:
    python pipeline.py              # Run full pipeline (generate + grid)
    python pipeline.py generate     # Generate images only
    python pipeline.py grid         # Create grid only
    python pipeline.py generate --vehicle bulldozer  # Regenerate specific vehicle
"""

import argparse
import logging
import sys

import config
from src import load_vehicles, generate_all_vehicles, create_grid_image

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def run_generate(vehicles, vehicle_ids: list[str] | None = None) -> bool:
    """
    Generate vehicle images using Gemini.

    Args:
        vehicles: List of Vehicle objects.
        vehicle_ids: Optional list of specific vehicle IDs to generate.

    Returns:
        True if all successful, False if any failed.
    """
    if not config.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY environment variable not set")
        logger.info("Set it with: export GEMINI_API_KEY='your-key'")
        return False

    logger.info("=" * 60)
    logger.info("Generating Vehicle Images")
    logger.info("=" * 60)

    results = generate_all_vehicles(
        vehicles=vehicles,
        output_dir=config.IMAGES_DIR,
        api_key=config.GEMINI_API_KEY,
        style_prompt=config.IMAGE_STYLE_PROMPT,
        model=config.GEMINI_MODEL,
        delay=config.GENERATION_DELAY,
        vehicle_ids=vehicle_ids,
    )

    # Summary
    success = [r for r in results.values() if r.success]
    failed = [r for r in results.values() if not r.success]

    logger.info("")
    logger.info("=" * 60)
    logger.info("GENERATION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Successful: {len(success)}")
    for r in success:
        logger.info(f"  - {r.vehicle_id}.png")

    if failed:
        logger.warning(f"Failed: {len(failed)}")
        for r in failed:
            logger.warning(f"  - {r.vehicle_id}: {r.error_message}")

    return len(failed) == 0


def run_grid(vehicles) -> bool:
    """
    Create the grid image from existing vehicle images.

    Args:
        vehicles: List of Vehicle objects.

    Returns:
        True if successful.
    """
    logger.info("=" * 60)
    logger.info("Creating Vehicle Grid")
    logger.info("=" * 60)

    output_path = config.OUTPUT_DIR / config.OUTPUT_FILENAME

    # Check for existing images
    logger.info(f"Looking for images in: {config.IMAGES_DIR}")
    for vehicle in vehicles:
        img_path = config.IMAGES_DIR / vehicle.image_filename
        if img_path.exists():
            logger.info(f"  Found: {vehicle.image_filename}")
        else:
            logger.warning(f"  Missing: {vehicle.image_filename} (will use placeholder)")

    create_grid_image(
        vehicles=vehicles,
        images_dir=config.IMAGES_DIR,
        output_path=output_path,
        cols=config.GRID_COLS,
        cell_width=config.CELL_WIDTH,
        cell_height=config.CELL_HEIGHT,
        padding=config.PADDING,
        text_area_height=config.TEXT_AREA_HEIGHT,
        background_color=config.BACKGROUND_COLOR,
        title_hebrew=config.GRID_TITLE_HEBREW,
        title_russian=config.GRID_TITLE_RUSSIAN,
    )

    logger.info(f"Grid saved to: {output_path}")
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Vehicle Card Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["generate", "grid", "all"],
        default="all",
        help="Command to run (default: all)",
    )
    parser.add_argument(
        "--vehicle",
        "-v",
        action="append",
        dest="vehicles",
        help="Specific vehicle ID to generate (can be used multiple times)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load vehicles from config file
    try:
        vehicles = load_vehicles(config.VEHICLES_FILE)
    except FileNotFoundError:
        logger.error(f"Vehicles file not found: {config.VEHICLES_FILE}")
        return 1
    except ValueError as e:
        logger.error(f"Error parsing vehicles file: {e}")
        return 1

    logger.info(f"Loaded {len(vehicles)} vehicles from {config.VEHICLES_FILE}")

    # Validate requested vehicle IDs
    if args.vehicles:
        valid_ids = {v.id for v in vehicles}
        for vid in args.vehicles:
            if vid not in valid_ids:
                logger.error(f"Unknown vehicle ID: {vid}")
                logger.info(f"Valid IDs: {', '.join(sorted(valid_ids))}")
                return 1

    # Execute commands
    success = True

    if args.command in ("generate", "all"):
        if not run_generate(vehicles, args.vehicles):
            success = False
            if args.command == "generate":
                return 1

    if args.command in ("grid", "all"):
        if not run_grid(vehicles):
            success = False

    if success:
        logger.info("")
        logger.info("Pipeline completed successfully!")
    else:
        logger.warning("")
        logger.warning("Pipeline completed with some failures")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

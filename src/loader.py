"""
Load vehicle definitions from the vehicles.txt file.
"""

import logging
from pathlib import Path

from .models import Vehicle

logger = logging.getLogger(__name__)


def load_vehicles(file_path: Path) -> list[Vehicle]:
    """
    Load vehicle definitions from a pipe-separated text file.

    File format:
        # Comments start with #
        id | English | Hebrew | Russian | color

    Args:
        file_path: Path to the vehicles.txt file.

    Returns:
        List of validated Vehicle objects.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If a line has invalid format.
    """
    vehicles = []

    try:
        with open(file_path, encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                parts = [p.strip() for p in line.split("|")]

                if len(parts) < 5 or len(parts) > 6:
                    raise ValueError(
                        f"Line {line_num}: Expected 5-6 pipe-separated values, "
                        f"got {len(parts)}: {line}"
                    )

                vehicle_id, english, hebrew, russian, color = parts[:5]
                description = parts[5] if len(parts) == 6 else ""

                vehicle = Vehicle(
                    id=vehicle_id,
                    english=english,
                    hebrew=hebrew,
                    russian=russian,
                    color=color,
                    description=description,
                )
                vehicles.append(vehicle)
                logger.debug(f"Loaded vehicle: {vehicle.id}")

    except FileNotFoundError:
        logger.error(f"Vehicle file not found: {file_path}")
        raise

    logger.info(f"Loaded {len(vehicles)} vehicles from {file_path}")
    return vehicles


def get_vehicle_by_id(vehicles: list[Vehicle], vehicle_id: str) -> Vehicle | None:
    """
    Find a vehicle by its ID.

    Args:
        vehicles: List of vehicles to search.
        vehicle_id: The ID to find.

    Returns:
        The Vehicle if found, None otherwise.
    """
    for vehicle in vehicles:
        if vehicle.id == vehicle_id:
            return vehicle
    return None

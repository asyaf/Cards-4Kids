"""
Configuration settings for the Vehicle Card Pipeline.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
VEHICLES_FILE = PROJECT_ROOT / "vehicles.txt"
IMAGES_DIR = PROJECT_ROOT / "images"
OUTPUT_DIR = PROJECT_ROOT / "output"

# API Configuration - load from environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini model configuration
GEMINI_MODEL = "gemini-2.0-flash-exp"

# Image Generation Style Prompt
IMAGE_STYLE_PROMPT = """Generate an image of a cute cartoon {vehicle} for a children's book.

EXACT STYLE REQUIREMENTS (follow precisely):
- Kawaii/chibi style with a friendly smiling face on the front of the vehicle
- Big cute eyes with highlights, happy smile
- Chunky, rounded, simplified shapes - no sharp edges
- Flat color shading with minimal gradients
- Bright saturated primary colors (yellow, red, blue, green, orange)
- Pure white background, no shadows or ground
- Vehicle facing 3/4 view toward the viewer
- Cartoonish proportions - slightly oversized wheels and cab
- No text, labels, watermarks, or human characters
- Single vehicle only, centered in frame
- Style similar to: Tayo the Little Bus, Bob the Builder vehicles"""

# Grid Layout Configuration
GRID_COLS = 3
GRID_ROWS = 3
CELL_WIDTH = 400
CELL_HEIGHT = 450
PADDING = 20
TEXT_AREA_HEIGHT = 80
BACKGROUND_COLOR = "#F0F8FF"  # Alice Blue

# Grid title
GRID_TITLE_HEBREW = "רכבי עבודה"
GRID_TITLE_RUSSIAN = "Рабочие машины"

# Output filename
OUTPUT_FILENAME = "construction_vehicles_kids.png"

# Generation delay (seconds) to avoid rate limiting
GENERATION_DELAY = 2

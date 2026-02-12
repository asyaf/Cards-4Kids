# Image-4kids Project Status

## Project Overview
Creating a 6x3 grid (18 vehicles) of construction/work vehicles with Hebrew and Russian labels for children's educational material.

## Major Refactoring Completed

### New Architecture
The codebase was refactored to separate data from code:

| File/Folder | Purpose |
|-------------|---------|
| `vehicles.txt` | Single source of truth for all vehicle definitions |
| `config.py` | All configuration settings (API key, prompts, grid layout) |
| `pipeline.py` | Main entry point - runs generate and/or grid commands |
| `src/models.py` | Pydantic Vehicle model with validation |
| `src/loader.py` | Parses vehicles.txt into Vehicle objects |
| `src/generator.py` | Gemini image generation |
| `src/grid_builder.py` | Grid creation with multilingual labels |
| `images/` | Generated vehicle images |
| `images_final/` | Backup of final 18 images used in grid |
| `output/` | Final grid output |

### Old Files Deleted
- `generate_with_gemini.py` (replaced by `src/generator.py`)
- `create_vehicles_grid.py` (replaced by `src/grid_builder.py`)
- `download_vehicle_images.py` (no longer needed)

## Vehicle List (18 vehicles in 7 categories)

### Construction Vehicles
| ID | English | Hebrew | Russian |
|----|---------|--------|---------|
| excavator | Excavator | מחפר | Экскаватор |
| bulldozer | Bulldozer | דחפור | Бульдозер |
| forklift | Forklift | מלגזה | Вилочный погрузчик |
| shovel_loader | Shovel Loader | שופל | Фронтальный погрузчик |
| dump_truck | Dump Truck | משאית עפר | Самосвал |

### Cranes
| ID | English | Hebrew | Russian |
|----|---------|--------|---------|
| truck_crane | Truck Crane | משאית מנוף | Кран-машина |
| backhoe_loader | Backhoe Loader | מחפרון | Экскаватор-погрузчик |

### Road and Concrete
| ID | English | Hebrew | Russian |
|----|---------|--------|---------|
| road_roller | Road Roller | מכבש | Каток |
| cement_mixer | Cement Mixer | מערבל בטון | Бетономешалка |
| concrete_pump | Concrete Pump | משאבת בטון | Бетононасос |

### Emergency Vehicles
| ID | English | Hebrew | Russian |
|----|---------|--------|---------|
| fire_truck | Fire Truck | כבאית | Пожарная машина |
| police_car | Police Car | ניידת משטרה | Полицейская машина |
| ambulance | Ambulance | אמבולנס | Скорая помощь |

### Transport Vehicles
| ID | English | Hebrew | Russian |
|----|---------|--------|---------|
| truck | Truck | משאית | Грузовик |
| bus | Bus | אוטובוס | Автобус |

### Utility Vehicles
| ID | English | Hebrew | Russian |
|----|---------|--------|---------|
| garbage_truck | Garbage Truck | משאית זבל | Мусорная машина |
| snow_plow | Snow Plow | מפלסת שלג | Снегоуборочная машина |

### Farm Vehicles
| ID | English | Hebrew | Russian |
|----|---------|--------|---------|
| tractor | Tractor | טרקטור | Трактор |

## Issues Encountered and Resolved

### 1. Tower Crane Removed
**Problem**: Tower crane (עגורן) is not a vehicle - it's stationary construction equipment.
**Solution**: Removed tower_crane and replaced with backhoe_loader (מחפרון).

### 2. Israeli-Style Ambulance
**Problem**: Default ambulance images were American-style (red/orange).
**Solution**: Added description field to vehicles.txt format. Ambulance description: "White ambulance van like Israeli Magen David Adom"

### 3. Concrete Pump vs Cement Mixer Confusion
**Problem**: Gemini kept generating cement mixer images instead of concrete pump with boom arm.
**Solution**: Added detailed description: "Truck with Z-shaped folding boom arm made of 3-4 straight sections connected at angles, with outriggers extended for stability, no rotating drum"
Also mirrored the final image to face left.

### 4. Bus Style
**Problem**: Default bus images were yellow school buses.
**Solution**: Added description: "Green city public transit bus with large windows, not a yellow school bus"

### 5. Fire Truck Color
**Problem**: Fire truck face wasn't red.
**Solution**: Added description: "Fire truck with red front face, red cabin, red body". First attempt created a fire truck with red wheels.

### 6. Description Field Added
To solve image generation issues, a 6th optional field was added to vehicles.txt format:
```
id | English | Hebrew | Russian | color | description (optional)
```
The description is sent to Gemini for more precise image generation.

## Pipeline Usage

```bash
# Set API key (PowerShell)
$env:GEMINI_API_KEY="AIzaSyBiZGQGAKOKHmXdkjIhT4oakPaxo7lmT6w"

# Generate all images and create grid
python pipeline.py

# Generate images only
python pipeline.py generate

# Create grid only
python pipeline.py grid

# Regenerate specific vehicle
python pipeline.py generate --vehicle concrete_pump
```

## Output
- Final grid: `output/construction_vehicles_kids.png` (6x3 grid, 18 vehicles)
- Final images backup: `images_final/` (18 PNG files)

## API Key
Gemini API key loaded from environment variable `GEMINI_API_KEY`

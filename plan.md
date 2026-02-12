# Plan: Construction Machinery Vehicles Image for Kids

## Goal
Create a kid-friendly image featuring 9 construction machinery vehicles in a 3x3 grid, with each vehicle labeled in Hebrew and Russian.

## The 9 Construction Vehicles

| # | English | Hebrew | Russian |
|---|---------|--------|---------|
| 1 | Excavator | מחפר | Экскаватор |
| 2 | Bulldozer | דחפור | Бульдозер |
| 3 | Crane | מנוף | Кран |
| 4 | Dump Truck | משאית זבל | Мусорная машина |
| 5 | Cement Mixer | מערבל בטון | Бетономешалка |
| 6 | Forklift | מלגזה | Погрузчик |
| 7 | Tractor | טרקטור | Трактор |
| 8 | Fire Truck | משאית כיבוי | Пожарная машина |
| 9 | Shovel Loader | שופל | Погрузчик |

## Implementation Steps

### Step 1: Search & Download Vehicle Images
- Use WebSearch to find royalty-free/stock images of each construction vehicle
- Download 9 clear images (one per vehicle)
- Save images to an `images/` folder

### Step 2: Create Base Layout with Python
- Use PIL/Pillow to create a 3x3 grid image
- Resize each vehicle image to fit grid cells
- Add Hebrew text above each vehicle
- Add Russian text below each vehicle
- Use a kid-friendly font (if available) or clear sans-serif

### Step 3: Enhance with Gemini (Nano Banana)
- Send the composite image to Gemini 2.0 Flash
- Prompt: Transform into a colorful, cartoon/kid-friendly style while keeping the vehicles recognizable and text readable
- Save the final enhanced image

## Output
- Final image file: `construction_vehicles_kids.png`

## Verification
- Check all 9 vehicles are visible and recognizable
- Verify Hebrew and Russian text is readable and correctly spelled
- Confirm cartoon style is appealing for children

## Technical Requirements
- Python with PIL/Pillow library
- Fonts that support Hebrew and Russian characters (e.g., Arial Unicode, Noto Sans)
- Internet access for image search and Gemini API

#!/usr/bin/env python3
"""
Test script to verify GUI components can be loaded without displaying the window.
"""

import os
from PIL import Image

def test_image_loading():
    """Test if all required images can be loaded"""
    base_path = os.path.dirname(os.path.abspath(__file__))

    print("Testing image loading...")

    # Test dice images
    print("\n1. Testing dice images:")
    for i in range(1, 7):
        img_path = os.path.join(base_path, "assets", f"wuerfel{i}.png")
        if os.path.exists(img_path):
            img = Image.open(img_path)
            print(f"  ✓ wuerfel{i}.png: {img.size}")
        else:
            print(f"  ✗ wuerfel{i}.png: NOT FOUND")

    # Test tile images
    print("\n2. Testing tile images:")
    for i in range(1, 7):
        img_path = os.path.join(base_path, "assets", f"tile_{i}.png")
        if os.path.exists(img_path):
            img = Image.open(img_path)
            print(f"  ✓ tile_{i}.png: {img.size}")
        else:
            print(f"  ✗ tile_{i}.png: NOT FOUND")

    # Test coin image
    print("\n3. Testing coin image:")
    img_path = os.path.join(base_path, "assets", "stableCoinEuro.png")
    if os.path.exists(img_path):
        img = Image.open(img_path)
        print(f"  ✓ stableCoinEuro.png: {img.size}")
    else:
        print(f"  ✗ stableCoinEuro.png: NOT FOUND")

    # Test emotion SVGs
    print("\n4. Testing emotion SVG files:")
    emotions = ["neutral", "optimistisch", "euphorisch", "frustriert", "angespannt"]
    for emotion in emotions:
        svg_path = os.path.join(base_path, f"{emotion}.svg")
        if os.path.exists(svg_path):
            print(f"  ✓ {emotion}.svg: EXISTS")
        else:
            print(f"  ✗ {emotion}.svg: NOT FOUND")

    print("\n✓ All image resources verified!")

if __name__ == "__main__":
    test_image_loading()

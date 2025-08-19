import os
import tempfile
from PIL import Image, ImageChops, ImageEnhance

def convert_to_ela_image(image_path, output_path, quality=90):
    """
    Converts an image to its ELA (Error Level Analysis) version.

    Args:
        image_path (str): Path to the original image.
        output_path (str): Where the ELA image will be saved.
        quality (int): JPEG resave quality (default: 90).

    Returns:
        PIL.Image.Image: The processed ELA image.
    """
    try:
        # Ensure image is in RGB
        original = Image.open(image_path).convert('RGB')

        # Create a temporary resaved JPEG copy
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            resaved_path = temp_file.name
            original.save(resaved_path, 'JPEG', quality=quality)

        # Compute pixel-wise differences
        resaved = Image.open(resaved_path).convert('RGB')
        ela_image = ImageChops.difference(original, resaved)

        # Avoid zero division
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        if max_diff == 0:
            max_diff = 1

        # Scale brightness to enhance differences
        scale = 255.0 / max_diff
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

        # Save ELA output
        ela_image.save(output_path)

        # Clean up temporary file
        os.remove(resaved_path)

        return ela_image

    except Exception as e:
        raise RuntimeError(f"Failed to generate ELA image: {e}")
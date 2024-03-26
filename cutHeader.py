from PIL import Image

def cut_top_of_image(image_path, output_path, inches=1.7, dpi=72):
    """
    Cuts the top 'inches' of an image and saves the result.

    Parameters:
    - image_path: Path to the input image.
    - output_path: Path where the output image will be saved.
    - inches: The height of the top portion of the image to keep, in inches.
    - dpi: The DPI of the image. Defaults to 72.
    """
    # Calculate the height to keep in pixels
    height_to_keep = int(inches * dpi)

    # Open the image
    with Image.open(image_path) as img:
        # Calculate the box to crop: left, upper, right, lower
        crop_box = (0, 0, img.width, height_to_keep)

        # Perform the crop
        top_image = img.crop(crop_box)

        # Save or return the cropped image
        top_image.save(output_path)

# Example usage
image_path = 'CPP.png'
output_path = 'CPPHeader.png'
cut_top_of_image(image_path, output_path)

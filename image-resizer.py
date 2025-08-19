import argparse
from PIL import Image
import os

def resize_and_pad_image(input_path: str, output_path: str, target_size: int = None):
    """
    Crops any transparent padding, then resizes a PNG image to fit within a square
    canvas, maintaining its aspect ratio. The canvas size is determined by the
    largest dimension of the cropped image or a specified target size.

    Args:
        input_path (str): The path to the input PNG image file.
        output_path (str): The path where the output image will be saved.
        target_size (int, optional): The side length of the square canvas.
                                     If None, the largest dimension of the
                                     cropped image is used.
    """
    try:
        # Step 1: Open the original image and convert to RGBA to handle transparency
        with Image.open(input_path) as img:
            img = img.convert("RGBA")

            # Step 2: Find the bounding box of non-transparent content
            # The getbbox() method returns a tuple (left, top, right, bottom)
            # of the bounding box of the non-zero pixels in the image.
            bbox = img.getbbox()
            
            # If the image is not completely transparent, proceed
            if bbox:
                # Crop the image to the bounding box to remove transparent padding
                cropped_img = img.crop(bbox)
            else:
                # If the image is entirely transparent, skip cropping
                print(f"Warning: Image '{os.path.basename(input_path)}' is entirely transparent and will not be processed.")
                return

            # Step 3: Determine the target canvas size
            if target_size is None:
                # Use the largest dimension of the cropped image as the target
                target_dimension = max(cropped_img.size)
            else:
                target_dimension = target_size
            
            target_size_tuple = (target_dimension, target_dimension)

            # Step 4: Calculate new dimensions to fit the cropped image within the target size
            original_width, original_height = cropped_img.size
            scale = min(target_dimension / original_width, target_dimension / original_height)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            
            # Step 5: Resize the cropped image
            resized_img = cropped_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Step 6: Create a new, blank canvas with a transparent background
            new_img = Image.new("RGBA", target_size_tuple, (255, 255, 255, 0))

            # Step 7: Calculate the position to center the resized image on the new canvas
            x_offset = (target_dimension - new_width) // 2
            y_offset = (target_dimension - new_height) // 2

            # Step 8: Paste the resized image onto the center of the new canvas
            new_img.paste(resized_img, (x_offset, y_offset))

            # Step 9: Save the final image
            new_img.save(output_path, "PNG")
            
            print(f"Image resized to {target_dimension}x{target_dimension} and padded. Saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: The file at '{input_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def process_folder(input_folder: str, target_size: int = None):
    """
    Processes all PNG images in a given folder, resizing and padding them to
    a square canvas. Saves the new images to a 'resized_images' subfolder.

    Args:
        input_folder (str): The path to the folder containing the images.
        target_size (int, optional): The side length of the square canvas.
                                     If None, the largest dimension of the
                                     cropped image is used.
    """
    # Create the output directory if it doesn't exist
    output_folder = os.path.join(input_folder, 'resized_images')
    os.makedirs(output_folder, exist_ok=True)

    # List all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            print(f"Processing '{filename}'...")
            # Pass the target_size argument
            resize_and_pad_image(input_path, output_path, target_size)
            
    print("\nAll PNG images have been processed.")


if __name__ == "__main__":
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="Resize and pad all PNG images in a folder to a square canvas.")
    parser.add_argument("input_folder", help="Path to the folder containing the PNG images.")
    parser.add_argument("--size", type=int, default=None,
                        help="Optional: The side length for the square canvas. If not provided, the script will use the largest dimension of each image as the target size.")
    
    args = parser.parse_args()
    
    # Check if the input path is a valid directory
    if not os.path.isdir(args.input_folder):
        print(f"Error: The input path '{args.input_folder}' is not a valid directory.")
    else:
        # Call the function to process the folder with the new size argument
        process_folder(args.input_folder, args.size)

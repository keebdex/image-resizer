# PNG Image Resizer

A command-line tool written in Python to batch process and resize PNG images to a perfect square, with the option to remove extra transparent padding.

### Features

* **Automatic Cropping:** Removes excess transparent space around the image's content before resizing.

* **Square Sizing:** Resizes images to a square canvas, using either a user-specified size or the largest dimension of the original image.

* **Aspect Ratio Preservation:** Centers the image on the new canvas, ensuring the original aspect ratio is maintained.

* **Batch Processing:** Processes all PNG files within a specified folder.

### Prerequisites

You need Python 3 installed on your system.
This script requires the **Pillow** library for image manipulation, which you can install and run with `uv`.

```bash
uv pip install Pillow
```

### How to Use

1.  **Save the Script:** Save the Python code as a file named `main.py`.

2.  **Run from Terminal:** Open your terminal or command prompt and navigate to the directory where you saved the script.

3.  **Run the Script with `uv`:** After installing the prerequisites, you can run the script using `uv run`. This command handles finding the correct Python interpreter and executing the script.

    **Basic Usage:** To process all PNGs in a folder and resize them to a square based on their largest dimension:

    ```bash
    uv run main.py /path/to/your/images
    ```

    This will create a `resized_images` subfolder within your specified directory and save the output there.

    **Specify a Custom Size:** To process all PNGs in a folder and resize them to a fixed 500x500 canvas:

    ```bash
    uv run main.py /path/to/your/images --size 500
    ```

### Example

Let's say you have a folder named `my_photos` with these files:

```bash
my_photos/
├── logo_with_padding.png (1000x500)
├── photo_tall.png (400x800)
└── another_photo.png (600x600)
```

Running the script with the basic command:

```bash
uv run main.py my_photos
```

The script will process each file and save the output in `my_photos/resized_images/`:

* `logo_with_padding.png` will be cropped to its content (let's say 800x400) and then resized to an 800x800 square.
* `photo_tall.png` will be resized to an 800x800 square.
* `another_photo.png` will remain a 600x600 square (though its file properties will be updated).
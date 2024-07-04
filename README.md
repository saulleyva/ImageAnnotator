# ImageAnnotator
A Python tool for annotating images with instance segmentation masks. This script allows users to draw and save masks with unique colors for each instance, making it useful for tasks such as segmenting glistening effects in AS-OCT images or other similar image segmentation projects.

## Features
- Annotate images by drawing on them with unique colors for each instance.
- Supports undoing the last drawing action.
- Optionally applies CLAHE for contrast enhancement.
- Saves the generated masks in the specified directory.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ImageAnnotator.git
    ```

2. Install the required dependencies:
    ```sh
    cd ImageAnnotator
    pip install opencv-python-headless numpy matplotlib
    ```

## Usage
1. Prepare your images and specify the paths in the script.
    ```python
    annotator = ImageAnnotator(
        image_path="images\\example.png",
        mask_save_path="masks\\example.png"
    )
    ```
2. Optional: Configure Parameters. Before running the script, you can customize the parameters to suit your needs. The parameters available for customization include:

- `paint_button`: The mouse button to use for drawing (default: 3 for right mouse button).
- `circle_size`: The size of the circle to draw (default: 3).
- `redo_key`: The key to press to undo the last drawing action (default: 'z').
- `max_history_size`: The maximum number of images to keep in the drawing history for undo functionality (default: 15).
- `apply_clahe`: Whether to apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to the image before annotating (default: True).
- `brightness_threshold`: The minimum brightness of the colors to be used for drawing (default: 80).

3. Run the script:
    ```sh
    python image_annotator.py
    ```

4. Use the mouse to draw on the image and create masks.
    - Right mouse button to draw (default, can be changed).
    - Press 'z' to undo the last drawing action.

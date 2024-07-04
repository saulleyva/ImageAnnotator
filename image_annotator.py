import os
import random
import cv2
import numpy as np
from matplotlib import pyplot as plt

class ImageAnnotator:
    """
    Annotate an image by drawing on it and save the mask.

    Args:
        image_path (str): The path to the image file.
        mask_save_path (str): The path to save the generated mask file.
        paint_button (int): The mouse button to use for drawing (1 for left, 2 for middle, 3 for right).
        circle_size (int): The size of the circle to draw.
        redo_key (str): The key to press to undo the last drawing.
        max_history_size (int): The maximum number of images in the drawing history, if redo_key is pressed.
        apply_clahe (bool): Whether to apply CLAHE to the image before annotating.
        brightness_threshold (int): The minimum brightness of the colors to be used for drawing.
    """

    def __init__(self, image_path, mask_save_path, paint_button=3, circle_size=3, redo_key='z', max_history_size=15, apply_clahe=True, brightness_threshold=80):
        # Set the arguments as attributes
        self.image_path = image_path
        self.mask_save_path = mask_save_path
        self.redo_key = redo_key
        self.paint_button = paint_button
        self.apply_clahe = apply_clahe
        self.brightness_threshold = brightness_threshold
        self.circle_size = circle_size
        self.max_history_size = max_history_size

        # Initialize the image, plot, mask, and other attributes
        self.img = self.load_and_prepare_image()
        self.fig, self.ax, self.im = self.setup_plot()
        self.mask = np.zeros_like(self.img)
        self.mask_history = [self.mask.copy()]
        self.is_pressing = False
        self.used_colors = set()
        self.current_color = self.generate_random_color()

        # Connect the event handlers for drawing
        self.connect_event_handlers()

    def load_and_prepare_image(self):
        """Load the image and apply CLAHE if needed."""
        img = cv2.cvtColor(cv2.imread(self.image_path, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        if self.apply_clahe:
            lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            img = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
        return img

    def setup_plot(self):
        """Create a plot with the image and hide the axes."""
        fig, ax = plt.subplots(figsize=(18, 10))
        im = ax.imshow(self.img)
        ax.axis("off")
        return fig, ax, im

    def connect_event_handlers(self):
        """Connect the event handlers for drawing on the image."""
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def on_press(self, event):
        """Start drawing a circle at the mouse position when the button is pressed."""
        if event.inaxes and event.button == self.paint_button:
            self.is_pressing = True
            self.draw_circle(event.xdata, event.ydata)

    def on_motion(self, event):
        """Draw a circle at the mouse position while the button is pressed."""
        if self.is_pressing and event.inaxes:
            self.draw_circle(event.xdata, event.ydata)

    def on_release(self, event):
        """Finish drawing the circle and update the mask and display."""
        if event.button == self.paint_button:
            self.is_pressing = False
            self.overlay_mask_on_image()
            self.update_drawing_history()
            self.current_color = self.generate_random_color()

    def on_key(self, event):
        """Undo the last drawing if the redo key is pressed."""
        if event.key == self.redo_key and len(self.mask_history) > 1:
            self.undo_last_drawing()

    def generate_random_color(self):
        """Generate a random color with a minimum brightness."""
        while True:
            color = tuple(random.randint(0, 255) for _ in range(3))
            if color not in self.used_colors and sum(color) / 3 > self.brightness_threshold:
                self.used_colors.add(color)
                return color

    def draw_circle(self, xdata, ydata):
        """Draw a circle on the mask at the given coordinates."""
        x, y = int(xdata), int(ydata)
        cv2.circle(self.mask, (x, y), self.circle_size, self.current_color, -1)

    def overlay_mask_on_image(self):
        """Overlay the mask on the image and update the display."""
        overlay = self.img.copy()
        mask_nonzero = np.any(self.mask != 0, axis=-1)
        overlay[mask_nonzero] = self.mask[mask_nonzero]
        self.im.set_data(overlay)
        self.fig.canvas.draw_idle()

    def update_drawing_history(self):
        """Update the drawing history with the current mask."""
        self.mask_history.append(self.mask.copy())
        if len(self.mask_history) > self.max_history_size:
            self.mask_history.pop(0)

    def undo_last_drawing(self):
        """Undo the last drawing by reverting to the previous mask."""
        self.mask_history.pop()
        self.mask = self.mask_history[-1].copy()
        self.overlay_mask_on_image()

    def save_mask(self):
        """Save the generated mask to the given path."""
        os.makedirs(os.path.dirname(self.mask_save_path), exist_ok=True)
        cv2.imwrite(self.mask_save_path, cv2.cvtColor(self.mask, cv2.COLOR_RGB2BGR))

    def show(self):
        """Show the image and start the interactive drawing."""
        plt.tight_layout()
        plt.show()
        self.save_mask()


if __name__ == "__main__":
    annotator = ImageAnnotator(
        image_path="images\\radial1.png",
        mask_save_path="masks\\radial1.png"
    )
    annotator.show()

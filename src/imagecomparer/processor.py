"""
processor.py

Image processing engine for ImageComparer Pro.

Responsibilities
----------------
- Load image
- Store original image
- Apply RGB adjustments
- Convert to QImage
- Save modified image
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from PIL import Image

from PySide6.QtGui import QImage


class ImageProcessor:
    """
    Performs all image processing.

    The original image is never modified.
    Every adjustment is generated from the original image.
    """

    def __init__(self):

        self.original_image: Image.Image | None = None
        self.modified_image: Image.Image | None = None

        self.original_array: np.ndarray | None = None
        self.modified_array: np.ndarray | None = None

        self.red = 0
        self.green = 0
        self.blue = 0

    # --------------------------------------------------

    @property
    def has_image(self) -> bool:

        return self.original_image is not None

    # --------------------------------------------------

    def reset(self):

        self.red = 0
        self.green = 0
        self.blue = 0

        if self.original_array is not None:
            self.modified_array = self.original_array.copy()

            self.modified_image = Image.fromarray(
                self.modified_array,
                "RGBA"
            )

    # --------------------------------------------------

    def load_image(self, filename: str | Path):

        filename = Path(filename)

        image = Image.open(filename)

        image = image.convert("RGBA")

        self.original_image = image

        self.original_array = np.array(
            image,
            dtype=np.uint8
        )

        self.modified_array = self.original_array.copy()

        self.modified_image = Image.fromarray(
            self.modified_array,
            "RGBA"
        )

        self.reset()

    # --------------------------------------------------

    def save_image(self, filename: str | Path):

        if self.modified_image is None:
            return

        self.modified_image.save(filename)

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

    # --------------------------------------------------

    def set_rgb(
        self,
        red: int,
        green: int,
        blue: int,
    ) -> None:
        """
        Update the RGB adjustments and regenerate the modified image.
        """

        self.red = int(red)
        self.green = int(green)
        self.blue = int(blue)

        self._process()

    # --------------------------------------------------

    def _process(self) -> None:
        """
        Apply RGB adjustments to the original image.

        The original image is never modified.
        """

        if self.original_array is None:
            return

        # Work in a signed integer format so negative values are allowed.
        rgb = self.original_array[:, :, :3].astype(np.int16)

        rgb[:, :, 0] += self.red
        rgb[:, :, 1] += self.green
        rgb[:, :, 2] += self.blue

        np.clip(rgb, 0, 255, out=rgb)

        # Start with a copy so the alpha channel is preserved.
        result = self.original_array.copy()

        result[:, :, :3] = rgb.astype(np.uint8)

        self.modified_array = result

        self.modified_image = Image.fromarray(
            result,
            "RGBA"
        )

        # Invalidate cached Qt image.
        self._modified_qimage = None

    # --------------------------------------------------

    def get_original_qimage(self) -> QImage | None:

        if self.original_array is None:
            return None

        if self._original_qimage is None:

            image = np.ascontiguousarray(self.original_array)

            self._original_qimage = QImage(
                image.data,
                image.shape[1],
                image.shape[0],
                image.strides[0],
                QImage.Format_RGBA8888,
            ).copy()

        return self._original_qimage

    # --------------------------------------------------

    def get_modified_qimage(self) -> QImage | None:

        if self.modified_array is None:
            return None

        if self._modified_qimage is None:

            image = np.ascontiguousarray(self.modified_array)

            self._modified_qimage = QImage(
                image.data,
                image.shape[1],
                image.shape[0],
                image.strides[0],
                QImage.Format_RGBA8888,
            ).copy()

        return self._modified_qimage

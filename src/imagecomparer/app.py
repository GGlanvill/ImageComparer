from PySide6.QtWidgets import QApplication

from imagecomparer.constants import APP_NAME


class ImageComparerApp(QApplication):

    def __init__(self, argv):

        super().__init__(argv)

        self.setApplicationName(APP_NAME)

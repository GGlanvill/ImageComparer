import sys

from imagecomparer.app import ImageComparerApp
from imagecomparer.ui.main_window import MainWindow


def main():

    app = ImageComparerApp(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

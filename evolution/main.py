import sys
from PySide6.QtWidgets import QApplication
from evolution.ui.gui import EvolutionGUI
from evolution.services.logger_setup import setup_logging

def main():
    """Main function to run the Evolution GUI."""
    setup_logging()
    app = QApplication(sys.argv)
    window = EvolutionGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

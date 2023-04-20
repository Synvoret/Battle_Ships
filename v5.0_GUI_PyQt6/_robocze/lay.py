from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedLayout
import sys

def show_first_view(self):
        # ustawianie pierwszego widgeta jako aktualny widget QStackedLayout
        self.stacked_layout.setCurrentWidget(self.main_widget)
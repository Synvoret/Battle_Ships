# from PyQt6.QtCore import QThread, QUrl
# from PyQt6.QtMultimedia import QMediaPlayer, QSoundEffect

# class SoundThread(QThread):
#     def __init__(self, file_path):
#         super().__init__()
#         self.file_path = file_path

#     def run(self):
#         sound_effect = QSoundEffect()
#         sound_effect.setSource(QUrl.fromLocalFile(self.file_path))
#         sound_effect.play()


# from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

# app = QApplication([])
# window = QWidget()
# layout = QVBoxLayout()

# button = QPushButton("PLAY explosion")
# layout.addWidget(button)

# def play_sound():
#     thread = SoundThread(r"C:/Users/lukasz.szabat/Desktop/KursPython/_free_apps/battle_ships/v5.0_GUI_PyQt6/data/sounds/explosion.wav")
#     thread.start()
#     thread.wait()
#     del thread

# button.clicked.connect(play_sound)

# window.setLayout(layout)
# window.show()
# app.exec()




import sys
import time

from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal, QUrl
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

class SoundPlayer(QObject):
    finished = pyqtSignal()

    def __init__(self, sound_file):
        super().__init__()
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile(sound_file))

    def play(self):
        self.sound.play()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        button = QPushButton("Play Sound")
        button.clicked.connect(self.play_sound)
        layout.addWidget(button)

        self.setLayout(layout)

    def play_sound(self):
        sound_player = SoundPlayer(r"C:/Users/lukasz.szabat/Desktop/KursPython/_free_apps/battle_ships/v5.0_GUI_PyQt6/data/sounds/explosion.wav")
        thread = QThread()
        sound_player.moveToThread(thread)
        sound_player.finished.connect(thread.quit)
        thread.started.connect(sound_player.play)
        thread.finished.connect(sound_player.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.start()
        thread.wait()
        del thread

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

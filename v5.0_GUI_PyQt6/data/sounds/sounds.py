from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QGraphicsScene, QGraphicsView, QPushButton, QSizePolicy, QHBoxLayout, QMenuBar, QMenu, QSpinBox, QLineEdit, QStackedWidget, QStackedLayout, QInputDialog, QMessageBox, QTableWidget, QTableWidgetItem, QLayout, QBoxLayout, QGroupBox, QStyle, QTextEdit, QFileDialog, QSpacerItem
from PyQt6.QtGui import QPixmap, QIcon, QImage, QBrush, QFont, QPainter, QAction, QCursor, QPalette, QColor, QTextCursor, QGuiApplication
from PyQt6.QtCore import QSize, Qt, QRectF, QTimer, QFileInfo, QBuffer, QCoreApplication, QUrlQuery, QRect, QThread
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6 import QtCore, QtGui, QtMultimedia
from PyQt6.QtCore import QUrl, QMargins, QThreadPool
from PyQt6.QtMultimedia import QSoundEffect, QMediaPlayer, QAudioOutput
import time


class SeaSound:
    
    def __init__(self):
        self.seaS = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.seaS.setAudioOutput(self.audioOutput)
        self.seaS.setSource(QUrl.fromLocalFile('data\sounds\creaky_ship.mp3'))
        self.start_volume = 0.2
        self.audioOutput.setVolume(self.start_volume)
    
    def sea_sound_start(self):
        self.seaS.play()
        # for i in range(50):
        #     self.audioOutput.setVolume(i / 50)
    
    def sea_sound_stop(self):
        self.seaS.stop()
    
    def sea_sound_play(self):
        self.sea_sound_start()
        QTimer.singleShot(5000, self.sea_sound_stop) # zatrzymaj odtwarzanie po 5 sekundach


class ShotSound:
    
    def __init__(self):
        self.shotS = QSoundEffect()
        self.shotS.setSource(QUrl.fromLocalFile('data\sounds\shot.wav'))
        self.start_volume = 0.2
        self.shotS.setVolume(0.2)
    
    def shot_sound_start(self):
        self.shotS.play()
        # for i in range(50):
        #     self.audioOutput.setVolume(i / 50)
    
    def shot_sound_stop(self):
        self.shotS.stop()
    
    def shot_sound_play(self):
        self.shot_sound_start()
        QTimer.singleShot(5000, self.shot_sound_stop) # zatrzymaj odtwarzanie po 5 sekundach


class HitSound:
    
    def __init__(self):
        self.hitS = QSoundEffect()
        self.hitS.setSource(QUrl.fromLocalFile('data\sounds\hit.wav'))
        self.start_volume = 0.2
        self.hitS.setVolume(self.start_volume)
    
    def hit_sound_start(self):
        self.hitS.play()
        # for i in range(50):
        #     self.audioOutput.setVolume(i / 50)
    
    def hit_sound_stop(self):
        self.hitS.stop()
    
    def hit_sound_play(self):
        self.hit_sound_start()
        QTimer.singleShot(5000, self.hit_sound_stop) # zatrzymaj odtwarzanie po 5 sekundach


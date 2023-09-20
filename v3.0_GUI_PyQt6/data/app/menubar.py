import sys, os, random, itertools, re

from data.db.db import *

from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QGraphicsScene,
    QGraphicsView,
    QPushButton,
    QSizePolicy,
    QHBoxLayout,
    QMenuBar,
    QMenu,
    QSpinBox,
    QLineEdit,
    QStackedWidget,
    QStackedLayout,
    QInputDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt6.QtGui import QPixmap, QIcon, QImage, QBrush, QFont, QPainter, QAction
from PyQt6.QtCore import (
    QSize,
    Qt,
    QRectF,
    QTimer,
    QFileInfo,
    QBuffer,
    QCoreApplication,
    QUrlQuery,
)
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect

# def menu_bar():

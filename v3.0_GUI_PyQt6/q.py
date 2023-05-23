from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Tabela")
        
        # Tworzenie tabeli
        table = QTableWidget()
        table.setColumnCount(6)
        table.setRowCount(10)
        
        # Wyłączenie numeracji wierszy
        table.verticalHeader().setVisible(False)
        
        # Dodanie komórek do tabeli
        for row in range(10):
            for col in range(6):
                item = QTableWidgetItem(f"({row},{col})")
                table.setItem(row, col, item)
        
        # Wyśrodkowanie tabeli w layoucie
        layout = QVBoxLayout()
        layout.addWidget(table)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

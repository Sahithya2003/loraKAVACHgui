import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QVBoxLayout, QWidget
from PyQt5.QtCore import QUrl

class HTMLViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTML Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.text_browser = QTextBrowser(self)
        self.layout.addWidget(self.text_browser)

        self.open_html_file("map_rssi.html")

    def open_html_file(self, file_path):
        with open(file_path, "r") as f:
            html_content = f.read()
            self.text_browser.setHtml(html_content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = HTMLViewerApp()
    main_win.show()
    sys.exit(app.exec_())

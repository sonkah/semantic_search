from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QLineEdit, QPushButton, QWidget, QVBoxLayout, QComboBox, \
    QApplication, QPlainTextEdit, QMenu, QDialog, QListWidget, QAction
from PyQt5.QtGui import QIntValidator
import sys, traceback
from SemanticSearchEngine import SemanticSearchEngine


def loadCorpusMock():
    ye = open('YorkEngland.txt', 'r')
    yeText = ye.read()
    ye.close()
    ya = open('YorkAustralia.txt', 'r')
    yaText = ya.read()
    ya.close()
    ny = open('NewYork.txt', 'r')
    nyText = ny.read()
    ny.close()
    return [yeText, yaText, nyText], ['YorkEngland', 'YorkAustraila', 'NewYork']


class MainWindow(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setGeometry(50, 50, 500, 400)
        self.setWindowTitle("Semantic search engine")

        cw = QWidget(self)
        self.setCentralWidget(cw)
        layout = QVBoxLayout(cw)

        topBarLayout = QHBoxLayout(self)
        self.searchbox = QLineEdit(self)
        self.triggerButton = QPushButton('Search')
        self.triggerButton.clicked.connect(self.search)
        self.searchbox.returnPressed.connect(self.search)
        topBarLayout.addWidget(self.searchbox)
        topBarLayout.addWidget(self.triggerButton)
        self.topBar = QWidget(self)
        self.topBar.setLayout(topBarLayout)

        layout.addWidget(self.topBar)

        self.vectorTypeCombobox = QComboBox()
        self.vectorTypeCombobox.addItems(['BoW', 'TFIDF', 'Word2Vec'])
        self.distanceCombobox = QComboBox()
        self.distanceCombobox.addItems(['L1', 'L2', 'Cosine'])
        self.decompositionAlgCombobox = QComboBox()
        self.decompositionAlgCombobox.addItems(['SVD', 'PCA', 'LDiA'])
        self.nInput = QLineEdit()
        self.nInput.setPlaceholderText('Ilość analizowanych tematów')
        self.nInput.setText('1')


        layout.addWidget(self.vectorTypeCombobox)
        layout.addWidget(self.distanceCombobox)
        layout.addWidget(self.decompositionAlgCombobox)
        layout.addWidget(self.nInput)

        self.output = QPlainTextEdit()
        layout.addWidget(self.output)

    def search(self):
        try:
            vectortype = self.vectorTypeCombobox.currentText().lower()
            distance = self.distanceCombobox.currentText().lower()
            da = self.decompositionAlgCombobox.currentText().lower()
            n = int(self.nInput.text())
            question = self.searchbox.text().lower()
            sse = SemanticSearchEngine(distance, vectortype, da, n)
            corpus, labels = loadCorpusMock()
            sse.loadData(corpus, labels)
            answer = sse.askQuestion(question)
            self.output.setPlainText(answer)
        except Exception as e:
            print(traceback.format_exc())

if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec_())

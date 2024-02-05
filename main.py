import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

SCREEN_SIZE = [1000, 700]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        # self.getImage()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.show_map_btn = QPushButton(self)
        self.show_map_btn.setText('показать карту')
        self.show_map_btn.setGeometry(30, 300, 120, 120)


        self.spn_text = QLabel(self)
        self.spn_text.setText('Введите параметры spn через запятую: ')
        self.spn_text.setGeometry(15, 50, 250, 50)

        self.ll_text = QLabel(self)
        self.ll_text.setText('Введите параметры ll через запятую: ')
        self.ll_text.setGeometry(15, 150, 250, 50)

        self.spn_inp = QLineEdit(self)
        self.spn_inp.setGeometry(30, 100, 150, 50)

        self.ll_inp = QLineEdit(self)
        self.ll_inp.setGeometry(30, 200, 150, 50)

        self.show_map_btn.clicked.connect(self.getImage)

        ## Изображение


    def getImage(self):
        spn, ll = self.spn_inp.text(), self.ll_inp.text()
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.setGeometry(350, 90, 600, 450)
        self.image.setPixmap(self.pixmap)
        self.image.show()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
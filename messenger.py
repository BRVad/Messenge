from datetime import datetime

import requests
from PyQt5 import QtWidgets, QtCore

from clientui import Ui_Dialog


class Messenger(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)

        self.url = url
        self.after_id = -1

        self.pushButton.pressed.connect(self.pressed_button)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def pretty_print(self, message):
        """
        2020/09/23 16:12:55 Lika
        Text

        """
        dt = datetime.fromtimestamp(message['timestamp'])
        dt = dt.strftime('%Y/%m/%d %H:%M:%S')

        self.textBrowser.append(dt + ' ' + message['name'])
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')
        self.textBrowser.repaint()

    def update_messages(self):
        response = None

        try:
            response = requests.get(self.url + '/messages',
                                    params={'after_id': self.after_id})
        except:
            pass

        if response and response.status_code == 200:
            messages = response.json()['messages']
            for message in messages:
                self.pretty_print(message)
                self.after_id = message['timestamp']

        # TODO paginate if messages

    def pressed_button(self):
        name = self.nameinput.text()
        text = self.textinput.toPlainText()
        data = {'name': name,
                'text': text}
        response = requests.post(self.url + '/send', json=data)
        # TODO обрабатывать ошибки
        self.textinput.clear()
        self.textinput.repaint()


app = QtWidgets.QApplication([])
window = Messenger('http://127.0.0.1:5000')
window.show()
app.exec_()

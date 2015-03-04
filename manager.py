#!/usr/bin/env python3

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QListWidget,
                             QGridLayout, QFileDialog, QStyle,
                             QAbstractItemView, QShortcut)
import sys
import atexit


# change this
playlist = '/home/china/playlist.m3u'


def loadDialog(listView):
    fileNames = QFileDialog.getOpenFileNames()
    if len(fileNames[0]) > 0:
        listView.addItems(fileNames[0])


def deleteItem(listView):
    listView.takeItem(listView.currentRow())


def moveItem(listView, mod):
    currentRow = listView.currentRow()
    currentItem = listView.takeItem(currentRow)
    listView.insertItem(currentRow + mod, currentItem)
    listView.setCurrentRow(currentRow + mod)


def saveList(listView):
    with open(playlist, 'w') as f:
        for item in range(0, listView.count()):
            f.write(listView.item(item).text() + '\n')


def populateList(listView):
    with open(playlist, 'r') as f:
        for line in f:
            test = line.split('\n')
            listView.addItem(test[0])


def exitApp(listView):
    saveList(listView)
    exit()


def main():
    app = QApplication(sys.argv)
    screen = QWidget()

    # widgets
    loadButton = QPushButton("&Add item", screen)
    deleteButton = QPushButton("", screen)
    upButton = QPushButton("", screen)
    downButton = QPushButton("", screen)
    listView = QListWidget(screen)

    # widget positions
    loadButton.setGeometry(QRect(10, 10, 100, 32))
    deleteButton.setGeometry(QRect(474, 10, 32, 32))
    upButton.setGeometry(QRect(516, 10, 32, 32))
    downButton.setGeometry(QRect(558, 10, 32, 32))
    listView.setGeometry(QRect(10, 50, 580, 440))

    # button icons
    deleteButton.setIcon(deleteButton.style().standardIcon(QStyle.SP_DialogDiscardButton))
    upButton.setIcon(upButton.style().standardIcon(QStyle.SP_ArrowUp))
    downButton.setIcon(downButton.style().standardIcon(QStyle.SP_ArrowDown))

    # events
    listView.setDragDropMode(QAbstractItemView.InternalMove)
    loadButton.clicked.connect(lambda: loadDialog(listView))
    upButton.clicked.connect(lambda: moveItem(listView, -1))
    downButton.clicked.connect(lambda: moveItem(listView, +1))
    deleteButton.clicked.connect(lambda: deleteItem(listView))

    # shortcuts
    delHotkey = QShortcut(listView)
    upHotkey = QShortcut(listView)
    downHotkey = QShortcut(listView)

    delHotkey.setKey(Qt.Key_Delete)
    upHotkey.setKey(Qt.CTRL + Qt.Key_Up)
    downHotkey.setKey(Qt.CTRL + Qt.Key_Down)

    delHotkey.activated.connect(lambda: deleteItem(listView))
    upHotkey.activated.connect(lambda: moveItem(listView, -1))
    downHotkey.activated.connect(lambda: moveItem(listView, +1))

    # screen setup
    screen.setWindowTitle('Playlist Manager')
    screen.resize(600, 500)
    populateList(listView)
    screen.show()
    atexit.register(saveList, listView)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

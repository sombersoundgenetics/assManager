import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtCore import QFile

from PySide2 import QtGui

from thumb import Thumbnail
from arnold import *

from os import remove, path

from time import sleep

source = "blah/blash.ass"
target = "blah blah.jpeg"
light = "blah blah blah.ass "

class Paths:
    def __init__(self, the_path):

        self.path = str(the_path)
        split = path.split(self.path)
        self.name = split[1]
        self.parent = split[0]
        self.ext = path.splitext(self.path)[1]


    def setparams(self, param):
        param['path'] = self.path
        param['name'] = self.name
        param['parent'] = self.parent


class MainWindow:
    def __init__(self):
        app = QApplication(sys.argv)

        self.fileName = None

        ui_file = QFile("GUI/mainwindow.ui")
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        self.myThumbnail = Thumbnail(source)

        pushbutton_render = self.window.findChild(QPushButton, 'pushbutton_render')

        toolbutton_source = self.window.findChild(QToolButton, 'toolbutton_source')
        toolbutton_destination = self.window.findChild(QToolButton, 'toolbutton_destination')
        toolbutton_lights = self.window.findChild(QToolButton, 'toolbutton_lights')

        toolbutton_source.clicked.connect(self.getsource)
        toolbutton_destination.clicked.connect(self.getdestination)
        toolbutton_lights.clicked.connect(self.getlights)

        pushbutton_render.clicked.connect(self.render)

        self.window.show()

        sys.exit(app.exec_())


    def getsource(self):
        fileName = self.pick()
        line_source = self.window.findChild(QLineEdit, 'line_source')
        line_destination = self.window.findChild(QLineEdit, 'line_destination')

        check_useDest = self.window.findChild(QCheckBox, 'check_useDest')


        param = self.myThumbnail.params['paths']['source']
        source_path = Paths(fileName)
        source_path.setparams(param)

        line_source.setText(self.myThumbnail.params['paths']['source']['path'])

        if not check_useDest.isChecked() :

            param = self.myThumbnail.params['paths']['target']

            target_path = Paths(path.join(self.myThumbnail.params['paths']['source']['parent'],
                                          path.splitext(self.myThumbnail.params['paths']['source']['name'])[0] +
                                          "-thumbnail.jpeg"))
            #print target_path.path
            target_path.setparams(param)
            line_destination.setText(self.myThumbnail.params['paths']['target']['path'])

        print self.myThumbnail.params['paths']['source']

    def getdestination(self):
        fileName = self.save()
        line_destination = self.window.findChild(QLineEdit, 'line_destination')
        check_useDest = self.window.findChild(QCheckBox, 'check_useDest')

        line_destination.setText(fileName)
        check_useDest.setEnabled(True)
        check_useDest.setChecked(True)

    def getlights(self):
        fileName = self.pick()
        line_lights = self.window.findChild(QLineEdit, 'line_lights')
        line_lights.setText(fileName)

    def render(self):
        AiBegin()
        label_imagebox = self.window.findChild(QLabel, 'label_imagebox')
        label_imagebox.clear()
        label_imagebox.setText("RENDERING THUMBNAIL")
        label_imagebox.repaint()

        box_resolution = self.window.findChild(QSpinBox, 'box_resolution')
        box_sample = self.window.findChild(QSpinBox, 'box_sample')
        box_fov = self.window.findChild(QSpinBox, 'box_fov')
        box_azimuth = self.window.findChild(QSpinBox, 'box_azimuth')
        box_zenith = self.window.findChild(QSpinBox, 'box_zenith')
        box_position = self.window.findChild(QDoubleSpinBox, 'box_position')
        box_overscan = self.window.findChild(QDoubleSpinBox, 'box_overscan')

        assfile = path.join(self.myThumbnail.params['paths']['target']['parent'],
                            path.splitext(self.myThumbnail.params['paths']['target']['name'])[0] +
                            ".ass")

        self.myThumbnail.params['universe']['options']['resolution'] = box_resolution.value()
        self.myThumbnail.params['universe']['options']['quality'] = box_sample.value()
        self.myThumbnail.params['universe']['camera']['fov'] = box_fov.value()
        self.myThumbnail.params['universe']['camera']['azimuth'] = box_azimuth.value()
        self.myThumbnail.params['universe']['camera']['zenith'] = box_zenith.value()
        self.myThumbnail.params['universe']['camera']['position'] = box_position.value()
        self.myThumbnail.params['universe']['camera']['overscan'] = box_overscan.value()


        param = self.myThumbnail.params['paths']['assfile']
        assfile_path = Paths(assfile)
        assfile_path.setparams(param)

        image_path = self.myThumbnail.params['paths']['target']['name']
        ass_path = self.myThumbnail.params['paths']['assfile']['name']

        if path.exists(path.abspath(image_path)):
            print "removing old thumbnail"
            remove(image_path)

        if path.exists(path.abspath(ass_path)):
            print "removing old ass file"
            remove(ass_path)

        self.myThumbnail.create()
        self.myThumbnail.render()

        label_imagebox.clear()
        image = QtGui.QPixmap(image_path)
        label_imagebox.setPixmap(image)
        label_imagebox.repaint()
        AiEnd()

    def pick(self):
        fileName = QFileDialog().getOpenFileName()[0]

        if fileName:
            return fileName

    def save(self):
        fileName = QFileDialog().getSaveFileName()[0]

        if fileName:
            return fileName




if __name__ == "__main__":
    MyWindow = MainWindow()



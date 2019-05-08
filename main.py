import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtCore import QFile

from PySide2 import QtGui

from thumb import Thumbnail
from arnold import *

from os import remove, path, getcwd, chdir


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

        self.home = getcwd()

        self.thumbnail = Thumbnail()

        self.fileName = None

        ui_file = QFile("GUI/mainwindow.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        self.pushbutton_render = self.window.findChild(QPushButton, 'pushbutton_render')
        self.toolbutton_source = self.window.findChild(QToolButton, 'toolbutton_source')
        self.toolbutton_destination = self.window.findChild(QToolButton, 'toolbutton_destination')
        self.toolbutton_lights = self.window.findChild(QToolButton, 'toolbutton_lights')
        self.line_source = self.window.findChild(QLineEdit, 'line_source')
        self.line_destination = self.window.findChild(QLineEdit, 'line_destination')
        self.check_useDest = self.window.findChild(QCheckBox, 'check_useDest')
        self.line_lights = self.window.findChild(QLineEdit, 'line_lights')
        self.label_imagebox = self.window.findChild(QLabel, 'label_imagebox')
        self.box_resolution = self.window.findChild(QSpinBox, 'box_resolution')
        self.box_sample = self.window.findChild(QSpinBox, 'box_sample')
        self.box_fov = self.window.findChild(QSpinBox, 'box_fov')
        self.box_azimuth = self.window.findChild(QSpinBox, 'box_azimuth')
        self.box_zenith = self.window.findChild(QSpinBox, 'box_zenith')
        self.box_position = self.window.findChild(QDoubleSpinBox, 'box_position')
        self.box_overscan = self.window.findChild(QDoubleSpinBox, 'box_overscan')
        self.label_imagebox = self.window.findChild(QLabel, 'label_imagebox')

        self.gui()

        sys.exit(app.exec_())

    def gui(self):
        self.window.show()

        self.pushbutton_render.clicked.connect(self.render)

        self.toolbutton_source.clicked.connect(self.source_path)
        self.toolbutton_destination.clicked.connect(self.target_path)
        self.toolbutton_lights.clicked.connect(self.lights_path)

        self.line_source.editingFinished.connect(self.set_source_path)
        self.line_destination.editingFinished.connect(self.set_target_path)
        self.line_lights.editingFinished.connect(self.set_light_path)

    def render(self):
        chdir(self.home)
        self.set_all()
        self.thumbnail.params['paths']['light']['path'] = path.abspath(self.thumbnail.params['paths']['light']['path'])

        if path.exists(self.thumbnail.params['paths']['source']['path']) and path.exists(self.thumbnail.params['paths']['light']['path']):
            self.status("RENDERING THUMBNAIL")

            image_path = self.thumbnail.params['paths']['target']['path']
            ass_path = self.thumbnail.params['paths']['assfile']['path']

            if path.exists(path.abspath(image_path)):
                print "removing old thumbnail"
                remove(image_path)

            if path.exists(path.abspath(ass_path)):
                print "removing old ass file"
                remove(ass_path)

            AiBegin()
            self.thumbnail.create()
            self.thumbnail.render()
            AiEnd()

            self.imagebox(image_path)

        elif not path.exists(self.thumbnail.params['paths']['source']['path']):
            self.status("INVALID ASSET")
            return False

        elif not path.exists(self.thumbnail.params['paths']['light']['path']):
            self.status("INVALID LIGHT")
            return False

    def status(self,status):
        self.label_imagebox.clear()
        self.label_imagebox.setText(status)
        self.label_imagebox.repaint()

    def imagebox(self,image_path):
        if path.exists(image_path):
            image = QtGui.QPixmap(image_path)
            self.label_imagebox.clear()
            self.label_imagebox.setPixmap(image)
            self.label_imagebox.repaint()
        else:
            return False

    def source_path(self):
        myFile = self.open_dialog()

        if myFile:
            self.line_source.setText(myFile)
            self.set_source_path()
        else:
            return False

    def target_path(self):
        myFile = self.save_dialog()

        if myFile:
            self.line_source.setText(myFile)
            self.set_target_path()
        else:
            return False

    def lights_path(self):
        myFile = self.open_dialog()

        if myFile:
            self.line_lights.setText(myFile)
            self.set_light_path()
        else:
            return False

    def open_dialog(self):
        return QFileDialog().getOpenFileName()[0]

    def save_dialog(self):
        return QFileDialog().getSaveFileName()[0]

    def set_all(self):
        self.set_source_path()
        self.set_target_path()
        self.set_light_path()
        self.set_resolution()
        self.set_quality()
        self.set_fov()
        self.set_azimuth()
        self.set_zenith()
        self.set_position()
        self.set_overscan()

    def set_source_path(self):
        param = self.thumbnail.params['paths']['source']
        myFile = self.line_source.text()

        myPath = Paths(myFile)
        myPath.setparams(param)

        if not self.check_useDest.isChecked():
            target_name = path.splitext(self.thumbnail.params['paths']['source']['name'])[0] + "-thumbnail.jpeg"
            target = path.join(self.thumbnail.params['paths']['source']['parent'], target_name)
            self.line_destination.setText(target)

            self.set_target_path()

    def set_target_path(self):
        param = self.thumbnail.params['paths']['target']
        myFile = self.line_destination.text()
        myPath = Paths(myFile)
        myPath.setparams(param)

        param = self.thumbnail.params['paths']['assfile']
        ass_name = path.splitext(self.thumbnail.params['paths']['source']['name'])[0] + "-thumbnail.ass"
        ass = path.join(self.thumbnail.params['paths']['source']['parent'], ass_name)
        myPath = Paths(ass)
        myPath.setparams(param)

    def set_light_path(self):
        param = self.thumbnail.params['paths']['light']
        myFile = self.line_lights.text()
        myPath = Paths(myFile)
        myPath.setparams(param)

        print param

    def set_resolution(self):
        self.thumbnail.params['universe']['options']['resolution'] = self.box_resolution.value()

    def set_quality(self):
        self.thumbnail.params['universe']['options']['quality'] = self.box_sample.value()

    def set_fov(self):
        self.thumbnail.params['universe']['camera']['fov'] = self.box_fov.value()

    def set_azimuth(self):
        self.thumbnail.params['universe']['camera']['azimuth'] = self.box_azimuth.value()

    def set_zenith(self):
        self.thumbnail.params['universe']['camera']['zenith'] = self.box_zenith.value()

    def set_position(self):
        self.thumbnail.params['universe']['camera']['position'] = self.box_position.value()

    def set_overscan(self):
        self.thumbnail.params['universe']['camera']['overscan'] = self.box_overscan.value()


if __name__ == "__main__":
    MyWindow = MainWindow()



# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sampleparamdlg.ui'
#
# Created: Sat Feb 25 15:11:59 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SampleParamDlg(object):
    def setupUi(self, SampleParamDlg):
        SampleParamDlg.setObjectName(_fromUtf8("SampleParamDlg"))
        SampleParamDlg.resize(352, 214)
        self.layoutWidget = QtGui.QWidget(SampleParamDlg)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 10, 306, 196))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.samplenameEdit = QtGui.QLineEdit(self.layoutWidget)
        self.samplenameEdit.setObjectName(_fromUtf8("samplenameEdit"))
        self.gridLayout.addWidget(self.samplenameEdit, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.areaDoubleSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.areaDoubleSpinBox.setMinimum(0.01)
        self.areaDoubleSpinBox.setMaximum(100.0)
        self.areaDoubleSpinBox.setSingleStep(0.01)
        self.areaDoubleSpinBox.setProperty("value", 0.25)
        self.areaDoubleSpinBox.setObjectName(_fromUtf8("areaDoubleSpinBox"))
        self.gridLayout.addWidget(self.areaDoubleSpinBox, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.irradianceSpinBox = QtGui.QSpinBox(self.layoutWidget)
        self.irradianceSpinBox.setMaximum(200)
        self.irradianceSpinBox.setProperty("value", 100)
        self.irradianceSpinBox.setObjectName(_fromUtf8("irradianceSpinBox"))
        self.gridLayout.addWidget(self.irradianceSpinBox, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.closeButton = QtGui.QPushButton(self.layoutWidget)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.label.setBuddy(self.samplenameEdit)
        self.label_2.setBuddy(self.areaDoubleSpinBox)
        self.label_4.setBuddy(self.irradianceSpinBox)

        self.retranslateUi(SampleParamDlg)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), SampleParamDlg.close)
        QtCore.QMetaObject.connectSlotsByName(SampleParamDlg)

    def retranslateUi(self, SampleParamDlg):
        SampleParamDlg.setWindowTitle(QtGui.QApplication.translate("SampleParamDlg", "Sample parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SampleParamDlg", "Sample name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SampleParamDlg", "Sample area (cm<sup>2</sup>)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("SampleParamDlg", "Irradiance (mW/cm<sup>2</sup>)", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("SampleParamDlg", "&Close", None, QtGui.QApplication.UnicodeUTF8))


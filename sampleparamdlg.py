#!/usr/bin/env python
# Copyright (c) 2012 Julio C. Rimada. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.


from PyQt4.QtCore import (QDate, Qt, SIGNAL, pyqtSignature)

try:
	from PyQt4.QtCore import QString
except ImportError:
	# we are using Python3 so QString is not defined
	QString = str  
	
from PyQt4.QtGui import (QApplication, QDialog, QDialogButtonBox,
        QGridLayout, QLabel, QSpinBox, QDoubleSpinBox)
import ui_sampleparamdlg


class SampleParamDlg(QDialog, ui_sampleparamdlg.Ui_SampleParamDlg):

    def __init__(self, sampleparam = ['',0.,100], parent = None):
        super(SampleParamDlg, self).__init__(parent)
        self.setupUi(self)
		
        self.paramset=['',0.,0]
        if sampleparam[1] is not None:
            self.samplenameEdit.setText(sampleparam[0])
        else:
            self.samplenameEdit.setFocus()
        self.areaDoubleSpinBox.setValue(sampleparam[1])
        self.irradianceSpinBox.setValue(sampleparam[2])
        self.on_samplenameEdit_textEdited(QString())
        self.connect(self.closeButton, SIGNAL("clicked()"), self.close)
		
    @pyqtSignature("QString")
    def on_samplenameEdit_textEdited(self, text):
        self.closeButton.setEnabled(self.samplenameEdit.text() != "")
    
    def closeEvent(self, event):
        self.paramset[0] = self.samplenameEdit.text()
        self.paramset[1] = self.areaDoubleSpinBox.value()
        self.paramset[2] = self.irradianceSpinBox.value()
#       self.reject()
     


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = SampleParamDlg()
    form.show()
    app.exec_()


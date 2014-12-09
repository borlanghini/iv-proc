#!/usr/bin/env python
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

import sys
from PyQt4.QtCore import (Qt, SIGNAL, SLOT)
from PyQt4.QtGui import (QApplication, QComboBox, QDialog,
        QGridLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox,
        QVBoxLayout, QDialogButtonBox)

class PltTypeDlg(QDialog):
    def __init__(self, parent=None):        
        super(PltTypeDlg, self).__init__(parent)
        
        pltLabel = QLabel("&Select plot type:")
        self.pltComboBox = QComboBox()
        pltLabel.setBuddy(self.pltComboBox)
        self.pltComboBox.addItems(["", "Dark", "Illuminated"])
        
        pltbuttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        pltbuttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        
        layout = QGridLayout()
        layout.addWidget(pltLabel, 0, 0)
        layout.addWidget(self.pltComboBox,  0,  1)
        layout.addWidget(pltbuttonBox,  1,  0, 1,  2)
        
        self.connect(pltbuttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(pltbuttonBox, SIGNAL("rejected()"), self, SLOT("reject()"))
        
        self.setWindowTitle("I-V proc - Plot type")
    
    def accept(self):
        plttype = unicode(self.pltComboBoxcurrentText())
        try:
            if plttype is None:
                raise TypeError,  ("You must select between Dark or Illuminated plot")
        except TypeError,  e:
            QMessageBox.warning(self, "Selection Error", unicode(e))
            return
        selt.plottype = plttype
                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = PltTypeDlg()
    form.show()
    app.exec_()

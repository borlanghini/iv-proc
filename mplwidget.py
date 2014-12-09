#!/usr/bin/env python

# Python Qt4 bindings for GUI objects
from PyQt4 import QtGui

# import the Qt4Agg FigureCanvas object, that binds Figure to
# Qt4Agg backend. It also inherits from QWidget
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

# Matplotlib Figure object
import matplotlib.pyplot as plt
#from pylab import *
#from matplotlib.ticker import MultipleLocator, FormatStrFormatter
#from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    """Class to represent the FigureCanvas widget"""
    def __init__(self):
        # setup Matplotlib Figure and Axis
        #majorFormatter = FormatStrFormatter('%1.2f')
        #majorLocator   = MultipleLocator(20)
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylabel('Current (A)',  fontsize=16)
        self.ax.set_xlabel('Voltage(V)',  fontsize=16)
        self.ax.set_title('Illuminated I-V')
        #self.ax.ticker.xaxis_set_major_formatter(majorFormatter)
        # initialization of the canvas
        FigureCanvas.__init__(self, self.fig)
        # set specific limits for X and Y axes
        self.ax.set_xlim(xmin=-0.1)
        self.ax.set_ylim(ymax=1e-6)
        # and disable figure-wide autoscale
        self.ax.grid(True)
        
        # we define the widget as expandable
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        # notify the system of updated policy
        FigureCanvas.updateGeometry(self)


class MplWidget(QtGui.QWidget):
    """Widget defined in Qt Designer"""
    def __init__(self, parent = None):
        # initialization of Qt MainWindow widget
        QtGui.QWidget.__init__(self, parent)
        # set the canvas to the Matplotlib widget
        self.canvas = MplCanvas()
        # create a vertical box layout
        self.vbl = QtGui.QVBoxLayout()
        # add mpl widget to the vertical box
        self.vbl.addWidget(self.canvas)
        # set the layout to the vertical box
        self.setLayout(self.vbl)

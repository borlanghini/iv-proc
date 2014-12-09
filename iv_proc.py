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
#
#Bibliography:
#Mark Lutz, Learning Python(3rd edition), O'Reilly Media, Sebastopol, CA 95472 (2008) ISBN-13: 978-0-596-51398-6
#Mark Summerfield, Rapid GUI Programming with Python and Qt: the Definitive Guide to PyQt Programming, Prentice Hall (2007) ISBN-13: 978-0132354189
#Sandro Tosi, Matplotlib for Python Developers, Packt Publishing Ltd. Birmingham, B27 6PA, UK (2009) ISBN 978-1-847197-90-0
#http://www.scipy.org/

import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
	from PyQt4.QtCore import QString
except ImportError:
	# we are using Python3 so QString is not defined
	QString = str  

import numpy as np
from mplwidget import MplWidget
# import the NavigationToolbar Qt4Agg widget
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
#import scipy
from scipy import interpolate,  stats
import helpform
import sampleparamdlg
import qrc_resources3



__version__ = "1.2"


class MainWindow(QMainWindow):
    NextId = 1
    Instances = set()
    
    def __init__(self, filename=str(),  parent=None):
        super(MainWindow, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        MainWindow.Instances.add(self)
        
#        create the layout 
        self.table = QTableWidget()
         # instantiate a widget, it will be the main one
        self.graph_widget = QWidget()
        # create a vertical box layout widget
        graph_layout = QVBoxLayout(self.graph_widget)
        # instantiate our Matplotlib canvas widget
        self.plotiv = MplWidget()
        # instantiate the navigation toolbar
        self.navtoolbar = NavigationToolbar(self.plotiv.canvas, self.graph_widget)
        # pack these widget into the vertical box
        graph_layout.addWidget(self.plotiv)
        graph_layout.addWidget(self.navtoolbar)
        self.ivSplitter = QSplitter(Qt.Horizontal)
        self.ivSplitter.addWidget(self.table)
        self.ivSplitter.addWidget(self.graph_widget)
        self.setCentralWidget(self.ivSplitter)
        
#        main variables
        self.dirty = False
        self.setparam = False
        self.calculated = False
        self.filename = None
        self.loadedfile = False
        self.sampleparameters = ['', 0,100]
        self.calcparameters = [0, 0,  0,  0, 0, 0,  0] # [isc,  voc,  fillfactor,  maxscpower,  effic, rshunt,  rseries]
        self.normalArray = []
        self.ivdata = np.zeros((0, 2))
        self.plottype = 'None'
        self.isDark = None
        self.lastfile = ''

        self.printer = None

        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen",
                "Open an I-V data file")
        fileSaveAction = self.createAction("&Save", self.fileSave,
                QKeySequence.Save, "filesave", "Save results file")

        filePrintAction = self.createAction("&Print", self.filePrint,
                QKeySequence.Print, "fileprint", "Print the results")
        fileCloseAction = self.createAction("&Close", self.close, 
                                            QKeySequence.Close, "fileclose","Close this window")
        fileQuitAction = self.createAction("&Quit", self.close,
                                            "Ctrl+Q", "filequit", "Close the application")
                
        processGraphAction = self.createAction("Make &Graph",  self.processGraph,  "Ctrl+G",  "graph",  "Show I-V graph")
        
        processCalculateAction = self.createAction("Calculate P&arameters",  self.processCalculate,  
                "Ctrl+A",  "calculate",  "Calculate parameters from I-V data")

        helpAboutAction = self.createAction("&About this program", self.helpAbout)
        helpHelpAction = self.createAction("&Help", self.helpHelp, QKeySequence.HelpContents)

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu,  (fileOpenAction, fileSaveAction, None, fileCloseAction,
                fileQuitAction))
        
        processMenu = self.menuBar().addMenu("&Process")
        self.addActions(processMenu,  (processGraphAction,  processCalculateAction))
        #mirrorMenu = processMenu.addMenu(QIcon(":/editmirror.png"), "&Mirror")
        
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.connect(self.windowMenu, SIGNAL("aboutToShow()"), self.updateWindowMenu)

        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, (helpAboutAction, helpHelpAction))
        

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileOpenAction, fileSaveAction))
        processToolbar = self.addToolBar("Process")
        processToolbar.setObjectName("ProcessToolBar")
        self.addActions(processToolbar,  (processGraphAction,  processCalculateAction))
#        darkIvGraphModeToolbar = self.addToolbar("")

        self.connect(self, SIGNAL("destroyed(QObject*)"), MainWindow.updateInstances)
        
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)
        
        self.filename = filename
        if self.filename == "":
            self.filename = str("Unnamed-{0}".format(MainWindow.NextId))
            MainWindow.NextId += 1
            self.loadedfile = False
            self.setWindowTitle("Solar Cell I-V processing - {0}".format(self.filename))
        else:
            self.loadFile()
            
        settings = QSettings()
        #self.recentFiles = settings.value("RecentFiles").toStringList()
        if len(sys.argv) > 1:
            self.loadFiles()
#            self.updateFileMenu()


    @staticmethod
    def updateInstances(qobj):
        MainWindow.Instances = (set([window for window in MainWindow.Instances if isAlive(window)]))

    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


    def closeEvent(self, event):
         if (self.dirty and
            QMessageBox.question(self,
                "I-V Processing - Unsaved Changes",
                "Save unsaved changes in {0}?".format(self.filename),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.Yes):
            self.fileSave()
       


    def okToContinue(self):
        if self.dirty:
            reply = QMessageBox.question(self,
                    "I-V processing - Unsaved Changes",
                    "Save unsaved changes?",
                    QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave()
        return True


    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)
#        self.listWidget.addItem(message)
        if self.filename is not None:
            self.setWindowTitle("I-V processing - {0}[*]".format(
                                os.path.basename(self.filename)))
        elif not self.loadedfile:
            self.setWindowTitle("I-V processing - Unnamed[*]")
        else:
            self.setWindowTitle("I-V processing[*]")
        self.setWindowModified(self.dirty)


    def fileOpen(self):
        dir = (os.path.dirname(self.lastfile)
               if self.filename is not None else ".")
        filename = QFileDialog.getOpenFileName(self, "Choose an Illuminated I-V data file", dir,
        "Text files(*.txt);;Data files(*.dat);;CSV files(*.csv);;IVK files(*.ivk);;All files(*.*)")
        if not filename == "":
            if (not self.loadedfile):
                self.filename = filename
                self.loadFile()
                self.lastfile = self.filename
            else:
                MainWindow(filename).show()
#            msg = self.loadFile(fname)
    
    def loadFile(self):
        ok, msg = self.loadData()
        self.table.show()
        self.initGraph()
#        self.addRecentFile(fname)
        self.updateTable()
#        self.filename = fname
#        settings = QSettings()
#        settings.setValue("LastFile", fname)
        self.loadedfile = True
        self.updateGraph()
        self.updateStatus(msg)

    def loadData(self):
        error = None
        fh = None
        self.ivdata=np.zeros((0, 2))
        try:
            fh = open(self.filename,  "r")
            for line in fh:
                if not line or line.startswith(("#", "\n", "\r")):
                    continue
                line = line.rstrip()
                fields = line.split("\t")
                self.ivdata = np.append(self.ivdata,  [[float(fields[0]), float(fields[1])]],  axis=0)
                
        except Exception:
            return "Failed to load file"
        finally:
            return True,  "File successfully loaded"


    def loadFiles(self):
        for filename in sys.argv[1:5]:
            filename = QString(filename)
            if QFileInfo(filename).isFile():
                self.filename = filename
                self.loadFile()
                

    def addRecentFile(self, fname):
        if fname is None:
            return
        if not self.recentFiles.contains(fname):
            self.recentFiles.prepend(QString(fname))
            while self.recentFiles.count() > 9:
                self.recentFiles.takeLast()


    def fileSave(self):
        if not self.dirty:
            return True
        filetypes = self.plotiv.canvas.get_supported_filetypes_grouped()
        sorted_filetypes = filetypes.items()
        sorted_filetypes.sort()
        default_filetype = self.plotiv.canvas.get_default_filetype()
        start = self.sampleparameters[0] + default_filetype
        filters = []
        selectedFilter = None
        for name, exts in sorted_filetypes:
            exts_list = " ".join(['*.%s' % ext for ext in exts])
            filter = '%s (%s)' % (name, exts_list)
            if default_filetype in exts:
                selectedFilter = filter
            filters.append(filter)
        filters = ';;'.join(filters)
        
        self.navtoolbar.save_figure()
        self.dirty = False
    

    def fileSaveAs(self):
        if not self.dirty:
            return True
        fname = self.filename if self.filename is not None else "."
        formats = (["*.{0}".format(format.lower())
                for format in QImageWriter.supportedImageFormats()])
        fname = QFileDialog.getSaveFileName(self,
                "Solar Cell I-V processing - Save Graph Image", fname,
                "Image files ({0})".format(" ".join(formats)))
        if fname:
            if "." not in fname:
                fname += ".png"
            self.addRecentFile(fname)
            self.filename = fname
            return self.fileSave()
        return False

    def updateWindowMenu(self):
        self.windowMenu.clear()
        for window in MainWindow.Instances:
            if isAlive(window):
                action = self.windowMenu.addAction(
                        window.windowTitle().mid(
                                len("Solar Cell I-V processing - ")),
                                self.raiseWindow)
                action.setData(QVariant(long(id(window))))
    
    def raiseWindow(self):
        action = self.sender()
        if not isinstance(action, QAction):
            return
        windowId = action.data().toLongLong()[0]
        for window in MainWindow.Instances:
            if isAlive(window) and id(window) == windowId:
                window.activateWindow()
                window.raise_()
                break

    def filePrint(self):
        if self.image.isNull():
            return
        if self.printer is None:
            self.printer = QPrinter(QPrinter.HighResolution)
            self.printer.setPageSize(QPrinter.Letter)
        form = QPrintDialog(self.printer, self)
        if form.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(),
                                size.height())
            painter.drawImage(0, 0, self.image)

    def helpAbout(self):
        QMessageBox.about(self, "I-V processing",
                """<b>Solar Cell I-V processing</b> v {0}
                <p>Copyright &copy; 2012 Borlanghini  
                All rights reserved.
                <p>This application can be used to process illuminated I-V
                    measured data in order to obtain the main parameters from the device .
                <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR,
                platform.system()))


    def helpHelp(self):
        form = helpform.HelpForm("index.html", self)
        form.show()

    def updateTable(self, current=None):
        self.table.clear()
        self.table.setRowCount(len(self.ivdata))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Voltage (V)", "Current (A)"])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        selected = None
        for i, row in enumerate(self.ivdata.tolist()):
            for j,  col in enumerate(row):
                item = QTableWidgetItem(str(col))
                item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                self.table.setItem(i,  j,  item)
        self.table.resizeColumnsToContents()
        if selected is not None:
            selected.setSelected(True)
            self.table.setCurrentItem(selected)
            self.table.scrollToItem(selected)
            
    def processGraph(self):
        self.updateGraph()


    def initGraph(self):
        self.calculated = False
        jsc = ''
        voc = ''
        maxpower = ''
        fillfactor = ''
        effic = ''
        graphtitle = "Iluminated IV\nSample: "
        self.plotiv.canvas.ax.clear()
        self.plotiv.canvas.ax.grid(True)
        self.plotiv.canvas.ax.set_ylabel('Current (A)',  fontsize=16)
        self.plotiv.canvas.ax.set_xlabel('Voltage(V)',  fontsize=16)
        self.plotiv.canvas.draw()


    def updateGraph(self):
        if self.calculated:
            isc = " %.2f " % (self.calcparameters[0]*1000)
            jsc = " %.2f " % (self.calcparameters[0]*1000/ self.sampleparameters[1])
            voc = " %.2f " % (self.calcparameters[1]*1000)
            maxpower = " %.2f " %(self.calcparameters[3]*1000)
            fillfactor = " %.2f "%(self.calcparameters[2])
            effic = " %.2f "%(self.calcparameters[4]*100)
            rshunt = " %.2f "%(self.calcparameters[5])
            rseries = " %.2f "%(self.calcparameters[6])
        else:
            jsc = ''
            voc = ''
            maxpower = ''
            fillfactor = ''
            effic = ''
        if self.setparam:
            area = " %.2f " %(self.sampleparameters[1])
            irrad = " %.2f " %(self.sampleparameters[2])
        else:
            area = ''
            irrad = ''
            
        graphtitle = "Iluminated IV\nSample: "+ self.sampleparameters[0]
        self.plotiv.canvas.ax.clear()        
        self.plotiv.canvas.ax.grid(True)
        self.plotiv.canvas.ax.set_ylabel('Current (A)',  fontsize=16)
        self.plotiv.canvas.ax.set_xlabel('Voltage(V)',  fontsize=16)
        self.plotiv.canvas.ax.set_title(graphtitle,  fontsize=16)
        if self.isDark is None:
            if not self.calculated:
                xmin= np.amin(self.ivdata[:, 0])
                xmax=np.amax(self.ivdata[:, 0])
                ymin=np.amin(self.ivdata[:, 1])
                ymax=np.amax(self.ivdata[:, 1])
                self.plotiv.canvas.ax.set_xlim(xmin=xmin,  xmax=xmax)
                
                if abs(np.amin(self.ivdata[:, 1]))<0.5:
                    self.plotiv.canvas.ax.set_ylabel('Current (mA)',  fontsize=16)
                    self.plotiv.canvas.ax.set_ylim(ymin=ymin*1000,  ymax=ymax*1000)
                    self.plotiv.canvas.ax.plot(self.ivdata[:,0], self.ivdata[:,1]*1000, color='b', linestyle ='dashed', marker='o', lw=1.5, zorder=1)
                else:
                    self.plotiv.canvas.ax.set_ylim(ymin=ymin,  ymax=ymax)
                    self.plotiv.canvas.ax.plot(self.ivdata[:,0], self.ivdata[:,1], color='b', linestyle ='dashed', marker='o', lw=1.5, zorder=1)
            if self.calculated:
                if abs(self.calcparameters[0])<0.5:
                    self.plotiv.canvas.ax.set_ylabel('Current (mA)',  fontsize=16)
                    ymin = self.calcparameters[0]*1000
                    self.plotiv.canvas.ax.plot(self.ivdata[:,0], self.ivdata[:,1]*1000, color='b', linestyle ='dashed', marker='o', lw=1.5, zorder=1)
                else:
                    ymin = self.calcparameters[0]
                    self.plotiv.canvas.ax.plot(self.ivdata[:,0], self.ivdata[:,1], color='b', linestyle ='dashed', marker='o', lw=1.5, zorder=1)
                self.plotiv.canvas.ax.set_xlim(xmin= -0.01,  xmax= self.calcparameters[1]+ self.calcparameters[1]*0.1)
                self.plotiv.canvas.ax.set_ylim(ymin=ymin-abs(ymin*0.1),  ymax=abs(ymin*0.1))
                self.plotiv.canvas.ax.text(0.05, 0.95, r'Cell area $=$' +area+' $cm^{2}$',  fontsize = 14,  transform = self.plotiv.canvas.ax.transAxes)
                self.plotiv.canvas.ax.text(0.05, 0.87, r'$I_{SC} = $' + isc + ' $mA \quad J_{SC} = $' +jsc +' $mA/cm^{2}$',  fontsize = 14,  transform = self.plotiv.canvas.ax.transAxes)
                self.plotiv.canvas.ax.text(0.05, 0.80, r'$V_{OC} = $'+voc+' $mV$',  fontsize = 14,  transform = self.plotiv.canvas.ax.transAxes)
                self.plotiv.canvas.ax.text(0.05, 0.73, r'$FF = $'+fillfactor,  fontsize = 14,  transform = self.plotiv.canvas.ax.transAxes)
                self.plotiv.canvas.ax.text(0.05, 0.66, r'$P_{MAX} = $'+maxpower+' $mW$',  fontsize = 14,  transform = self.plotiv.canvas.ax.transAxes)
                self.plotiv.canvas.ax.text(0.05, 0.59, r'$\eta = $'+effic+' $\%$',  fontsize = 14,  transform = self.plotiv.canvas.ax.transAxes)
                self.plotiv.canvas.ax.text(0.05, 0.52, r'$R_{Shunt} \sim $' +rshunt+'$ \Omega$',  fontsize = 14,  transform = self.plotiv.canvas.ax.transAxes)
                self.plotiv.canvas.ax.text(0.05, 0.45, r'$R_{Series} \sim $' +rseries+'$ \Omega$',  fontsize = 14,  transform = self.plotiv.canvas.ax.transAxes)
        self.plotiv.canvas.draw()
        
    
    def processCalculate(self):
        form = sampleparamdlg.SampleParamDlg(self.sampleparameters, None)
        form.show()
        form.exec_()
        self.sampleparameters = form.paramset
        self.setparam = True
        self.calcparameters = self.findscparam()
        self.calculated = True
        self.dirty = True
        self.updateGraph()


    def findscparam(self):
        if  not self.setparam:
            return
        if self.ivdata[:, 0][0]>self.ivdata[:, 0][1]:
            volt = np.flipud(self.ivdata[:, 0])
            curr = np.flipud(self.ivdata[:, 1])
        else:
            volt = self.ivdata[:, 0]
            curr = self.ivdata[:, 1]
#        finding last data position before zero crossing
        zero_crossing=np.where(np.diff(np.sign(curr)))[0][0]
#        creating function for data interpolation
        data_interpld = interpolate.interp1d(volt, curr,  kind='cubic')
#        approximate Voc value by linear interpolation
        slope = (curr[zero_crossing +1] - curr[zero_crossing])/(volt[zero_crossing + 1]-volt[zero_crossing])
        intercept = curr[zero_crossing] - slope*volt[zero_crossing]
#        slope,  intercept,  r_value,  p_value,  std_err = stats.linregress(volt[zero_crossing:zero_crossing+1],  curr[zero_crossing:zero_crossing+1])
        voc = - intercept/slope
        isc = data_interpld(0)
#        finding max power point
        voltnew = np.arange(0, volt[zero_crossing+1],  0.001)
        maxscpower = max(np.abs(np.multiply(voltnew,  data_interpld(voltnew))))
        maxscpower_voltposition = np.argmax(np.abs(np.multiply(voltnew, data_interpld(voltnew))))
        fillfactor = np.abs(maxscpower/(voc*isc))
        effic = maxscpower*1000/(self.sampleparameters[2]*self.sampleparameters[1])
#        finding r_s and r_shunt graphically --- approximate method
        rsh_slope,  intercept,  r_value,  p_value,  std_err = stats.linregress(voltnew[0:int(maxscpower_voltposition*0.8)], data_interpld(voltnew[0:int(maxscpower_voltposition*0.8)]))
        rshunt = np.abs(1/rsh_slope)
        rs_slope,  intercept,  r_value,  p_value,  std_err = stats.linregress(voltnew[-50:-1], data_interpld(voltnew[-50:-1]))
        rseries = np.abs(1/rs_slope)
        return [isc,  voc,  fillfactor,  maxscpower,  effic, rshunt,  rseries]


def isAlive(qobj):
    import sip
    try:
        sip.unwrapinstance(qobj)
    except RuntimeError:
        return False
    return True


app = QApplication(sys.argv)
app.setOrganizationName("Borlanghini.")
app.setOrganizationDomain("http://imre.oc.uh.cu/")
app.setApplicationName("Solar Cell I-V processing")
app.setWindowIcon(QIcon(":/icon.png"))
MainWindow().show()
app.exec_()



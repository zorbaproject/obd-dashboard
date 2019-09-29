#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Pyside2 dashboard example
# by Luca Tringali
# 
# Using Python-OBD (https://github.com/brendan-w/python-OBD)
# We are actually using a slightly modified version, because the original does not work with cheap bluetooth adapters

#You will need to run this with sudo, if your user is not in the dialout group



import obd
import sys, os
import os.path
from time import sleep

try:
    from PySide2.QtWidgets import QApplication
except:
    try:
        from tkinter import messagebox
        messagebox.showinfo("Install", "I'm going to install PySide2, it might take some time. Go get a coffee. Maybe some cookies too.")
        pip.main(["install", "PySide2"])
        from PySide2.QtWidgets import QApplication
    except:
        try:
            from pip._internal import main
            main(["install", "PySide2"])
            from PySide2.QtWidgets import QApplication
        except:
            sys.exit(1)


from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtCore import Qt
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QThread
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QPainter


toSleep = 1



class ShowData(QThread):
    TempReached = Signal(bool)

    def __init__(self, w, s0, c0, s1, c1, s2, c2):
        QThread.__init__(self)
        self.w = w
        self.setTerminationEnabled(True)
        self.serie0 = s0
        self.serie1 = s1
        self.serie2 = s2
        self.chart0 = c0
        self.chart1 = c1
        self.chart2 = c2
        self.i = 0
        if self.w.autoConnect.isChecked():
            self.connectCommands()
        self.connection = obd.OBD(fast=False, timeout=30) # auto-connects to USB or RF port
        #self.connection = obd.OBD("/dev/rfcomm0")

    def __del__(self):
        print("Shutting down thread")

    def connectCommands(self):
        guisudo = "/usr/lib/x86_64-linux-gnu/libexec/kf5/kdesu"
        if not os.path.isfile(guisudo):
            guisudo = "/usr/lib/arm-linux-gnueabihf/libexec/kf5/kdesu"
        os.system(guisudo+" -c '/bin/sh "+os.path.abspath(os.path.dirname(sys.argv[0]))+"/connect.sh'")


    def run(self):
        global toSleep
        while True:
            try:
                if self.w.SwitchOn.isChecked():
                    self.first()
                    self.second()
                    self.third()
                    self.i = self.i +1
                #else:
                    #self.TempReached.emit(True)
                    #break
            except:
                #self.TempReached.emit(False)
                #break
                print("Error reading OBD")
            sleep(toSleep)
        return
    
    def first(self):
        cmd = obd.commands.SPEED
        response = self.connection.query(cmd)
        #sdata = str(format(response.value.to("kph")))
        sdata = str(response.value.__str__())
        ndata = float(sdata.split(" ")[0])
        self.serie0.append(self.i, ndata)
        self.chart0.removeSeries(self.serie0)
        self.chart0.addSeries(self.serie0)
        self.chart0.createDefaultAxes()
        self.w.data_0.setText(str(ndata)+" km/h")
    
    def second(self):
        cmd = obd.commands.RPM
        response = self.connection.query(cmd)
        sdata = str(response.value.__str__())
        ndata = float(sdata.split(" ")[0])
        self.serie1.append(self.i, ndata)
        self.chart1.removeSeries(self.serie1)
        self.chart1.addSeries(self.serie1)
        self.chart1.createDefaultAxes()
        self.w.data_1.setText(str(ndata).split(".")[0]+" rpm")
        
    def third(self):
        cmd = obd.commands.ACCELERATOR_POS_D
        response = self.connection.query(cmd)
        sdata = str(response.value.__str__())
        ndata = float(sdata.split(" ")[0])
        self.serie2.append(self.i, ndata)
        self.chart2.removeSeries(self.serie2)
        self.chart2.addSeries(self.serie2)
        self.chart2.createDefaultAxes()
        self.w.data_2.setText(str(ndata).split(".")[0]+" %")


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        file = QFile(os.path.abspath(os.path.dirname(sys.argv[0]))+"/dashboard.ui")
        file.open(QFile.ReadOnly)
        loader = QUiLoader(self)
        self.w = loader.load(file)
        self.setCentralWidget(self.w)
        self.setWindowTitle("Dashboard")
        self.w.SwitchOn.clicked.connect(self.StopThis)
        self.w.SwitchOn.setChecked(False)
        self.w.SwitchOn.setText("On")
        self.alreadyOn = False
        
        # Creating QChart
        self.w.label_0.setText("Speed")
        self.chart0 = QtCharts.QChart()
        #self.chart0.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        self.serie0 = QtCharts.QLineSeries(self.chart0)
        self.chart0.addSeries(self.serie0)
        self.chart0.createDefaultAxes()
        self.chart_view0 = QtCharts.QChartView(self.chart0)
        self.chart_view0.setRenderHint(QPainter.Antialiasing)
        self.w.verticalLayout_0.addWidget(self.chart_view0)
        
        # Creating QChart
        self.w.label_1.setText("RPM")
        self.chart1 = QtCharts.QChart()
        #self.chart1.setAnimationOptions(QtCharts.QChart.AllAnimations)
        self.serie1 = QtCharts.QLineSeries(self.chart1)
        self.chart1.addSeries(self.serie1)
        self.chart1.createDefaultAxes()
        self.chart_view1 = QtCharts.QChartView(self.chart1)
        self.chart_view1.setRenderHint(QPainter.Antialiasing)
        self.w.verticalLayout_1.addWidget(self.chart_view1)
        
        # Creating QChart
        self.w.label_2.setText("Throttle")
        self.chart2 = QtCharts.QChart()
        #self.chart2.setAnimationOptions(QtCharts.QChart.AllAnimations)
        self.serie2 = QtCharts.QLineSeries(self.chart2)
        self.chart2.addSeries(self.serie2)
        self.chart2.createDefaultAxes()
        self.chart_view2 = QtCharts.QChartView(self.chart2)
        self.chart_view2.setRenderHint(QPainter.Antialiasing)
        self.w.verticalLayout_2.addWidget(self.chart_view2)
        
    def itIsOff(self):
        self.w.SwitchOn.setChecked(False)
        self.StopThis()
        
    def reached(self):
        if self.stoponreached:
            self.itIsOff()
        
    def dostuff(self):
        if not self.alreadyOn:
            self.getTempThread = ShowData(self.w, self.serie0, self.chart0, self.serie1, self.chart1, self.serie2, self.chart2)
            self.getTempThread.finished.connect(self.itIsOff)
            self.getTempThread.start()
            self.alreadyOn = True
            
    def StopThis(self):
        if self.w.SwitchOn.isChecked():
            self.w.SwitchOn.setText("Off")
            self.dostuff()
        else:
            self.w.SwitchOn.setText("On")
            #self.alreadyOn = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setFixedSize(640,480)
    w.show()
    sys.exit(app.exec_())

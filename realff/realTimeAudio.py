import ui_plot
import sys
import numpy
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from recorder import *



def plotSomething():
    if SB.newAudio==False: 
        return
    xs,ys=SB.fft()
    c.setData(xs,ys)
    uiplot.qwtPlot.replot()
    SB.newAudio=False

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    
    win_plot = ui_plot.QtGui.QMainWindow()
    uiplot = ui_plot.Ui_win_plot()
    uiplot.setupUi(win_plot)
    c=Qwt.QwtPlotCurve()  
    c.attach(uiplot.qwtPlot)
    
    uiplot.qwtPlot.setAxisScale(uiplot.qwtPlot.yLeft, 0, 3)
    
    uiplot.timer = QtCore.QTimer()
    uiplot.timer.start(1.0)
    
    win_plot.connect(uiplot.timer, QtCore.SIGNAL('timeout()'), plotSomething) 
    
    SB=Recorder()
    SB.setup()
    SB.continuousStart()

    ### DISPLAY WINDOWS
    win_plot.show()
    code=app.exec_()
    SB.close()
    sys.exit(code)

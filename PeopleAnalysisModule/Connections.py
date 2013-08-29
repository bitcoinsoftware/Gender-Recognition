from Functions import *
from PyQt4 import QtCore, QtGui
class Connections(Functions):
    def connect(self):
        print "connect"
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL('clicked()'),self.turn_camera_on)
        #QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL('clicked()'),self.check_results_permanently)
        QtCore.QObject.connect(self.pushButton_4,QtCore.SIGNAL('clicked()'),self.turn_camera_off)
        QtCore.QObject.connect(self.pushButton_3,QtCore.SIGNAL('clicked()'),self.run_data_analysis_module)
        QtCore.QObject.connect(self.checkBox_4,QtCore.SIGNAL('stateChanged(int)'),self.set_new_person_treshold)
        
        
        

#---------------------------------importing libraries-----------------------------------------------------------------------------------------

import os
import sys
import rx
from rx.scheduler.mainloop import QtScheduler
from rx.subject import Subject
import rx.operators as ops
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
# from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication, QLabel,QWidget

# --------------------------------Defining length of buffer (timeout) to distinguish between single and double click-----------------------------

TIME = 1 #in seconds
#-------------------------Creating class MouseEvent ------------------------------------------------------------------------------------------------------

class MouseEvent(QWidget):

    def __init__(self,parent = None):
        QWidget.__init__(self)

#-----Providing Title-----------------------------------------------------------------------------------------------------------------------

        self.setWindowTitle("Distinguish Single and Double Clicks M20CS020")
        self.setFixedSize(QSize(800, 800))

#-----Display text inside the window----------------------------------------------------------------------------------------------------------

        self.label = QLabel('Click anywhere inside this window to distinguish whether it is single or double click and check the result in command prompt.', self)

#-------Setting some styles-----------------------------------------------------------------------------------------------------------------

        self.label.setStyleSheet("background-color: pink; border: 1px solid red;padding :5px; color:red")
        self.label.move(30, 350)

#---------Creating reactive environment------------------------------------------------------------------------------------------------------

        self.checkmouse = Subject()

#----------Overriding mousePressEvent and mouseReleaseEvent----------------------------------------------------------------------------------

    def mousePressEvent(self, event):
        self.checkmouse.on_next((event.pos(), 1))
    def mouseReleaseEvent(self, event):
       self.checkmouse.on_next((event.pos(), 2))

#---------Funstion to detect whether the click is single click or double click--------------------------------------------------------------

def determineClick(data):
    length_data=len(data)
    if (length_data==2):
        print('Single click detected')
    elif (length_data>2):
        print('Double click detected')




#----------------Use main for calling function-------------------------------------------------------------------------------------------------

if __name__ == '__main__':
# start_event()
    application = QApplication(sys.argv)
#-----------creating a scheduler for event loop--------------------------------------------------------------------------------------------
    scheduling_ = QtScheduler(QtCore)
#----------measuring time between events--------------------------------------------------------------------------------------------------
    time_calculation = ops.time_interval(scheduling_)
#----------determine timing information---------------------------------------------------------------------------------------------------
    timing_info = ops.buffer_with_time(TIME)
    mapper = ops.map(determineClick)
    window_ = MouseEvent("800x800")
#----------show/display window------------------------------------------------------------------------------------------------------------
    window_.show()
    
    window_.checkmouse.pipe(time_calculation, timing_info, mapper).subscribe(
        on_next=(lambda x: x), scheduler=scheduling_
        )
#----------end the main loop of the application-----------------------------------------------------------------------------------
    sys.exit(application.exec_())
  

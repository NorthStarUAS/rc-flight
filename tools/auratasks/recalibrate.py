from PyQt4 import QtGui, QtCore
import subprocess

from combobox_nowheel import QComboBoxNoWheel
import fgtelnet

class Recalibrate():
    def __init__(self, changefunc, host="localhost", port=6499):
        self.changefunc = changefunc
        self.host = host
        self.port = port
        self.original_values = []
        self.container = self.make_page()
        self.xml = None

    def onChange(self):
        self.changefunc()

    def make_page(self):
        toppage = QtGui.QFrame()
        toplayout = QtGui.QVBoxLayout()
        toppage.setLayout(toplayout)

        # 'Command' button bar
        cmd_group = QtGui.QFrame()
        toplayout.addWidget(cmd_group)
        cmd_layout = QtGui.QHBoxLayout()
        cmd_group.setLayout( cmd_layout )
        cmd_layout.addWidget( QtGui.QLabel("<b>Commands:</b> ") )
        recalibrate = QtGui.QPushButton('Recalibrate')
        recalibrate.clicked.connect(self.task_recalibrate)
        cmd_layout.addWidget(recalibrate)
        cmd_layout.addStretch(1)

        toplayout.addStretch(1)

        # set initial values
        self.revert()

        return toppage

    def get_widget(self):
        return self.container

    def send_value(self, t, prop, val):
        if len(val):
            if self.port != 6499:
                command = "send set," + prop + "," + str(val)
                print command
                t.send(command)
            else:
                command = "set " + prop + " " + str(val)
                print command
                t.send(command)

    def update(self):
        print "update parameters"
        t = fgtelnet.FGTelnet(self.host, self.port)
        t.send("data")
        #self.send_value(t, "/task/preflight/duration_sec",
        #                self.edit_duration.text())
        t.quit()

    def revert(self):
        print str(self.original_values)
        # revert form
        #self.edit_duration.setText( self.original_values[0] )

        # send original values to remote
        self.update()

    def task_recalibrate(self):
        print "request recalibreate task"
        self.update()
        t = fgtelnet.FGTelnet(self.host, self.port)
        t.send("data")
        if self.port != 6499:
            t.send("send task,recalibrate")
        else:
            t.send("set /task/command_request task,recalibrate")
        t.quit()
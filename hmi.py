import sys
from PyQt4 import QtGui

from PyQt4.QtGui import *
from PyQt4.QtCore import *


import threading
import time
from pymodbus.client.sync import ModbusTcpClient

MODBUS_HOLDING_REGISTER = 0
MODBUS_INPUT_REGISTER = 1

BOOL = '?'
INT = 'i'
UNINT = 'I'
FLOAT = 'f'

class StoppableThread(threading.Thread):
    """Basic Stoppable Thread Wrapper
    Adds event for stopping the execution
    loop and exiting cleanly."""
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.daemon = True

    def start(self):
        if not self.isAlive():
            self.stop_event.clear()
            threading.Thread.start(self)

    def stop(self):
        if self.isAlive():
            self.stop_event.set()
            self.join()


class AsyncWorker(StoppableThread):
    """Basic thread wrapper class for asynchronously running functions
    Return False from the worker function to abort loop."""
    def __init__(self, todo):
        StoppableThread.__init__(self)
        self.todo = todo

    def run(self):
        while not self.stop_event.is_set():
            # Explicitly check for False being returned
            # from worker, IE: Don't allow None
            if self.todo() is False:
                self.stop_event.set()
                break


class AsyncModbusMaster():
    def __init__ (self, host =  "localhost", port= 502, cycle_time=1):
        self.cycle_time = cycle_time
        self.tick_count = 0
        self.async_worker = AsyncWorker(self.tick)
        self.inputs = []
        self.outputs = []
        self.host = host
        self.port = port
        #self.modbus_slave = ModbusClient()
        #self.modbus_slave.host(self.host )
        #self.modbus_slave.port(self.port)
        self.client = ModbusTcpClient(self.host, port=self.port)
        
        
        
        self.async_worker.start()

    def tick(self):
        self.tick_count += 1
        for s in self.inputs:
            if (s.changed()):
                if (s.register == MODBUS_HOLDING_REGISTER):
                    self.client.write_register(s.address, s.get())
                
                s.last_value = s.value
            for s in self.outputs:
                if (s.register == MODBUS_HOLDING_REGISTER):
                    value = self.client.read_holding_registers(s.address, 2).registers[0]
                    bit = (value >> s.bit) & 1
                    s.set (bit)
                elif (s.register == MODBUS_INPUT_REGISTER):
                    
                    value = self.client.read_input_registers(s.address, 2).registers[0]
                    bit = (value >> s.bit) & 1
                    s.set (bit)
                


        time.sleep (self.cycle_time)
    def AddInput (self, oh_state):
        self.inputs.append (oh_state)
    def AddOutput (self, oh_state):
        self.outputs.append (oh_state)

class BoolVar ():
    def __init__(self, value, address=0, parent = None):
        self.value = value
        self.last_value = value
        self.address = address
        self.register = MODBUS_HOLDING_REGISTER
        self.parent = parent
        self.format = BOOL
        self.bit = 0
    def set(self, v):
        self.last_value = self.value
        self.value = v
        if (self.parent): self.parent.update()
    def get(self):
        return self.value
    def changed (self):
        return self.value is not self.last_value

class IndicatorLight (QLabel):
    def __init__ (self, off_pixmap, on_pixmap, width, height, parent=None):
        super(IndicatorLight, self).__init__(parent)
        self.on_pixmap = on_pixmap.scaledToHeight(height, Qt.SmoothTransformation)
        self.off_pixmap = off_pixmap.scaledToHeight(height, Qt.SmoothTransformation)
        self.pixmap = self.off_pixmap
        self.setFixedSize(height,width)
        self.bool_var = BoolVar (0,parent=self)

    def paintEvent(self, event):
        if (self.bool_var.get()):
            self.pixmap = self.on_pixmap
        else:
            self.pixmap = self.off_pixmap


        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

class AnalogMeter (QLabel):
    def __init__ (self, bg_pixmap, fg_pixmap, width, height, parent=None):
        super(AnalogMeter, self).__init__(parent)
        self.bg_pixmap = bg_pixmap.scaledToHeight(height, Qt.SmoothTransformation)
        self.fg_pixmap = fg_pixmap.scaledToHeight(height, Qt.SmoothTransformation)
        self.setFixedSize(height,width)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.bg_pixmap)
        painter.drawPixmap(event.rect(), self.fg_pixmap)

class MomentarySwitch(QAbstractButton):
    def __init__(self, pixmap,  pixmap_pressed,  width, height, parent=None):
        super(MomentarySwitch, self).__init__(parent)
        self.pixmap =  pixmap.scaledToHeight(height, Qt.SmoothTransformation)
        self.pixmap_pressed =  pixmap_pressed.scaledToHeight(height, Qt.SmoothTransformation)
        #self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pressed.connect(self.down)
        self.released.connect(self.up)
        self.dwell = 0.2
        self.setFixedSize(height,width)
        self.bool_var = BoolVar(0)
    def down(self):

        self.bool_var.set(1)
        self.update()
    def up(self):
        time.sleep(self.dwell)
        self.bool_var.set(0)
        self.update()
    def paintEvent(self, event):
        pix = self.pixmap

        if self.bool_var.get():
            pix = self.pixmap_pressed


        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()


    def leaveEvent(self, event):
        self.update()


    def sizeHint(self):
        return QSize(160, 160)

def main():

    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    w.resize(600, 600)
    w.move(300, 300)
    w.setWindowTitle('Simple')



    layout = QHBoxLayout(w)
    palette = QPalette()
    palette.setBrush(QPalette.Background,QBrush(QPixmap("darkbg.png"))) # Haha, aren't I so funny??
    w.setPalette(palette)
    button = MomentarySwitch(QPixmap("images/start_button_normal.png"),QPixmap("images/start_button_down.png"),128,128)
    
    indicator2 = IndicatorLight(QPixmap("images/red_indicator_off.png"),QPixmap("images/red_indicator_on.png"),128,128)
    indicator = IndicatorLight(QPixmap("images/red_indicator_off.png"),QPixmap("images/red_indicator_on.png"),128,128)
    analog_meter = AnalogMeter(QPixmap("meter_bg.png"),QPixmap("meter_overlay.png"),250,300)
    layout.addWidget(button)

    layout.addWidget(indicator)
    layout.addWidget(indicator2)
    layout.addWidget(analog_meter)

    async_modbus = AsyncModbusMaster(cycle_time = 0.2)
    button.bool_var.address = 0
    button.bool_var.register = MODBUS_HOLDING_REGISTER
    indicator2.bool_var.address =0
    indicator2.bool_var.register = MODBUS_INPUT_REGISTER
    indicator2.bool_var.bit = 0
    indicator.bool_var.address =0
    indicator.bool_var.register = MODBUS_INPUT_REGISTER
    indicator.bool_var.bit = 1
    
    async_modbus.AddInput (button.bool_var)
    async_modbus.AddOutput (indicator.bool_var)
    async_modbus.AddOutput (indicator2.bool_var)
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# definitions
PUSH_BUTTON_WIDTH         = 75
PUSH_BUTTON_HEIGHT        = 75
PID_WIDTH                           =  234
PID_HEIGHT                          = 179                   

ENABLE_SERIAL = False           # Disable if in test mode.

import wx
import serial 
import wx.gizmos as gizmos
import math
import decimal

class PIDPanel (wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, label="", pos=wx.DefaultPosition, size= (PID_WIDTH+10, PID_HEIGHT+10)):
        wx.Panel.__init__(self, parent, id, pos,  size)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.frame = parent
        bmp = wx.Bitmap("pid.png")
        image = wx.ImageFromBitmap(bmp)
        w = image.Width
        h = image.Height
        wratio = PID_WIDTH/float(w)
        hratio = PID_HEIGHT/float(h)

        image = image.Scale(PID_WIDTH, PID_HEIGHT, wx.IMAGE_QUALITY_HIGH)
        bmp = wx.BitmapFromImage(image)
        

        self.backgroundBitmap = wx.StaticBitmap(self, -1, bmp, (0, 0)) #576,226
        
        led1_posx =int(87*wratio)
        led1_posy =int(94*hratio)

        led1_sizex = int(498*wratio)
        led1_sizey = int(135*hratio)
        self.led1 = gizmos.LEDNumberCtrl(self, -1, pos=(led1_posx,led1_posy), size=(led1_sizex, led1_sizey))
        self.led1.SetAlignment(gizmos.LED_ALIGN_RIGHT)
        self.led1.SetBackgroundColour("black")
        self.led1.SetForegroundColour("green")
        
        
        led2_posx =int(211*wratio)
        led2_posy =int(275*hratio)

        led2_sizex = int(375*wratio)
        led2_sizey = int(103*hratio)
        self.led2 = gizmos.LEDNumberCtrl(self, -1, pos=(led2_posx, led2_posy), size=(led2_sizex,led2_sizey)) #585, 377
        self.led2.SetAlignment(gizmos.LED_ALIGN_RIGHT)
        self.led2.SetBackgroundColour("black")
        self.led2.SetForegroundColour("red")
    def SetPV(self,  pv):
        self.pv = pv
        self.led1.SetValue(str(self.pv))
    def SetSV(self, sv):
        self.sv = sv
        self.led2.SetValue(str(self.sv))

class ControlPanelFrame (wx.Frame):
     def __init__(self,  parent,  id,  title):
        wx.Frame.__init__(self,  parent,  id,  title, size = (640, 480))
        

class MomentaryButtonControl(wx.PyControl):

    def __init__(self, parent, id=wx.ID_ANY, label="", pos=wx.DefaultPosition,
        size= (PUSH_BUTTON_WIDTH+10, PUSH_BUTTON_HEIGHT+10),  style=wx.NO_BORDER, validator=wx.DefaultValidator,
        name="PushButtonControl",  relayNum=1):
        self.relay = relayNum
      
        wx.PyControl.__init__(self, parent, id, pos,  size , style, validator, name)
        self.normal_bitmap = wx.Bitmap('start button normal.png')
        self.clicked_bitmap = wx.Bitmap('start button down.png')
        
        # scale normal and clicked bitmaps to appropriate size
        image = wx.ImageFromBitmap(self.normal_bitmap)
        image = image.Scale(PUSH_BUTTON_WIDTH, PUSH_BUTTON_HEIGHT, wx.IMAGE_QUALITY_HIGH)
        self.normal_bitmap = wx.BitmapFromImage(image)
        image = wx.ImageFromBitmap(self.clicked_bitmap)
        image = image.Scale(PUSH_BUTTON_WIDTH, PUSH_BUTTON_HEIGHT, wx.IMAGE_QUALITY_HIGH)
        self.clicked_bitmap = wx.BitmapFromImage(image)
        self.bitmap1 = wx.StaticBitmap(self, -1, self.normal_bitmap, (0, 0))
        self.bitmap2 = wx.StaticBitmap(self, -1, self.clicked_bitmap, (0, 0))
        self.bitmap2.Hide()
        self.bitmap1.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.bitmap2.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)

    
    def Down(self):
        if  ENABLE_SERIAL: ser.write(str(self.relay))
        if  ENABLE_SERIAL: ser.write(str(1))
        return
    def Up(self):
        if  ENABLE_SERIAL: ser.write(str(self.relay))
        if  ENABLE_SERIAL: ser.write(str(0))
        return
        
    def OnMouseDown(self, event):
        wx.FutureCall(1, self.Press)
        self.Down()
    def OnMouseUp(self, event):
        wx.FutureCall(1, self.Depress)
        self.Up()


    def Press(self):
        self.bitmap2.Show()
        self.bitmap1.Hide()

    def Depress(self):
        self.bitmap2.Hide()
        self.bitmap1.Show()

class ToggleButtonControl(wx.PyControl):

    def __init__(self, parent, id=wx.ID_ANY, label="", pos=wx.DefaultPosition,
        size= (PUSH_BUTTON_WIDTH+10, PUSH_BUTTON_HEIGHT+10),  style=wx.NO_BORDER, validator=wx.DefaultValidator,
        name="PushButtonControl",  relayNum=1):
        self.relay = relayNum
      
        wx.PyControl.__init__(self, parent, id, pos,  size , style, validator, name)
        self.normal_bitmap = wx.Bitmap('switch off.png')
        self.clicked_bitmap = wx.Bitmap('switch on.png')
        
        # scale normal and clicked bitmaps to appropriate size
        image = wx.ImageFromBitmap(self.normal_bitmap)
        image = image.Scale(PUSH_BUTTON_WIDTH, PUSH_BUTTON_HEIGHT, wx.IMAGE_QUALITY_HIGH)
        self.normal_bitmap = wx.BitmapFromImage(image)
        image = wx.ImageFromBitmap(self.clicked_bitmap)
        image = image.Scale(PUSH_BUTTON_WIDTH, PUSH_BUTTON_HEIGHT, wx.IMAGE_QUALITY_HIGH)
        self.clicked_bitmap = wx.BitmapFromImage(image)
        self.bitmap1 = wx.StaticBitmap(self, -1, self.normal_bitmap, (0, 0))
        self.bitmap2 = wx.StaticBitmap(self, -1, self.clicked_bitmap, (0, 0))
        self.bitmap2.Hide()
        self.bitmap2.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.bitmap1.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.state = False
    

    
    def Toggle(self):
        if  ENABLE_SERIAL:  ser.write(str(self.relay))
        if self.state == False:
            if  ENABLE_SERIAL: ser.write(str(0))
        else:
            if  ENABLE_SERIAL: ser.write(str(1))
        return

        
    def OnMouseDown(self, event):
       
        if self.state == False:
            self.bitmap2.Show()
            self.bitmap1.Hide()
            self.state = True
        else:
            self.bitmap1.Show()
            self.bitmap2.Hide()
            self.state = False
        self.Toggle()
        





class MyApp(wx.App):
    def OnInit(self):
        self.frame = ControlPanelFrame(None,  -1,  'contr')
        button1 = MomentaryButtonControl(self.frame, -1, 'button', pos=(80*0, 0),  relayNum=0)
        button2 = MomentaryButtonControl(self.frame, -1, 'button', pos=(80*1, 0),  relayNum=1)
        button3 = MomentaryButtonControl(self.frame, -1, 'button', pos=(80*2, 0),  relayNum=2)
        button4 = ToggleButtonControl(self.frame, -1, 'button', pos=(80*3, 0),  relayNum=3)
        button5 = ToggleButtonControl(self.frame, -1, 'button', pos=(80*4, 0),  relayNum=4)
        button6 = MomentaryButtonControl(self.frame, -1, 'button', pos=(80*5, 0),  relayNum=5)
        button7 = MomentaryButtonControl(self.frame, -1, 'button', pos=(80*6, 0),  relayNum=6)
        button8 = MomentaryButtonControl(self.frame, -1, 'button', pos=(80*7, 0),  relayNum=7)
        pid1 = PIDPanel(self.frame,  -1, 'PID1',  pos = (50, 90))
        pid1.SetPV(150)
        pid1.SetSV(135)
        
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        self.frame.SetFocus()
        
        return True

app = MyApp()
# remember to sudo chmod 777 /dev/ttyACM0

if  ENABLE_SERIAL: ser = serial.Serial('/dev/ttyACM0', 9600)


# start the event loop
app.MainLoop()



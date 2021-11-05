#!/usr/bin/python
# i-Movie_player.py

"""
Muddassr Ali && Hammad khan
muddassar.geologist@gmail.com
MCS AUSTech Abbottabad (2018)
Final year project : i-Movie_player

"""
#---------------------------------------------------------------------Builtin modules -------------------------------------------------------------------------------------------
import wx , time
from wx.media import *
from wx.media import MediaCtrl
import os
import locale
#---------------------------------------------------------------------End Builtin modules ---------------------------------------------------------------------------------------

#---------------------------------------------------------------------user defined modules --------------------------------------------------------------------------------------
import Computer_Vision as c_v


#--------------------------------------------------------------------- End user defined modules ---------------------------------------------------------------------------------



#--------------------------------------------------------------------- Panel Class ---------------------------------------------------------------------------------------------

class Video(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)


class Image(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)




#--------------------------------------------------------------------- End Panel Class ----------------------------------------------------------------------------------------------

#--------------------------------------------------------------------- Master Class ----------------------------------------------------------------------------------------------
class Player(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,size=(350, 300))
#--------------------------------------------------------------------- Import MediaCtrl -------------------------------------------------------------------------------------------

        try:
            self.mc = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER,
                                         szBackend=wx.media.MEDIABACKEND_DIRECTSHOW
                                         #szBackend=wx.media.MEDIABACKEND_QUICKTIME
                                         #szBackend=wx.media.MEDIABACKEND_WMP10
                                         )

        except NotImplementedError:
            self.Destroy()
            raise

#--------------------------------------------------------------------- End MediaCtrl ----------------------------------------------------------------------------------------------

#--------------------------------------------------------------------- GUI ----------------------------------------------------------------------------------------------
        self.pnl1 = Video(self)
        self.IPanel = Image(self)
        self.IPanel.SetBackgroundColour(wx.WHITE)
        self.IPanel.Hide()
        panel = wx.Panel(self, 1)
#        self.pnl1 = wx.Panel(self, 1)
#        self.pnl3 = wx.Panel(self, 1)
##        pnl1.SetBackgroundColour(wx.BLACK)
        self.pnl1 = (self.mc)
        pnl2 = wx.Panel(self, -1 )
        menubar = wx.MenuBar()
        file = wx.Menu()
        play = wx.Menu()
        view = wx.Menu()
        tools = wx.Menu()
        favorites = wx.Menu()
        help = wx.Menu()
        file.Append(wx.ID_ANY , '&OPEN', 'Add new files')
        exitItem = file.Append(wx.ID_EXIT , '&Quit', 'Quit application')
        menubar.Append(file, '&File')
        menubar.Append(play, '&Play')
        menubar.Append(view, '&View')
        menubar.Append(tools, '&Tools')
        menubar.Append(favorites, 'F&avorites')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)
        self.slider1 = wx.Slider(pnl2, size= wx.DefaultSize)
        pause = wx.BitmapButton(pnl2, -1, wx.Bitmap('icons/stock_media-pause.png'))
        play = wx.BitmapButton(pnl2, -1, wx.Bitmap('icons/stock_media-play.png'))
        next = wx.BitmapButton(pnl2, -1, wx.Bitmap('icons/stock_media-next.png'))
        prev = wx.BitmapButton(pnl2, -1, wx.Bitmap('icons/stock_media-prev.png'))
        volume = wx.BitmapButton(pnl2, -1, wx.Bitmap('icons/volume.png'))
        slider2 = wx.Slider(pnl2, -1, 50, 0, 100, size=(120, -1))

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.slider1, 1, wx.ALL|wx.EXPAND)
        hbox2.Add(play, flag=wx.RIGHT, border=5)
        hbox2.Add(pause)
        hbox2.Add(next, flag=wx.LEFT, border=5)
        hbox2.Add(prev)
        hbox2.Add((-1, -1), 1)
        hbox2.Add(volume)
        hbox2.Add(slider2, flag=wx.TOP | wx.LEFT, border=5)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.BOTTOM, border=10)
        vbox.Add(hbox2, 1, wx.EXPAND)
        pnl2.SetSizer(vbox)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.IPanel, 1, flag=wx.EXPAND | wx.ALL)
        self.sizer.Add(self.pnl1, 1, flag=wx.EXPAND | wx.ALL)
        self.sizer.Add(pnl2, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=10)
        self.SetMinSize((350, 300))
        self.sb = self.CreateStatusBar()
        self.SetSizer(self.sizer)
        self.Centre()

#--------------------------------------------------------------------- End GUI ----------------------------------------------------------------------------------------------



#--------------------------------------------------------------------- Bind GUI and Events ----------------------------------------------------------------------------------------------

        self.Bind(wx.EVT_MENU  , self.QUIT, exitItem)


        self.Bind(wx.EVT_MENU, self.OPEN)

        self.Bind(wx.EVT_BUTTON , self.onPlay, play  )
        self.play=play


        self.Bind(wx.EVT_BUTTON, self.onPause, pause)


        self.Bind(wx.EVT_BUTTON, self.onPrevious, prev)

        self.Bind(wx.EVT_BUTTON, self.onNext, next)

        self.Bind(wx.EVT_BUTTON, self.B_vol, volume)


        self.Bind(wx.EVT_SLIDER, self.onSeek, self.slider1)


        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.timer.Start(100)

        self.slider2 = slider2
        self.Bind(wx.EVT_SLIDER, self.onVolume, self.slider2)



#--------------------------------------------------------------------- End Bind GUI and Events -------------------------------------------------------------------------------------------

#--------------------------------------------------------------------- Wedget Status ----------------------------------------------------------------------------------------------
#        play.Bind(wx.EVT_ENTER_WINDOW, self.play, id=2)
#    def play(self, event):
#        self.sb.SetStatusText('PLAY')
#        event.Skip()
#--------------------------------------------------------------------- End Wedget ----------------------------------------------------------------------------------------------




#--------------------------------------------------------------------- Functions ----------------------------------------------------------------------------------------------


    def QUIT(self, e):
        self.Quit()
        e.SKIP()

    def OPEN(self, e):
        dlg = wx.FileDialog(self,   message="Choose a media file",
                            defaultDir=os.getcwd(), defaultFile="",
                            style=wx.FD_OPEN | wx.FD_CHANGE_DIR |  wx.FD_MULTIPLE )
        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPaths()
            self.ind=list()
##            for i in self.path:
##                self.ind.append(self.path)
##            for j in self.ind:
            self.LoadFile(self.path[0])



        dlg.Destroy()


    def LoadFile(self, path):
        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path, "ERROR", wx.ICON_ERROR | wx.OK)
        else:
            folder, filename = os.path.split(path)
            self.SetTitle('%s' % filename)

            self.mc.Play()
            self.Maximize()
##            self.mc.SetInitialSize()
##            self.GetSizer().Layout()
##            self.slider1.SetRange(0, self.mc.Length())
##            self.onPlay(path) # initial play on load ..



    def B_vol(self, e):
        v = self.slider2.GetValue()
        if v == 0:
            self.slider2.SetValue(100)
            self.mc.SetVolume(1)
            self.sb.SetLabel("Full Volume")
        else:
            self.slider2.SetValue(0)
            self.mc.SetVolume(0)
            self.sb.SetLabel("MUTE")

    def onVolume(self, e):

        currentVolume = self.slider2.GetValue()
        self.mc.SetVolume(currentVolume)
        self.sb.SetLabel("setting volume to : %s" %int(currentVolume))


    def onPlay(self, e):
##        if self.path == None:
##            wx.MessageBox("No File Selected")
##        if not e.GetIsDown():
##            self.onPause()
##            return
        self.pnl1=(self.mc)
        if not self.mc.Play():
            self.pnl1=(self.mc)
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc.Play()
            self.pnl1.Show()
            self.IPanel.Hide()
            self.Layout()
            self.mc.SetInitialSize()
            self.GetSizer().Layout()
            self.slider1.SetRange(0, self.mc.Length())
            self.sb.SetLabel("PLAYING")

#        e.SKIP()





    def onPause(self, e):
            self.mc.Pause()
            self.cap_img()
            self.pnl1.Hide()
            self.IPanel.Show()
            self.Layout()
            self.sb.SetLabel("PAUSED")

    def onPrevious(self, e):
            current = self.myListBox.GetSelection()
            new = current - 1
            self.myListBox.SetSelection(new)
            self.mc.Stop()
            self.load2()

    def onNext(self, e):
        for j in self.path:
            n= self.path[self.i+j]
        self.LoadFile(self.path[n])



    def onSeek(self, e):
        offset = self.slider1.GetValue()
        self.mc.Seek(offset)
        self.sb.SetLabel("Video : %s" %int(offset))


    def onTimer(self, e):
        offset = self.mc.Tell()
        self.slider1.SetValue(offset)
##        self.Time = time.clock()
##        R_Time = self.mc.Length()-self.Time
##        self.sb.SetLabel('size: %s ms' % R_Time)
##        self.sb.SetLabel('( %d seconds )' % (self.mc.Length()/1000))
##        self.sb.SetLabel('position: %d ms' % offset)



#----------------------------------------------------------------------- End Functions -------------------------------------------------------------------------------------


#--------------------------------------------------------------------- Capture Image -------------------------------------------------------------------------------
##

    def cap_img(self):
        screen = wx.ScreenDC()
        size = self.pnl1.GetSize()
##        size = screen.GetSize()
        bmp = wx.Bitmap(size[0], size[1])
        mem = wx.MemoryDC(bmp)
        if self.IsMaximized() == True:
            x = self.pnl1.GetScreenPosition()
            mem.Blit(0, 0, size[0], size[1], screen, x[0], x[1])
        else:
            x = self.pnl1.GetScreenPosition()
            mem.Blit(0, 0, size[0], size[1], screen, x[0], x[1])
        img = bmp.ConvertToImage()
        img1 = wx.Bitmap(img)
        self.s_img = wx.StaticBitmap(self.IPanel, wx.ID_ANY, img1)
        if not os.path.exists('c://Temp//i-movie_player'):
            os.makedirs('c://Temp//i-movie_player')
        img.SaveFile('c://Temp//i-movie_player//Image.jpg', wx.BITMAP_TYPE_JPEG)
        self.img_pnt()

    def img_pnt(self):
        img = c_v.image.face_detect()
        h, w = img.shape[:2]
        wxbmp = wx.Bitmap.FromBuffer(w, h, img)
        wx.StaticBitmap(self.IPanel,
                        bitmap=wx.Bitmap(wxbmp.ConvertToImage()))




#---------------------------------------------------------------- end Capture Image --------------------------------------------------------------------------------




#------------------------------------------------------------------End Master Class --------------------------------------------------------------------------------------

#------------------------------------------------------------------Main Application --------------------------------------------------------------------------------------
if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'C')
    app = wx.App()
    Mp=Player(None, -1 , "i-Movie Player")
    Mp.Show()
    app.MainLoop()
#----------------------------------------------------------------End of Main Application --------------------------------------------------------------------------------------

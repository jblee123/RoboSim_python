import os

from Tkinter      import *
from utils        import *
from environment  import *
from console_comm import *

################################################################################

class Console(Frame):
    def __init__( self, parent=None, app_instance=None ):
        Frame.__init__(self, parent)

        self.app_instance = app_instance

        self.pack(expand=YES, fill=BOTH)                  # make me expandable

        self.pixels_per_meter = 10
        self.meter_width = 70
        self.meter_height = 50

        canvas = Canvas(self, bg='white')
        canvas.config(scrollregion=( 0, 0, 500, 500 ))    # canvas size corners
        canvas.config(highlightthickness=0)               # no pixels to border

        vertical = Scrollbar(self)
        vertical.config(command=canvas.yview)             # xlink sbar and canv
        canvas.config(yscrollcommand=vertical.set)        # move one moves other
        vertical.pack(side=RIGHT, fill=Y)                 # pack first=clip last

        horizontal = Scrollbar(self, orient=HORIZONTAL)
        horizontal.config(command=canvas.xview)           # xlink sbar and canv
        canvas.config(xscrollcommand=horizontal.set)      # move one moves other
        horizontal.pack(side=BOTTOM, fill=X)              # pack first=clip last

        canvas.pack(side=LEFT, expand=YES, fill=BOTH)     # canv clipped first

        self.canvas = canvas

        w = self.winfo_screenwidth() - 100
        h = self.winfo_screenheight() - 100
        self.winfo_toplevel().geometry( '%dx%d+%d+%d' % ( w, h, 50, 25 ) )

        self.scale = EnvironmentScale()
        self.scale.set_original_size( w, h )
        self.env_drawer = EnvDrawer( canvas, None, self.scale )

        parent.protocol( 'WM_DELETE_WINDOW', self.on_destroy )

        parent.bind( '<KeyPress-p>', self.switch_paused )

    def reset_canvas_scroll_bars( self ):
        ( w, h ) = self.scale.env_size_in_pixels()
        self.canvas.config( scrollregion=(0, 0, w, h ) )

    def update_environment( self, env ):
        self.scale.set_environment( env )
        self.env_drawer.set_environment( env )
        self.reset_canvas_scroll_bars()
        self.env_drawer.draw_env()

    def zoom_in( self ):
        self.scale.zoom_in()
        self.reset_canvas_scroll_bars()

    def zoom_out( self ):
        self.scale.zoom_out()
        self.reset_canvas_scroll_bars()

    def on_destroy( self ):
        self.app_instance.initiate_shutdown()

    def switch_paused( self, event ):
        self.app_instance.communicator.send_switch_pause()

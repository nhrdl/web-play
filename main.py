from gi.repository import WebKit 
from gi.repository import Gtk 
from gi.repository import GLib, GObject

from Config import Config
from eBay import eBayScript

class PyPlay:
   
    def exit(self, arg, a1):
        Gtk.main_quit()
        pass

    def activate_inspector(self, inspector, view):  
        return self.inspectorView

    def __init__(self):
        win = Gtk.Window()

        self.view = WebKit.WebView()
        self.view.open("http://www.yahoo.com")
        sw = Gtk.ScrolledWindow() 
        sw.add_with_viewport(self.view) 
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        vbox = Gtk.VBox()
        win.add(vbox)
        
        
        splitter = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)  
        vbox.add(splitter)
        
        sw.set_size_request( -1, 500)
        splitter.add1(sw)
        
        
 #       vbox.add(sw)

        settings = self.view.get_settings()
        
        if (Config.showWebInspector):
            settings.set_property("enable-developer-extras",True)
            sw1 = Gtk.ScrolledWindow() 
            self.inspectorView = WebKit.WebView();
            sw1.add(self.inspectorView) 
            inspector = self.view.get_inspector()  
            inspector.show()
            inspector.connect("inspect-web-view",self.activate_inspector) 
            splitter.add2(sw1)
        #    vbox.add(sw1)
        
          
        settings.set_property("enable-file-access-from-file-uris", True)
        self.view.set_settings(settings)
        
        win.show_all() 
        
        
        win.connect("delete-event", self.exit)
        self.view.open("https://www.finovera.com/cabinet")
        self.view.set_highlight_text_matches(True)    
        win.maximize()
        self.window = win
        #self.view.connect("context-menu", self.displayContextMenu)
        


app = PyPlay()

run = eBayScript(app.view)
GLib.idle_add(run.doIt)

Gtk.main()
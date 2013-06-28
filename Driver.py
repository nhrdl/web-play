from gi.repository import GLib
import time

class Driver(object):
    def navigate(self, view, frame, request, action, decision):
        print "Navigating:", request.get_uri()
        self.frameList.append(frame)
        self.view.execute_script("window.onbeforeunload = function(){alert('PYRECORD:UNLOAD');}")
        
    def alert(self, view, frame, message):
        print "Alert:",message
        if (message == "PYRECORD:UNLOAD"):
            # Clear the list so that we can build new list
            del self.frameList[:]
            return True
        
        return False
            
    def __init__(self, view):
        self.view = view
        self.frameList = [];
        self.view.connect("navigation-policy-decision-requested", self.navigate)
        self.view.connect("script-alert", self.alert)
         
    def _get_page(self, url):
        self.view.open(url)
        return False
        
    def get_page(self, url):
        GLib.idle_add(self._get_page, url)
    
    def allFramesLoaded(self):
        isLoaded = True
        for frame in self.frameList:
            if (frame.get_document().get_state() != "complete"):
                isLoaded = False
        
        return isLoaded
    
    def waitUntilAllFramesLoaded(self):
        endTime = (3*60) + time.time()
        while (time.time() < endTime):
            if (True == self.allFramesLoaded()):
                return
            
            time.sleep(1)
    def wait_until_xpath(self, query):
        pass
       
    def wait_until_text(self, text):
        self.wait_until_xpath("//*[. = '" + text + "']")
        #GLib.idle_add(self._wait_until_text, text)
        self.waitUntilAllFramesLoaded()
        pass
        
        
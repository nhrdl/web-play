from gi.repository import GLib
from gi.repository import GObject
from threading import Event
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
        self.functionWaitEvent = Event()
         
    def _get_page(self, args):
        url = args["url"]
        self.view.open(url)

    def informer_run(self, func, args):
        func(args)
        self.functionWaitEvent.set()
        return False
    
    def run_func(self, func, **args):
        
        GLib.idle_add(self.informer_run, func, args)
        self.functionWaitEvent.wait(3*60)
                
    def get_page(self, url):
        self.run_func(self._get_page, url=url)
        
    
    def allFramesLoaded(self):
        isLoaded = True
        for frame in self.frameList:
            if (frame.get_uri() == "about:blank"):
                continue
             
            if (frame.get_dom_document().get_state() != "complete"):
                isLoaded = False
        
        return isLoaded
    
    def waitUntilAllFramesLoaded(self):
        endTime = (3*60) + time.time()
        while (time.time() < endTime):
            if (True == self.allFramesLoaded()):
                return
            
            time.sleep(1)
    
    def _get_xpath_results(self, args):
        query = args["query"]
        print query
        
    def get_xpath_results(self, query):
        self.run_func(self._get_xpath_results, query=query)
                
    def wait_until_xpath(self, query):
        
        result = self.get_xpath_results(query)
        print result
        pass
       
    def wait_until_text(self, text):
        self.wait_until_xpath("//*[. = '" + text + "']")
        #GLib.idle_add(self._wait_until_text, text)
        self.waitUntilAllFramesLoaded()
        pass
        
        
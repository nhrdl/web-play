from gi.repository import GLib, WebKit
from threading import Event
import gi

import time
from ctypes import CDLL
import ctypes

#Thanks to http://stackoverflow.com/questions/8668333/create-python-object-from-memory-address-using-gi-repository
class _PyGObject_Functions(ctypes.Structure):
    _fields_ = [
       ('register_class',
        ctypes.PYFUNCTYPE(ctypes.c_void_p, ctypes.c_char_p,
                          ctypes.c_int, ctypes.py_object,
                          ctypes.py_object)),
       ('register_wrapper',
        ctypes.PYFUNCTYPE(ctypes.c_void_p, ctypes.py_object)),
       ('lookup_class',
        ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_int)),
       ('newgobj',
        ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
       ]
   
class PyGObjectCPAI(object):
    def __init__(self):
        PyCObject_AsVoidPtr = ctypes.pythonapi.PyCObject_AsVoidPtr
        PyCObject_AsVoidPtr.restype = ctypes.c_void_p
        PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
        addr = PyCObject_AsVoidPtr(ctypes.py_object(gi._gobject._PyGObject_API))
        self._api = _PyGObject_Functions.from_address(addr)

    def pygobject_new(self, addr):
        return self._api.newgobj(addr)
   

capi = PyGObjectCPAI()

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
        self.lastResult = None
        self.frameList = [];
        self.view.connect("navigation-policy-decision-requested", self.navigate)
        self.view.connect("script-alert", self.alert)
        self.functionWaitEvent = Event()
        self.libWebKit = CDLL("libwebkitgtk-3.0.so.0")
         
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
    
    def getDocument(self, *args):
        return self.view.get_dom_document()
    
    def _get_xpath_results(self, args):
        self.lastResult = None
        domDoc = self.getDocument()
        if (None == domDoc):
            return
        print domDoc.get_ready_state()
        if (domDoc.get_ready_state() != "complete"):
            return
        
        
        query = args["query"]
        queryPtr = ctypes.create_string_buffer(query)
        func = self.libWebKit.webkit_dom_document_evaluate
        
        err = GLib.GError()
        print "Query ptr", queryPtr
        print "Query is ", query
        resolver = domDoc.create_ns_resolver(domDoc)
        result = func(hash(domDoc), queryPtr, 0, 0, 7, 0, hash(err))
        print err
        obj = capi.pygobject_new(result)
        self.lastResult = obj
        print obj
        
    def get_xpath_results(self, query):
        self.run_func(self._get_xpath_results, query=query)
        return self.lastResult
                
    def wait_until_xpath(self, query):
        result = self.get_xpath_results(query)
        
        while(result == None or result.get_snapshot_length() == 0):
            time.sleep(1)
            result = self.get_xpath_results(query)
            
        print result
        print result.get_snapshot_length()
        
        pass
       
    def wait_until_text(self, text):
        self.wait_until_xpath("//*[. = '" + text + "']")
        #GLib.idle_add(self._wait_until_text, text)
        self.waitUntilAllFramesLoaded()
        pass
        
        
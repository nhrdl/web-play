from Driver import Driver

class eBayScript(Driver):
    
    def __init__(self, view):
        super(eBayScript, self).__init__(view)
    
    def doIt(self):
        self.get_page("http://www.ebay.com")
        self.wait_until_text("Electronics")
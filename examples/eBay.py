from Driver import Driver

class eBayScript(Driver):
    
    def __init__(self, view):
        super(eBayScript, self).__init__(view)
    
    def doIt(self):
        self.get_page("http://www.ebay.com")
        self.wait_until_text("Electronics")
        self.set_text("//input[@id='gh-ac']", "ipad")
        self.click_element("//*[@id='gh-btn']")
        self.wait_until_text_contains(" Pick Your iPad")
        self.click_element("//a[@class='vip ']")
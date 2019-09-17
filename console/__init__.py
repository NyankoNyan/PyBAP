# -*- coding:utf-8 -*-

from abap_parser import Workspace

#from abap_parser_old.workspace import Workspace  
#from abap_parser_old.token import Tokens  
  

class Console:
    def __init__(self):
        self.workspace = Workspace()
        
    def start(self):
        while True:
            inp = raw_input()
            if inp == "QQ":
                print "Program leave now!"
                break
            else:
                self.workspace.send(inp)
                
class ConsoleTest:
    def __init__(self):
        self.workspace = Workspace()
        
    def start(self):
        self._test_1()
    
    def _test_1(self):
        self.workspace.send("data: i type i, i1 type i, i2 type i. i = i1 + i2. write i.")
    
console_test = ConsoleTest()
console_test.start()

#console = Console()
#console.start()

from execution.statement import ExecutionStatement

class FileOpenError(Exception):
    def __init__(self, filename):
        Exception.__init__(self)
        self.filename = filename   
    def __str__(self, *args, **kwargs):
        return str('Can\'t read file "'+self.filename+'"')

def run_file(filename):
    file_ = open(filename,'r')
    if file_.mode == 'r':
        content = file_.read()
        statement = ExecutionStatement()
        statement.run(content)
        file_.close()
    else:
        file_.close()
        raise FileOpenError(filename)



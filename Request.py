import datetime

id = 1

class Request:
    def __init__(self, file_name):
        global id
        self.id = '{:06d}'.format(id)
        self.date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.time = datetime.datetime.now().strftime('%H:%M:%S')
        self.file_name = file_name
        id += 1

    def getDate(self):
        return self.date

    def getTime(self):
        return self.time

    def getFileName(self):
        return self.file_name

    def getID(self):
        return self.id

import time

class MyTimeInfo:
    def __init__(self, name, type, start=None, end=None, elapsed=None):
        self._name = name
        self._type = type
        self._start = start
        self._end = end
        self._elapsed = elapsed
        self.resultCount = None
        self.note = None

    @property
    def name(self):
        return self._name
    
    @property
    def type(self):
        return self._type
    
    @property
    def start(self):
        return self._start

    def start(self):
        self._start = time.time()
        self.__setElapsed()

    @property
    #def end(self):
    def getEnd(self):
        return self._end

    #@end.setter
    def end(self):
        self._end = time.time()
        self.__setElapsed()

    @property
    def elapsed(self):
        return self._elapsed
    
    def __setElapsed(self):
        if self._start is not None and self._end is not None:
            self._elapsed = self._end - self._start


    @staticmethod
    def csvColumns():
        return ['name', 'type', 'elapsed', 'resultCount', 'note']


    def toArray(self):
        return [self.name, self.type, self.elapsed, self.resultCount, self.note]
    
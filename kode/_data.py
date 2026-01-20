
class Data:

    def __init__(self):
        self._brukelig_data = []
        self._ufull_data = []
        
    def brukelig(self,data):
        self._brukelig_data.append(data)

    def ufullstendig(self,data):
        self._ufull_data.append(data)


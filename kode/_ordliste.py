
class Ordliste:

    def __init__(self, ovre_marg, ufullstendig_data, gloser, veiledning):
        self._ovre_marg = ovre_marg
        self._ufullstendig_data = ufullstendig_data
        self._gloser = gloser
        self._veiledning = veiledning

    def __iter__(self):
        return iter(self._gloser)
    
    def __len__(self):
        return len(self._gloser)
from _eksempel import Eksempel

class Ord:

    def __init__(self, navn, elo_fra, eksempel):
        self._navn = navn.split("/")
        self._elo_fra = float(elo_fra)
        self._eksempel = Eksempel(eksempel)

    def sett_elo(self, ny_elo):
        self._elo_fra = ny_elo

    def hent_navn(self):
        return self._navn
    
    def hent_elo(self):
        return self._elo_fra
    
    def hent_eksempel(self,skjul_ord=False):
        return self._eksempel.hent_eksempel(skjul_ord=skjul_ord)
    
    def __str__(self):
        return '/'.join(self._navn)
    
    def __eq__(self, ord2):
        return set(self._navn) == set(ord2._navn)
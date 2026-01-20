
class Glose:

    def __init__(self, sprak, sprak1_ord, sprak2_ord, kategorier, tagger):

        self._ord = {
            sprak._malsprak: sprak2_ord,
            sprak._hovedsprak: sprak1_ord,
        }

        self._kategorier = kategorier
        self._tagger = tagger

    def hent_score(self):
        return sum(ord.hent_elo()/2 for ord in self._ord.values())
        
    def hent_ord(self, sprak, streng=False):
        ord = self._ord[sprak]
        if streng:
            return str(ord)
        return ord.hent_navn()

    def hent_elo(self, sprak):
        return self._ord[sprak].hent_elo()
    
    def hent_eksempel(self, sprak, skjul_ord=False):
        return self._ord[sprak].hent_eksempel(skjul_ord=skjul_ord)
    
    def hent_kategorier(self, streng=False):
        if streng:
            return ', '.join(self._kategorier)
        return self._kategorier
    
    def sett_elo(self, sprak, ny_elo):
        self._ord[sprak].sett_elo(ny_elo)
    
    def er_kategori(self,hovedkat,underkat=None):
        if underkat==None:
            for kat in self._kategorier:
                hkat = kat.split("/")[0]
                if hkat==hovedkat:
                    return True
        else:
            kateg = hovedkat+"/"+underkat
            for kat in self._kategorier:
                if kateg==kat:
                    return True
        return False
    
    def har_tag(self, tag):
        return tag in self._tagger

    def hent_som_rad(self):
        rad = []

        attributter = (
            lambda x: str(x),
            lambda x: x.hent_elo(),
            lambda x: x.hent_eksempel(),
        )

        for attributt in attributter:
            for ord in self._ord.values():
                rad.append(attributt(ord))

        rad.append(self.hent_kategorier(streng=True))
        rad.append('/ '.join(self._tagger))

        return rad

    def hent_som_kortrad(self):
        return [str(ord) for ord in self._ord.values()]

    def __str__(self):
        ord1,ord2 = self.hent_som_kortrad()
        return f"{ord1} - {ord2}, Score: {self.hent_score()}"
    
    def er_lik(self, glose2):
        return all((self._ord[sprak] == glose2._ord[sprak]) for sprak in self._ord)
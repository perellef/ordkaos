import re

def er_float(string):
    pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
    return bool(re.match(pattern, string))

class Rad:

    def __init__(self, radnr, raddata):
        self.__radnr = radnr
        self.__spr1 = str(raddata[0])
        self.__spr2 = str(raddata[1])
        self.__sist_løst1 = str(raddata[2]) if str(raddata[2]) != '' else ";"*self.__spr1.count(";")
        self.__sist_løst2 = str(raddata[3]) if str(raddata[3]) != '' else ";"*self.__spr2.count(";")
        self.__spr1_elo = str(raddata[4]).replace(",",".")
        self.__spr2_elo = str(raddata[5]).replace(",",".")
        self.__spr1_eks = str(raddata[6])
        self.__spr2_eks = str(raddata[7])
        self.__kategori = str(raddata[8])
        self.__tagger = str(raddata[9])

    def __str__(self):
        return f"Rad {self.__radnr}: {self.__spr1} - {self.__spr2} ({self.__kategori})"

    def er_tom(self):
        return all((
            self.__spr1 == '',
            self.__spr2 == '',
            self.__spr1_elo == '',
            self.__spr2_elo == '',
            self.__spr1_eks == '',
            self.__spr2_eks == '',
            self.__kategori == '',
            self.__tagger == '',
        ))
    
    def er_ufullstendig(self):
        return all((
            self.__spr1 == '',
            self.__spr2 == '',
            self.__spr1_elo == '',
            self.__spr2_elo == '',
            self.__kategori == ''
        ))
        
    def har_elo_på_feil_format(self):
        return any(not er_float(elo.strip()) for elo in (self.__spr1_elo+";"+self.__spr2_elo).split(";"))

    def har_kategori_på_feil_format(self):
        return self.__kategori.count("/") != 1

    def har_sist_løst_på_feil_format(self):
        return any(dato != '' and dato.count("/") != 2 for dato in (self.__sist_løst1+";"+self.__sist_løst2).split(";"))

    def har_elo_som_ikke_matcher_antall_gloser(self):
        return any((
            len(self.__spr1.split(";")) != len(self.__spr1_elo.split(";")),
            len(self.__spr2.split(";")) != len(self.__spr2_elo.split(";"))
        ))
    
    def har_sist_løst_som_ikke_matcher_antall_gloser(self):
        return any((
            len(self.__spr1.split(";")) != len(self.__sist_løst1.split(";")),
            len(self.__spr2.split(";")) != len(self.__sist_løst2.split(";"))
        ))
    
    def spr1(self):return [s.strip() for s in self.__spr1.split(";")]
    def spr2(self): return [s.strip() for s in self.__spr2.split(";")]
    def sist_løst1(self): return self.__sist_løst1.split(";")
    def sist_løst2(self): return self.__sist_løst2.split(";")
    def spr1_elo(self): return self.__spr1_elo.split(";")
    def spr2_elo(self): return self.__spr2_elo.split(";")
    def spr1_eks(self): return self.__spr1_eks
    def spr2_eks(self): return self.__spr2_eks
    def kategori(self): return self.__kategori
    def tagger(self): return [e for e in self.__tagger.split("/") if e != '']
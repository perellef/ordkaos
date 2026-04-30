from datetime import datetime

class Glose:

    def __init__(self, glosegruppe, fra, til, sist_løst, elo, fra_eksempel, til_eksempel, kategori):
        self.__glosegruppe = glosegruppe
        self.__fra = fra
        self.__til = til
        self.__sist_løst = sist_løst
        self.__elo = elo
        self.__fra_eksempel = fra_eksempel
        self.__til_eksempel = til_eksempel
        self.__kategori = kategori
        self.__er_tvetydig = False

    def marker_tvetydig(self):
        self.__er_tvetydig = True

    def sett_elo(self, ny_elo):
        self.__elo = ny_elo

    def forny_sist_løst(self):
        self.__sist_løst = datetime.today().strftime("%d/%m/%y")
    
    def sist_løst_som_tall(self):
        if self.__sist_løst.strip() == '':
            return 0
        return int(''.join(reversed(self.__sist_løst.split("/"))))

    def fra(self): return self.__fra
    def ord_til(self): return self.__til
    def sist_løst(self): return self.__sist_løst
    def elo(self): return self.__elo
    def eksempel_fra(self): return self.__fra_eksempel
    def eksempel_til(self): return "[ ___ ]".join([e for b in self.__til_eksempel.split("[") for e in b.split("]")][::2])
    def kategori(self): return self.__kategori
    def er_tvetydig(self): return self.__er_tvetydig

    def motsatte_oversettelser(self):
        if self in self.__glosegruppe.høyregloser():
            return self.__glosegruppe.venstregloser()
        return self.__glosegruppe.høyregloser()

    def __str__(self):
        return f"{'/'.join(self.__fra)} -> {'/'.join(self.__til)}"

from _glose import Glose

class Glosegruppe:
    def __init__(self, rad):
        self.__rad = rad
        self.__venstregloser = self.__lag_høyregloser(rad)
        self.__høyregloser = self.__lag_venstregloser(rad)

    def __lag_høyregloser(self, rad):
        return self.__lag_gloser(rad.spr1, rad.sist_løst1, rad.spr1_elo, rad.spr2, rad.kategori, rad.spr1_eks, rad.spr2_eks)
    
    def __lag_venstregloser(self, rad):
        return self.__lag_gloser(rad.spr2, rad.sist_løst2, rad.spr2_elo, rad.spr1, rad.kategori, rad.spr2_eks, rad.spr1_eks)

    def __lag_gloser(self, f_spr1, f_sist_løst, f_spr1_elo, f_spr2, f_kategori, f_spr1_eks, f_spr2_eks):
        gloser = []
        for ord, elo, sist_løst in zip(f_spr1(), f_spr1_elo(), f_sist_løst()):
            fra = tuple(ord.split("/"))
            til = tuple(e.strip() for el in f_spr2() for e in el.strip().split("/"))

            glose = Glose(self, fra, til, sist_løst, float(elo), f_spr1_eks(), f_spr2_eks(), f_kategori())
            gloser.append(glose)

        return gloser

    def er_lik(self, andre):
        return all((
            sorted(self.__venstregloser) == sorted(andre.__venstregloser),
            sorted(self.__høyregloser) == sorted(andre.__høyregloser),
            self.__rad.kategori() == andre.__rad.kategori()
        ))

    def som_rad(self):
        return [
            "; ".join(self.__rad.spr1()),
            "; ".join(self.__rad.spr2()),
            '; '.join(map(lambda x: x.sist_løst(), self.__venstregloser)),
            '; '.join(map(lambda x: x.sist_løst(), self.__høyregloser)),
            '; '.join(map(lambda x: str(x.elo()).replace(".", ","), self.__venstregloser)),
            '; '.join(map(lambda x: str(x.elo()).replace(".", ","), self.__høyregloser)),
            self.__rad.spr1_eks(),
            self.__rad.spr2_eks(),
            self.__rad.kategori()
        ]

    def elo_gjennomsnitt(self):
        return sum(map(lambda x: x.elo(), self.__venstregloser+self.__høyregloser))/(len(self.__venstregloser)+len(self.__høyregloser))

    def kortrad(self): return ['; '.join(self.__rad.spr1()), '; '.join(self.__rad.spr2())]
    def venstregloser(self): return self.__venstregloser
    def høyregloser(self): return self.__høyregloser
    def kategori(self): return self.__rad.kategori()
    def tagger(self): return self.__rad.tagger()

    def er_venstreglose(self, item):
        return item in self.__venstregloser

    def er_høyreglose(self, item):
        return item in self.__høyregloser
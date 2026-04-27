from _språk import Språk
from _filhandterer import Filhandterer
from _dataprosessering import Dataprosessering

from collections import defaultdict

class Datasenter:

    def __init__(self):
        self._ordark = Filhandterer.les_json("mine-gloser/ordark.json")

        self._sprak = self.__sett_sprak(self._ordark)
        self._filhandterer = self.__sett_filhandterer(self._ordark)
        self._ordliste = Dataprosessering.hent_ordliste_fra_ordark(self)
        self._kategorier = self.__sett_kategorier()
        self._tagger = self.__sett_tagger()

        self.__marker_tvetydige_gloser()

    def oppdater_ordark(self):
        Dataprosessering.skriv_ordliste_til_ordark(self)

    def __sett_sprak(self, ordark):
        hovedsprak = ordark["hovedspråk"]
        malsprak = ordark["målspråk"]

        return Språk(hovedsprak, malsprak)

    def __sett_filhandterer(self, ordark):
        ordliste_ark = ordark["ordliste-ark"]
        excel_specs = ordark["excel"]
        googleark_specs = ordark["googleark"]

        return Filhandterer(ordliste_ark, excel_specs, googleark_specs)

    def __sett_kategorier(self):
        kategorier = defaultdict(lambda: defaultdict(set))
        for glosegruppe in self._ordliste.glosegrupper():
            kategori, undergruppe = glosegruppe.kategori().split("/")
            if kategori.lower() == "ordliste":
                print("FEIL: Du kan ikke ha kategorien 'ordliste'. Avbryter.")
                exit(1)
            if kategori.lower() == "tag":
                print("FEIL: Du kan ikke ha kategorien 'tag'. Avbryter.")
                exit(1)
            kategorier[kategori][undergruppe].add(glosegruppe)

        for kategori, undergrupper in kategorier.items():
            for emne, grupper in undergrupper.items():
                if len(grupper) <= 3:
                    print(f'MERKNAD: Kun {len(grupper)} glosegruppe{"r" if len(grupper) > 1 else ""} har kategori "{kategori}/{emne}".') 

        return kategorier
    
    def __sett_tagger(self):
        tagger = defaultdict(set)
        for glosegruppe in self._ordliste.glosegrupper():
            for tag in glosegruppe.tagger():
                tagger[tag].add(glosegruppe)

        for tag, grupper in tagger.items():
            if len(grupper) <= 3:
                print(f'MERKNAD: Kun {len(grupper)} glosegruppe{"r" if len(grupper) > 1 else ""} har tag "{tag}".') 

        return tagger

    def __marker_tvetydige_gloser(self):
        for f_sidegloser in (lambda x: x.venstregloser(), lambda x: x.høyregloser()):
            alle_sidegloser = defaultdict(list)

            for glosegruppe in self._ordliste.glosegrupper():
                for glose in f_sidegloser(glosegruppe):
                    alle_sidegloser['/'.join(sorted(glose.fra()))].append(glose)

            for fra, gloser in alle_sidegloser.items():
                if len(gloser) == 1:
                    continue
                
                kategorier = defaultdict(list)
                for glose in gloser:
                    glose.marker_tvetydig()
                    kategorier[glose.kategori()].append(glose)

                for kategori, kategorigloser in kategorier.items():
                    if len(kategorigloser) == 1:
                        continue

                    print(f'VARSEL: Det er {len(kategorigloser)} gloser "{fra}" med identisk kategori: "{kategori}".')
from _rad import Rad
from _glosegruppe import Glosegruppe
from _ordliste import Ordliste

# generelt
RADSTART = 4
KOLSTART = 2 # kolonne B

# ordliste
RADSTØRRELSE_ORDLISTE = 10
FANEFARGE_ORDLISTE = "5C8EDE"

# katliste
RAD_TITTEL = 2
KAT_AVSTAND = 1
RADSTØRRELSE_KATEG = 2
FANEFARGE_KATLISTE = "9FC5E8"

class Dataprosessering:

    @staticmethod
    def hent_ordliste_fra_ordark(datasenter):
        filhandterer = datasenter._filhandterer

        ordliste = Dataprosessering.__lag_ordliste(filhandterer.les_ordark)
        
        if (filhandterer.les_ordark2 is not None):
            ordliste2 = Dataprosessering.__lag_ordliste(filhandterer.les_ordark2)
            print()
            
            Dataprosessering.__verifiser_at_største(ordliste, ordliste2)
        else:
            print()
            
        print('\n'.join(ordliste.parse_errors()))

        return ordliste

    @staticmethod
    def __lag_ordliste(les_ordark):
        orddata = [rad[KOLSTART-1:KOLSTART-1+RADSTØRRELSE_ORDLISTE] for rad in les_ordark()]

        ovre_marg = orddata[:RADSTART-1]
        data = orddata[RADSTART-1:]
        
        ufullstendig_data = []
        parse_errors = []
        glosegrupper = set()

        for rad_indeks,raddata in enumerate(data):
            radnr = rad_indeks+RADSTART
            rad = Rad(radnr, raddata)

            if rad.er_tom():
                continue

            if rad.er_ufullstendig():
                parse_errors.append(f"OBS: {rad} er ufullstendig.")
                ufullstendig_data.append(raddata)
                continue

            if rad.har_elo_som_ikke_matcher_antall_gloser():
                parse_errors.append(f'OBS: {rad} har elo som ikke matcher antall gloser.')
                ufullstendig_data.append(raddata)
                continue

            if rad.har_sist_løst_som_ikke_matcher_antall_gloser():
                parse_errors.append(f'OBS: {rad} har "sist løst" som ikke matcher antall gloser.')
                ufullstendig_data.append(raddata)
                continue

            if rad.har_elo_på_feil_format():
                parse_errors.append(f"OBS: {rad} har elo på feil format.")
                ufullstendig_data.append(raddata)
                continue
            
            if rad.har_sist_løst_på_feil_format():
                parse_errors.append(f'OBS: {rad} har "sist løst" på feil format.')
                ufullstendig_data.append(raddata)
                continue
            
            if rad.har_kategori_på_feil_format():
                parse_errors.append(f"OBS: {rad} har kategori på ukjent format.")
                ufullstendig_data.append(raddata)
                continue

            glosegrupper.add(Glosegruppe(rad)) 

        return Ordliste(ovre_marg, ufullstendig_data, glosegrupper, parse_errors)
    
    @staticmethod
    def __verifiser_at_største(ordliste, ordliste2):
        print("========================\n")
        print("Sammenlikner excel mot googleark ordliste for å prevantivt unngå tap av data.\n")

        nye = ordliste.glosegrupper().difference(ordliste2.glosegrupper())
        mister = ordliste2.glosegrupper().difference(ordliste.glosegrupper())

        print(f"Nye: {len(nye)}")
        print(f"Mister: {len(mister)}")
        print(f"Felles: {len(ordliste.glosegrupper())-len(nye)}\n")

        if len(mister) == 0:
            print("Ingen gloser mistes. Går videre.")
            print("\n========================\n")
            return
        
        print(f'Skriv "MISTER {len(mister)} GLOSER" for å godta overskriving.\nTrykk ENTER for å avbryte.\n')
        while True:
            svar = input("Svar: ")
            if svar == '':
                print("Avslutter.")
                print("\n========================")
                import sys
                sys.exit()
            elif svar == f"MISTER {len(mister)} GLOSER":
                print("\n========================")
                return
            print("Svaret lot seg ikke forstå.")

    @staticmethod
    def skriv_ordliste_til_ordark(datasenter):

        ordliste = datasenter._ordliste
        filhandterer = datasenter._filhandterer
        kategorier = datasenter._kategorier

        data = {}

        # handterer ordliste data
        glosegrupper = list(sorted(ordliste, key=lambda x: (x.kategori(), x.elo_gjennomsnitt())))
        rader = [glosegruppe.som_rad() for glosegruppe in glosegrupper]

        ordliste_data = ordliste.ufullstendig_data() + rader

        # øvre marg
        ordliste_data = ordliste.øvre_marg() + ordliste_data

        # nedre marg
        for j in range(4):
            ordliste_data.append(RADSTØRRELSE_ORDLISTE*[''])

        # venstre marg
        for _ in range(KOLSTART-1):
            for rad in ordliste_data:
                rad.insert(0,'')

        data[filhandterer._ordark_navn] = (FANEFARGE_ORDLISTE, ordliste_data)

        # handterer kategori data

        for kategori, underkategorier in kategorier.items():
            glose_hoyde = max(map(len, underkategorier.values()))+4
            kategoridata = [[] for _ in range(glose_hoyde)]

            antall_kolonner = KOLSTART-1 + len(underkategorier)*(KAT_AVSTAND+RADSTØRRELSE_KATEG)

            # venstre marg
            for _ in range(KOLSTART-1):
                for rad in kategoridata:
                    rad.insert(0,'')

            # øvre marg 
            for _ in range(RADSTART-1):
                kategoridata.insert(0,antall_kolonner*[''])

            # glosene for hver underkategori
            for i,(tittel,glosegrupper) in enumerate(underkategorier.items()):
                glosekloss = [e.kortrad() for e in glosegrupper]

                # titler
                k = KOLSTART-1+i*(RADSTØRRELSE_KATEG+KAT_AVSTAND)

                kategoridata[RAD_TITTEL-1][k] = tittel

                # gloseklossene
                for j,gloserad in enumerate(glosekloss):
                    kategoridata[RADSTART-1+j].extend(gloserad)

                # tomme felter på bunnen av gloseklossene
                for j in range(glose_hoyde-len(glosekloss)):
                    kategoridata[RADSTART-1+len(glosekloss)+j].extend(RADSTØRRELSE_KATEG*[''])

                # tomme felter mellom gloseklossene
                for rad in kategoridata[RADSTART-1:]:
                    rad.extend(KAT_AVSTAND*[''])

            hoyre_marg = 1
            # tomme felter mellom gloseklossene
            for rad in kategoridata[RADSTART-1:]:
                rad.extend(hoyre_marg*[''])

            # nedre marg
            for j in range(4):
                kategoridata.append((antall_kolonner+hoyre_marg)*[''])

            data[kategori] = (FANEFARGE_KATLISTE, kategoridata)


        # skriv til ordark
        for skriv_ordark in filhandterer.skriv_ordark:
            skriv_ordark(data)
        
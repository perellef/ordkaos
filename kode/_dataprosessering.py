from _ord import Ord
from _glose import Glose
from _ordliste import Ordliste

import re

# generelt
radstart = 4
kolstart = 2 # kolonne B

# ordliste
radstorrelse_ordliste = 8
fanefarge_ordliste = "5C8EDE"

# katliste
rad_tittel = 2
kat_avstand = 1
radstorrelse_kateg = 2
fanefarge_katliste = "9FC5E8"


def er_float(string):
    pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
    return bool(re.match(pattern, string))

class Dataprosessering:

    @staticmethod
    def hent_ordliste_fra_ordark(datasenter):
        filhandterer = datasenter._filhandterer

        ordliste = Dataprosessering.__lag_ordliste(datasenter, filhandterer.les_ordark)
        
        if (filhandterer.les_ordark2 is not None):
            ordliste2 = Dataprosessering.__lag_ordliste(datasenter, filhandterer.les_ordark2)

            Dataprosessering.__verifiser_at_storste(ordliste, ordliste2)

        print('\n'.join(ordliste._veiledning))
        return ordliste

    @staticmethod
    def __lag_ordliste(datasenter, les_ordark):
        ordark = datasenter._ordark

        hovedsprak = ordark["hovedspråk"]
        malsprak = ordark["målspråk"]

        orddata = [rad[kolstart-1:kolstart-1+radstorrelse_ordliste] for rad in les_ordark()]

        ovre_marg = orddata[:radstart-1]
        data = orddata[radstart-1:]
        
        spr1_ord = set()
        spr2_ord = set()

        ufullstendig_data = []
        gloser = []
        veiledning = []

        tomme_rader = []
        for rad_indeks,rad in enumerate(data):
            spr2,spr1,spr2_elo,spr1_elo,spr2_eks,spr1_eks,kateg,tag = rad

            spr1_elo = str(spr1_elo).replace(",",".")
            spr2_elo = str(spr2_elo).replace(",",".")

            radnr = rad_indeks+radstart
            if all((el == '' for el in rad)):
                if len(tomme_rader)>0:
                    if (isinstance(tomme_rader[-1],list)):
                        if (tomme_rader[-1][-1] == radnr-1):
                            tomme_rader[-1][-1] += 1
                            continue
                    if (tomme_rader[-1] == radnr-1):
                        tomme_rader[-1] = [tomme_rader[-1], tomme_rader[-1]+1]
                        continue
                tomme_rader.append(radnr)
                continue


            if '' in [spr1,spr2,kateg]:
                veiledning.append(f"MERKNAD: Rad {radnr}: {spr2} - {spr1} ({kateg}) er ufullstendig, og legges øverst i ordlisten.\n")
                ufullstendig_data.append(rad)
                continue

            if spr1_elo == '':
                veiledning.append(f"NOTAT: Rad {radnr}: {spr2} - {spr1} ({kateg}) ble gitt {hovedsprak}->{malsprak} elo 5 som resultat av manglende verdi.")
                spr1_elo = '5'
            if spr2_elo == '':
                veiledning.append(f"NOTAT: Rad {radnr}: {spr2} - {spr1} ({kateg}) ble gitt {malsprak}->{hovedsprak} elo 5 som resultat av manglende verdi.")
                spr2_elo = '5'

            if not er_float(spr1_elo):
                veiledning.append(f"MERKNAD: Rad {radnr}: {spr2} - {spr1} ({kateg}) har uforståelig {hovedsprak}->{malsprak} elo, og legges øverst i ordlisten.")
                ufullstendig_data.append(rad)
                continue
            if not er_float(spr2_elo):
                veiledning.append(f"MERKNAD: Rad {radnr}: {spr2} - {spr1} ({kateg}) har uforståelig {malsprak}->{hovedsprak} elo, og legges øverst i ordlisten.")
                ufullstendig_data.append(rad)
                continue
            
            spr1 = spr1.strip()
            spr2 = spr2.strip()

            if spr1 in spr1_ord:
                veiledning.append(f'MERKNAD: "{spr1}" er ikke entydig fra {hovedsprak}->{malsprak}')
            if spr2 in spr2_ord:
                veiledning.append(f'MERKNAD: "{spr2}" er ikke entydig fra {malsprak}->{hovedsprak}')

            spr1_ord.add(spr1)
            spr2_ord.add(spr2)

            sprak1_ord = Ord(spr1, spr1_elo, spr1_eks)
            sprak2_ord = Ord(spr2, spr2_elo, spr2_eks)

            kat = re.split(r', ',kateg)

            glose = Glose(datasenter._sprak, sprak1_ord, sprak2_ord, kat, tag.split("/ "))
            gloser.append(glose)


        if len(tomme_rader)>0:
            tom_fjerning = 'NOTAT: Tomme rader ble fjernet fra rad: '
            for el in tomme_rader:
                if isinstance(el, list):
                    tom_fjerning += f'{el[0]}-{el[1]}, '
                else:
                    tom_fjerning += f'{el}, '
            veiledning.insert(0,tom_fjerning)

        return Ordliste(ovre_marg, ufullstendig_data, gloser, veiledning)
    
    @staticmethod
    def __verifiser_at_storste(ordliste, ordliste2):
        print("\n========================\n")
        print("Sammenlikner excel mot googleark ordliste for å prevantivt unngå tap av data.\n")

        nye = sum(1 for glose in ordliste if not any(glose.er_lik(gl) for gl in ordliste2))
        mister = sum(1 for glose in ordliste2 if not any(glose.er_lik(gl) for gl in ordliste))

        print(f"Nye: {nye}")
        print(f"Mister: {mister}")
        print(f"Felles: {len(ordliste)-nye}\n")

        if (mister == 0):
            print("Ingen gloser mistes. Går videre.")
            print("\n========================\n")
            return
        
        print('Avslutt ved å trykke enter hvis du er misfornøyd med dette. Svar "neste" for å gå videre.\n')
        while True:
            svar = input("Svar: ")
            if svar == '':
                print("Avslutter.")
                print("\n========================")
                import sys
                sys.exit()
            elif svar == "neste":
                print("\n========================\n")
                return
            print("Svaret lot seg ikke forstå.")

    @staticmethod
    def skriv_ordliste_til_ordark(datasenter):

        ordliste = datasenter._ordliste
        filhandterer = datasenter._filhandterer
        kategorier = datasenter._kategorier

        data = {}

        # handterer ordliste data

        sortering = lambda x: (x.hent_kategorier(streng=True), x.hent_score())
        gloser = list(sorted(ordliste._gloser, key=sortering))
        gloserader = [glose.hent_som_rad() for glose in gloser]

        ordliste_data = ordliste._ufullstendig_data + gloserader

        # øvre marg
        ordliste_data = ordliste._ovre_marg + ordliste_data

        # nedre marg
        for j in range(4):
            ordliste_data.append(radstorrelse_ordliste*[''])

        # venstre marg
        for _ in range(kolstart-1):
            for rad in ordliste_data:
                rad.insert(0,'')


        data[filhandterer._ordark_navn] = (fanefarge_ordliste, ordliste_data)

        # handterer kategori data

        for hkat in kategorier.values():

            underkategorier = hkat.hent_underkategorier()

            glose_hoyde = max((len(uk.hent_gloser_som_kortrader()) for uk in underkategorier.values()), default=0)+4
            kategoridata = [[] for _ in range(glose_hoyde)]

            antall_kolonner = kolstart-1 + len(underkategorier)*(kat_avstand+radstorrelse_kateg)

            # venstre marg
            for _ in range(kolstart-1):
                for rad in kategoridata:
                    rad.insert(0,'')

            # øvre marg 
            for _ in range(radstart-1):
                kategoridata.insert(0,antall_kolonner*[''])

            # glosene for hver underkategori
            for i,uk in enumerate(underkategorier.values()):
                glosekloss = uk.hent_gloser_som_kortrader()

                # titler
                k = kolstart-1+i*(radstorrelse_kateg+kat_avstand)

                kategoridata[rad_tittel-1][k] = uk._sprak2_tittel
                kategoridata[rad_tittel-1][k+1] = uk._sprak1_tittel

                # gloseklossene
                for j,gloserad in enumerate(glosekloss):
                    kategoridata[radstart-1+j].extend(gloserad)

                # tomme felter på bunnen av gloseklossene
                for j in range(glose_hoyde-len(glosekloss)):
                    kategoridata[radstart-1+len(glosekloss)+j].extend(radstorrelse_kateg*[''])

                # tomme felter mellom gloseklossene
                for rad in kategoridata[radstart-1:]:
                    rad.extend(kat_avstand*[''])

            hoyre_marg = 1
            # tomme felter mellom gloseklossene
            for rad in kategoridata[radstart-1:]:
                rad.extend(hoyre_marg*[''])

            # nedre marg
            for j in range(4):
                kategoridata.append((antall_kolonner+hoyre_marg)*[''])

            data[hkat.hent_navn()] = (fanefarge_katliste, kategoridata)


        # skriv til ordark
        for skriv_ordark in filhandterer.skriv_ordark:
            skriv_ordark(data)
        
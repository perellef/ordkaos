from _datasenter import Datasenter
from _prove import Prove

import random

def kommandolokke():

    print("\nLaster inn data.\n")

    datasenter = Datasenter()

    sporsmalsskille()
    print("Hei og velkommen! Hva ønsker du å gjøre?\n 1) Teste meg i en prøve.\n 2) Oppdatere regneark.")

    while True:
        svar = input("svar: ")

        if svar=="1":
            break
        elif svar=="2":
            print()
            datasenter.oppdater_ordark()
            return
        else:
            print("Svaret ble ikke forstått. Prøv på nytt.")
            continue

    while True:
        sporsmalsskille()

        print('Ønsker du å lage en prøve der elo oppdateres? Svar "Ja" eller "Nei".')
        
        while True:

            svar = input("svar: ").lower()

            if svar=="ja":
                elo = True
                print("[+] Med oppdatering av elo valgt.")
            elif svar=="nei":
                elo = False
                print("[+] Uten oppdatering av elo valgt.")
            else:
                print('Svaret ble ikke forstått. Oppgi enten "ja" eller "nei".')
                continue

            break

        
        sporsmalsskille()

        sprak = datasenter._sprak

        hovedsprak = sprak._hovedsprak
        malsprak = sprak._malsprak
    
        print(f"Hvilket av følgende prøveformat ønsker du?\n 1) {malsprak} -> {hovedsprak}\n 2) {hovedsprak} -> {malsprak}")
        
        while True:

            svar = input("svar: ")

            if svar=="1":
                start,slutt = malsprak, hovedsprak
            elif svar=="2":
                start,slutt = hovedsprak, malsprak
            else:
                print('Svaret ble ikke forstått. Oppgi enten "1" eller "2".')
                continue
            
            print(f'[+] Prøveformatet "{start} -> {slutt}" valgt.')
            break

        sporsmalsskille()

        kategorier = datasenter._kategorier

        print("Hvilke kategorier ønsker du å testes i? Kategoriene er:")
        for hkat in kategorier.values():
            print(f"\n {hkat._kortnavn}: {', '.join(hkat.hent_underkategorier().keys())}", end="")
                
        print('\n\nSkriv "<hovedkategori>/<underkategori>" eller "<hovedkategori>" for å velge kategorier. Du kan også skrive "alt" for å velge alle.')
        print('Skriv "neste" for å gå videre.\n')

        gloser = []
        while True:
            svar = input("svar: ").removeprefix('"').removesuffix('"').removeprefix('+')

            if svar=="alt":
                gloser = datasenter._ordliste._gloser
                print(f"[+] Alle kategorier lagt til ({len(gloser)} gloser).")
                break
            elif svar=="neste":
                if len(gloser)==0:
                    print("Du kan ikke ha en tom prøve.")
                    continue
                break

            svar_splt = svar.lower().split("/")
            
            if len(svar_splt)==1:
                hk = svar
                uk = None
            elif len(svar_splt)==2:
                hk,uk = svar_splt
            else:
                print("Svaret lot seg ikke forstå.")

            if hk not in kategorier:
                print(f'Ingen hovedkategori "{hk}" finnes.')
                continue

            hovedkategori = kategorier[hk]
            underkategorier = hovedkategori.hent_underkategorier()
            if uk == None:
                nye_gloser = [glose for ukat in underkategorier.values() for glose in ukat._gloser]
                gloser += nye_gloser
            else:
                if uk not in underkategorier:
                    print(f'"{hk}" har ingen underkategori "{uk}".')
                    continue
                nye_gloser = underkategorier[uk]._gloser
                gloser += nye_gloser 

            print(f'[+] Kategorien "{svar}" lagt til ({len(nye_gloser)} gloser).\n')

        gloser = list(set(gloser))

        print(f"\n[+] {len(gloser)} gloser valgt.\nGår videre.")

        sporsmalsskille()
        print('Hvis du vil filtrere på tag oppgi "+<tag>" eller "-<tag>", ellers "neste"')

        tagloop = True
        while tagloop:

            svar = input("svar: ")

            if svar=="neste":
                print("Går videre.")
                break

            if len(svar) < 2:
                print("Svaret lot seg ikke forstå.")
                continue

            filtervariant = svar[0]
            if filtervariant not in ("+", "-"):
                print("Tag'en skal oppgis med enten \"-\" eller \"+\" først.")
                continue

            tag = svar[1:]
            pot_gloser = [glose for glose in gloser if (filtervariant == "+") == glose.har_tag(tag)]

            print(f'\nDet er {len(pot_gloser)} etter valg av tag-filter. Er du fornøyd med å bruke disse? Svar "Ja" eller "Nei"')

            while True:
                svar2 = input("svar: ")

                if svar2.lower() == "ja":
                    tagloop = False
                    gloser = pot_gloser[:]
                    
                    print(f'[+] Gloser med tag "{svar}" valgt ({len(gloser)} gloser).')
                    break
                elif svar2.lower() == "nei":
                    break
                print(f'Svaret lot seg ikke forstå. Svar enten "Ja" eller "Nei".')
            
        sporsmalsskille()
        print("Hva slags uttrekk av spørsmål ønsker du? \n 1) Tilfeldig\n 2) Vanskelig\n 3) Lett\n 4) ELO-vektet sannsynlighet (svakere elo -> mer sannsynlig)")
        
        while True:

            svar = input("svar: ")

            if svar=="1":
                vanskgrad = "tilfeldig"
                break
            elif svar=="2":
                vanskgrad = "vanskelig"
            elif svar=="3":
                vanskgrad = "lett"
            elif svar=="4":
                vanskgrad = "sannsynlighetsvektet"
            else:
                print('Svaret ble ikke forstått. Oppgi enten "1", "2" eller "3".')
                continue
            
            break
        
        print(f'[+] {vanskgrad.capitalize()} prøve valgt.')

        utvalgte_gloser = gloser[:]
        if vanskgrad == "tilfeldig":
            pass
        elif vanskgrad in ("lett","vanskelig"):
            gloser = sorted(gloser, key=lambda x: x.hent_score(),reverse=False)

            sporsmalsskille()
            print(f"Hvilken persentil av {vanskgrad}e gloser ønsker du? Svar mellom 0 og 100.")

            persentilloop = True
            while persentilloop:

                svar = input("svar: ")

                try:
                    antall = int(svar)
                    if antall<1:
                        print('Svaret kan ikke være mindre enn 1. Prøv på nytt')
                        continue
                    if antall>100:
                        print('Svaret kan ikke været større enn 100. Prøv på nytt')
                        continue
                    
                except ValueError:
                    print('Svaret er ikke et heltall. Prøv på nytt.')
                    continue
                
                if vanskgrad=="vanskelig":
                    utvalgte_gloser = gloser[:int((antall/100)*len(gloser)+1e-4)]
                elif vanskgrad=="lett":
                    utvalgte_gloser = gloser[len(gloser)-1-int((antall/100)*len(gloser)+1e-4):]

                if len(utvalgte_gloser)==0:
                    print(f'Persentilen du valgte gir 0 gloser og er mindre enn minste mulige prøve. Velg en høyere persentil.')
                    continue

                print(f'\nDu er i ferd med å velge en persentil med {len(utvalgte_gloser)} gloser. Er du fornøyd med dette? Svar ja/nei.')
                
                while True:
                    svar2 = input("svar: ")

                    if svar2.lower() == "ja":
                        persentilloop = False
                        break
                    elif svar2.lower() == "nei":
                        print(f"\nHvilken persentil av {vanskgrad}e gloser ønsker du istedet? Svar mellom 0 og 100.")
                        break
                    print(f'Svaret lot seg ikke forstå. Svar enten "Ja" eller "Nei".')
                
        
            print(f'[+] {antall}%-persentil valgt ({len(utvalgte_gloser)} gloser).')
        elif vanskgrad == "sannsynlighetsvektet":
            utvalgte_gloser = sorted(gloser, key=lambda x: random.random()*x.hent_score(), reverse=False)

        sporsmalsskille()
        print("Hvor mange spørsmål ønsker du i prøven?")
        
        while True:

            svar = input("svar: ")

            try:
                antall = int(svar)
                if antall<1:
                    print('Svaret kan ikke være mindre enn 1. Prøv på nytt')
                    continue
                if antall>len(utvalgte_gloser):
                    print('Du kan ikke ha flere spørsmål enn antall gloser. Prøv på nytt')
                    continue
                print(f"[+] {svar} spørsmål valgt.")
                
            except ValueError:
                print('Svaret er ikke et heltall. Prøv på nytt.')
                continue
            break

        sporsmalsskille()

        prove = Prove(datasenter,elo,start,slutt,utvalgte_gloser,antall)

        print('Prøven er nå ferdiglaget.')

        provelokke = True
        while provelokke:
            print("Trykk enter for å starte prøven.")
            input()
            prove.start()

            sporsmalsskille()

            print("Hva ønsker du å gjøre nå?\n 1) Starte prøven på nytt.\n 2) Starte prøven på nytt med motsatt oversettelse.\n 3) Lage en ny prøve.\n 4) Avslutte.")

            while True:

                svar = input("svar: ")
                if svar=="1":
                    sporsmalsskille()
                    break
                elif svar=="2":
                    start,slutt = slutt, start
                    prove = Prove(datasenter,elo,start,slutt,utvalgte_gloser,antall)
                    sporsmalsskille()
                    break
                elif svar=="3":
                    provelokke = False
                    break
                elif svar=="4" or svar=="avslutte":
                    datasenter.oppdater_ordark()
                    return
                
                print('Svaret ble ikke forstått. Oppgi enten "1", "2", "3" eller "4".')
        


def sporsmalsskille(end="\n"):
    print("\n---------------------\n", end=end)

def oppdaterRegneark():
    datasenter = Datasenter()
    datasenter.oppdater_filer()

    


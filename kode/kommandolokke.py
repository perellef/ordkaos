from _datasenter import Datasenter
from _prove import Prove

import random
import shutil
import textwrap

def kommandolokke():
    print("\nLaster inn data.\n")

    datasenter = Datasenter()

    sprak = datasenter._sprak
    hovedsprak = sprak._hovedsprak
    malsprak = sprak._malsprak
    kategorier = datasenter._kategorier
    tagger = datasenter._tagger
    
    alle_glosegrupper = datasenter._ordliste.glosegrupper()

    while True:

        sporsmalsskille(1)
        print("Hva ønsker du å testes i?\n")
        print("  Kategorier:\n  ‾‾‾‾‾‾‾‾‾‾")

        maks = max(map(len, kategorier.keys()))
        for kategori,underkategorier in sorted(kategorier.items()):
            width = shutil.get_terminal_size((80, 20)).columns

            prefix = f"  {kategori.ljust(maks)}: "
            indent = " " * len(prefix)
            tekst = ", ".join(underkategorier)

            print(textwrap.fill(tekst, width=width, initial_indent=prefix, subsequent_indent=indent))

        print("\n  Tagger:", "(ingen tagger)" if len(tagger) == 0 else ', '.join(tagger))
        print("  ‾‾‾‾‾‾")

        print('Velg kategori med "<kategori>" eller "<kategori>/<tema>", og tag med "tag/<tag>". Tips: skriv "alt" for å velge alle.')
        print('Trykk ENTER for å gå videre.\n')

        glosegrupper = set()
        while True:
            svar = input("svar: ").strip('"').removeprefix('+')

            if svar=="alt":
                glosegrupper = set(alle_glosegrupper)
                print(f"[+] Alt lagt til ({len(glosegrupper)} glosegrupper).")
                break
            elif svar=="":
                if len(glosegrupper)==0:
                    print("Du kan ikke gå videre uten å ha valgt gloser.")
                    continue
                break

            svar_splt = svar.lower().split("/")
            
            if len(svar_splt)==1:
                hk = svar
                uk = None
            elif len(svar_splt)==2:
                hk, uk = svar_splt
            else:
                print("Svaret lot seg ikke forstå.")

            if hk == 'tag':
                if uk not in tagger:
                    print(f'Ingen tag "{uk}" finnes.')
                else:
                    nye_glosegrupper = tagger[uk].difference(glosegrupper)
                    glosegrupper = glosegrupper.union(nye_glosegrupper)
                    print(f'[+] Gloser med tag "{uk}" lagt til ({len(nye_glosegrupper)} glosegrupper).\n')
                continue

            if hk not in kategorier:
                print(f'Ingen hovedkategori "{hk}" finnes.')
                continue
            
            if uk == None:
                nye_glosegrupper = set(e for uk in kategorier[hk] for e in kategorier[hk][uk]).difference(glosegrupper)
                glosegrupper = glosegrupper.union(nye_glosegrupper)
            else:
                if uk not in kategorier[hk]:
                    print(f'"{hk}" har ingen underkategori "{uk}".')
                    continue
                nye_glosegrupper = kategorier[hk][uk].difference(glosegrupper)
                glosegrupper = glosegrupper.union(nye_glosegrupper)

            print(f'[+] Kategorien "{svar}" lagt til ({len(nye_glosegrupper)} glosegrupper).\n')

        print(f"\n[+] {len(glosegrupper)} glosegrupper valgt.\nGår videre.")

        sporsmalsskille(2)
        print(f"Hvilken vei vil du oversette?\n 1) {malsprak} -> {hovedsprak}\n 2) {hovedsprak} -> {malsprak}")
        
        while True:
            svar = input("svar: ")

            if svar=="1":
                start,slutt = malsprak, hovedsprak
                gloser = [glose for glosegruppe in glosegrupper for glose in glosegruppe.høyregloser()]
            elif svar=="2":
                start,slutt = hovedsprak, malsprak
                gloser = [glose for glosegruppe in glosegrupper for glose in glosegruppe.venstregloser()]
            else:
                print('Svaret ble ikke forstått. Oppgi enten "1" eller "2".')
                continue
            
            print(f'[+] Retning "{start} -> {slutt}" valgt ({len(gloser)} gloser)')
            break

        sporsmalsskille(3)
        print("Hva slags uttrekk av spørsmål ønsker du?\n 1) Tilfeldig\n 2) Lengst siden løst\n 3) Vanskelig\n 4) Lett\n 5) Sannsynlighetsvektet (svakere elo -> mer sannsynlig)")
        
        while True:

            svar = input("svar: ")

            if svar=="1":
                print(f'[+] Tilfeldig prøve valgt.')
                utvalgte_gloser = list(sorted(gloser, key=lambda _: random.random()))
            elif svar=="2":
                print(f'[+] Lengst siden løst- prøve valgt.')
                utvalgte_gloser = list(sorted(gloser, key=lambda x: x.sist_løst_som_tall()))
            elif svar=="3":
                print(f'[+] Vanskelig prøve valgt.')
                utvalgte_gloser = list(sorted(gloser, key=lambda x: x.elo()))
            elif svar=="4":
                print(f'[+] Lett prøve valgt.')
                utvalgte_gloser = list(sorted(gloser, key=lambda x: x.elo(), reverse=True))
            elif svar=="5":
                print(f'[+] Sannsynlighetsvektet prøve valgt.')
                utvalgte_gloser = list(sorted(gloser, key=lambda x: random.random()*x.elo()**2))
            else:
                print('Svaret ble ikke forstått. Oppgi enten "1", "2" eller "3".')
                continue
            break

        sporsmalsskille(4)
        print(f"Hvor mange spørsmål ønsker du i prøven? Du har {len(utvalgte_gloser)} gloser.")
        
        while True:

            svar = input("svar: ")

            try:
                antall = int(svar)
                if antall < 1:
                    print('Svaret kan ikke være mindre enn 1. Prøv på nytt')
                    continue
                if antall > len(utvalgte_gloser):
                    print('Du kan ikke ha flere spørsmål enn antall gloser. Prøv på nytt')
                    continue
                
                utvalgte_gloser = utvalgte_gloser[:antall]
                print(f"[+] {svar} spørsmål valgt.")
                
            except ValueError:
                print('Svaret er ikke et heltall. Prøv på nytt.')
                continue
            break

        sporsmalsskille()

        prøve = Prove(datasenter, start, slutt, utvalgte_gloser)

        print('Prøven er nå klar.')

        prøveløkke = True
        while prøveløkke:
            print("Trykk ENTER for å starte prøven.")
            input()
            prøve.start()

            sporsmalsskille()

            print("Hva ønsker du å gjøre nå?\n 1) Starte prøven på nytt.\n 2) Starte prøven på nytt med motsatt oversettelse.\n 3) Velg nye gloser.\n 4) Avslutte.")

            while True:

                svar = input("svar: ")
                if svar=="1":
                    sporsmalsskille()
                    break
                elif svar=="2":
                    start, slutt = slutt, start
                    utvalgte_gloser = list(set(motsatt_glose for glose in utvalgte_gloser for motsatt_glose in glose.motsatte_oversettelser()))
                    
                    prøve = Prove(datasenter, start, slutt, utvalgte_gloser)
                    sporsmalsskille()
                    break
                elif svar=="3":
                    prøveløkke = False
                    break
                elif svar=="4" or svar=="avslutte":
                    print()
                    datasenter.oppdater_ordark()
                    print()
                    return
                
                print('Svaret ble ikke forstått. Oppgi enten "1", "2", "3" eller "4".')

def sporsmalsskille(steg=None, end="\n"):
    width = shutil.get_terminal_size((80, 20)).columns
    if steg == None:
        print(f'\n{"-"*width}\n', end=end)
    else:
        print(f'\n{"-"*3} [STEG {steg}/4] {"-"*(width - 17)}\n', end=end)

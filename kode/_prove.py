from _score import Score

import math
import random
import time

BLOMST_ASCII_BILDE = """                                           -+*****+.                                                \n                                        -%+---------*%                                              \n                                       #=-------------+*                                            \n                                     .%----------------=*                                           \n                                     *------------------=#                                          \n                                    :*-------------------%                                          \n                                    -=-------------------%:-+*******=                               \n                         .**+=====+*%+-------------------*=----------=*.                            \n                       .#=-----------=---------+-------==--------------*=                           \n                      *+---------------=-------+------=-----------------++                          \n                     +=-----------------=------+-----=-------------------#                          \n                    .*-------------------==----=-------------------------+=                         \n                    :+---------------------=-=+**+==------==-------------*-                         \n                    :+-------------=-------=*-....+*--===----------------%                          \n                     *------------------=++#:......++-------------------#.         =**+.            \n                     :*--------------------#.......=+------------------*.       -+-------+          \n                      .#=---------------===+*:....+*--======---------*%*=---==-+----------+.        \n             +####=     -#----------==------=+*##+-=----------=+==*#:+=--------=-----------*        \n          -#--------*      +#+==-==--------=---==---=-------------*. +----------=----------*        \n         -=----------+        #+----------+----==----==------------+#*===-------+---------+-        \n         +-----------=*=++==+#=----------=-----==------=----------+=-------=-----=-=-----+=---===   \n         +-----------+=-----+=----------------------------------=+-----------==--=-=--==---------+. \n   :**===+=-----=---=-------*-----------------------------------+--------------====+=-------------= \n  +---------=---=--=---=---=*-------------------=---------------+--------------=....*====---------+ \n ==-----------=--==--=------*--------------------*--------------*=----------=--=-..-+------------=- \n *-------------+*::**---===-++------------------*%#--------------=*=-----=----=--+==---==-------+-  \n ==-----------=%....+--------++----------------####*+--------------**#+------=---=-==------=#=:     \n  +----------===#--#=++--------#+-----------=%..##*  *%=---------+#. #-----------=---=--------      \n   -*=-----=---=--------===----=***++===+*#+   :##.     :+#****+:    =-----------------------=      \n      =#=-----=--==-----------#-               ###                -*##-----------=-----------+      \n      +------=---=-------------*              .##-             .*##*  *---------#%=---------+:      \n      +----------=-------------*              ###             +##:     -=-----=   .+=-----=+        \n      +-----------+-----------*:              ##+           *#*:                     .:-:           \n       #=--------++*---------*.              =##:         -##                                       \n        .#+----++   =*----+%=                *##.        ##=                                        \n                          +#+                *#+       .##:                                         \n                           :##:             :##=      -#*                                           \n                             *#+            -##-     +#+                                            \n                              +#+           +##     =#*                                             \n                               -#*          *##    -##                                              \n                                -##         ##*   -##                                               \n                                 =#*       .##:  .##.                                               \n                                  +#+      -##   *#-                                                \n                                   *#=     *##  =#*                                                 \n                                    ##:    ### .##                                                  \n                                    :##    ### ##:                                                  \n                                     +#+   ##==#*                                                   \n                                      ##: .##.##:                                                   \n                                      +#+ :##*#+                                                    \n                                       ##.=####=                                                    \n                                       -##*####                                                     \n                                        ======-"""

class Prove:

    def __init__(self, datasenter, fra, til, gloser):
        self._datasenter = datasenter

        self._sprak_fra = fra
        self._sprak_til = til
        self._gloser = gloser

    def start(self):
        
        print(f"Oversett følgende fra {self._sprak_fra} til {self._sprak_til}. Trykk ENTER for å få eksempel til et ord.")

        forventet_poeng = 0
        tot_poeng = 0
        random.shuffle(self._gloser)

        resultat = {}

        print(f"\nDet er til sammen {len(self._gloser)} spørsmål.")
        for i,glose in enumerate(self._gloser[:len(self._gloser)]):

            if (i % 10)==0:
                print(f"\nGloser {i+1} - {min((i+10), len(self._gloser))}:")

            i = -1
            while True:
                i += 1
                skal_oversettes = (f'({glose.kategori()} )' if glose.er_tvetydig() else '') + '/'.join(glose.fra())
                svar = input(f" {skal_oversettes}: ")

                if svar!="":
                    break

                if i==0:
                    eksempel = glose.eksempel_fra()
                elif i==1:
                    eksempel = glose.eksempel_til()
                else:
                    continue

                print(eksempel)

            korrekthet = round(Score.beregn_fornuftig_score(svar, glose.ord_til()), 1)
            if korrekthet > 0.9:
                glose.forny_sist_løst()
            poeng = round(korrekthet,1)
            forventet_poeng += self.forventet_ant_poeng(glose.elo())

            if poeng==0:
                print(f"   {poeng:.1f}p - Feil. (svar: {', '.join(glose.ord_til())})")
            elif korrekthet<1:
                print(f"   {poeng:.1f}p - Delvis riktig. (svar: {', '.join(glose.ord_til())})")
            else:
                andre_svar = [ord for ord in glose.ord_til() if svar.lower() != ord.lower()]
                
                if len(andre_svar)>0:
                    print(f"   {poeng:.1f}p - Riktig! (eller: {', '.join(andre_svar)})", end="")
                else:
                    print(f"   {poeng:.1f}p - Riktig!", end="")
                print()

            self.ny_score(glose,poeng)

            tot_poeng += poeng

            hk, uk = glose.kategori().split("/")
            if hk not in resultat:
                resultat[hk] = {}
            if uk not in resultat[hk]:
                resultat[hk][uk] = [0,0]

            resultat[hk][uk][0] += poeng
            resultat[hk][uk][1] += 1

        print("\nPrøven er fullført.")
        input("Trykk enter for å se resultatet.\n")

        self.vis_resultat(resultat)
        
        if tot_poeng == len(self._gloser):
            print("\n")
            for blomstlinje in BLOMST_ASCII_BILDE.split("\n"):
                print(blomstlinje)
                time.sleep(0.04)
            print("\nFantastisk! Alt riktig!")
        else:
            print(f"\nTotalt fikk du {tot_poeng:.1f} poeng av {len(self._gloser)} mulige.", end="")
            print(f" Forventet score var {forventet_poeng:.1f} poeng.\n")
                
            if tot_poeng>0.9*len(self._gloser):
                print(f"Gratulerer! Dette kan du!:D")
            elif tot_poeng>0.8*forventet_poeng or tot_poeng>0.5*len(self._gloser):
                print("Du er på rett vei!:D Fortsett slik!")
            else:
                print("Herfra kan det bare gå oppover! Lykke til videre!:D")

    def vis_resultat(self, resultat):

        linjer = [["Kategori", "Poeng", "Totalt", "Ratio (%)"]]

        for hk,hkat in resultat.items():
            hkpoeng = sum(ukat[0] for ukat in hkat.values())
            hktot = sum(ukat[1] for ukat in hkat.values())

            linjer.append([hk,f"{hkpoeng:.1f}", f"{hktot}", f"{100*hkpoeng/hktot:.0f}"])

            ukat_linjer = []
            for uk,ukat in hkat.items():
                poeng, tot = ukat
                ukat_linjer.append([f" /{uk}", f"{poeng:.1f}", f"{tot}", f"{100*poeng/tot:.0f}"])
            
            linjer += sorted(ukat_linjer, key=lambda x: (float(x[3]), float(x[2])), reverse=True)
        
        maks_rader = [max([len(linje[i]) for linje in linjer]) for i in range(4)]

        for i,linje in enumerate(linjer):
            if i==1 or (i>1 and linje[0][0] != " ") :
                print((sum(maks_rader) + 11)*"¨")

            for j,celle in enumerate(linje):
                mellomrom = (maks_rader[j]-len(celle))*' '
                if j==0 or i==0:
                    print(f" {celle}", end=mellomrom)
                else:
                    print(f" {mellomrom}", end=celle)

                if j<len(linje)-1:
                    print(" |", end="")
            print()

    def forventet_ant_poeng(self,score):
        exp = (3.5-score+math.log(len(self._gloser)+5)/2)/2.5
        return 1/(1+10**exp)

    def ny_score(self,glose,korrekthet):
        score = glose.elo()
        poeng_score = 2.5*(korrekthet-self.forventet_ant_poeng(score))

        ny_score = round(max(min(poeng_score+score,10),1),1)
        glose.sett_elo(ny_score)
    
        forbedring = ny_score - score
        if forbedring>0:
            return f"+{forbedring:.1f}"
        return f"{forbedring:.1f}"
    

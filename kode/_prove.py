import numpy as np
import math
import random

class Prove:

    def __init__(self,  datasenter, elo, fra, til, gloser, antall):
        self._datasenter = datasenter

        self._sprak_fra = fra
        self._sprak_til = til
        self._gloser = gloser
        self._antall = min(antall,len(self._gloser))
        self._elo = elo

    def start(self):
        
        print(f"Oversett følgende fra {self._sprak_fra} til {self._sprak_til}. Trykk enter for å få eksempel til et ord.")

        forventet_poeng = 0
        tot_poeng = 0
        random.shuffle(self._gloser)

        resultat = {}

        print(f"\nDet er til sammen {self._antall} spørsmål.")
        for i,glose in enumerate(self._gloser[:self._antall]):

            if (i % 10)==0:
                print(f"\nGloser {i+1} - {min((i+10),self._antall)}:")

            delingstall = 1
            i = -1
            while True:
                i += 1
                skal_oversettes = '/'.join(self.sensurer_gloser(glose.hent_ord(self._sprak_fra)))
                svar = input(f" {skal_oversettes}: ")

                if svar!="":
                    break

                if i==0:
                    eksempel = glose.hent_eksempel(self._sprak_fra)
                    delingstall = 2
                elif i==1:
                    eksempel = glose.hent_eksempel(self._sprak_til, skjul_ord=True)
                    delingstall = 3
                else:
                    continue

                print(eksempel)

            korrekthet = round(self.korrekthet(svar,glose.hent_ord(self._sprak_til)),1)
            poeng = round(korrekthet/delingstall,1)
            forventet_poeng += self.forventet_ant_poeng(glose.hent_elo(self._sprak_fra))

            if poeng==0:
                print(f"   {poeng:.1f}p - Feil. (svar: {', '.join(glose.hent_ord(self._sprak_til))})")
            elif korrekthet<1:
                print(f"   {poeng:.1f}p - Delvis riktig. (svar: {', '.join(glose.hent_ord(self._sprak_til))})")
            else:
                andre_svar = [ord for ord in glose.hent_ord(self._sprak_til) if svar.lower()!=ord.lower()]
                
                if len(andre_svar)>0:
                    svar = input(max(1,len(skal_oversettes)-4)*" "+ "[evt]: ")
                    
                    korrekthet = round(self.korrekthet(svar, andre_svar), 1)
                    poeng2 = round(korrekthet/delingstall,1)

                    if poeng2 > 0.7:
                        print(f"   {poeng:.1f}p + {poeng2:.2f}p - Veldig bra!", end="")
                        if korrekthet == 1:
                            andre_svar = [ord for ord in andre_svar if svar.lower()!=ord.lower()]
                    else:
                        print(f"   {poeng:.1f}p + {poeng2:.2f}p!")
                        
                    if len(andre_svar) > 0: 
                        print(f" (eller: {', '.join(andre_svar)})", end="")
                else:
                    print(f"   {poeng:.1f}p - Riktig!", end="")
                print()

            if self._elo:
                self.ny_score(glose,poeng)

            tot_poeng += poeng

            kategorier = glose.hent_kategorier()
            for kat in kategorier:
                hk, uk = kat.split("/")
                if hk not in resultat:
                    resultat[hk] = {}
                if uk not in resultat[hk]:
                    resultat[hk][uk] = [0,0]

                resultat[hk][uk][0] += poeng
                resultat[hk][uk][1] += 1

        print("\nPrøven er fullført.")
        input("Trykk enter for å se resultatet.\n")

        self.vis_resultat(resultat)
        
        print(f"\nTotalt fikk du {tot_poeng:.1f} poeng av {self._antall} mulige.", end="")
        if self._elo:
            print(f" Forventet score var {forventet_poeng:.1f} poeng.\n")
            
        if tot_poeng>0.9*self._antall:
            print(f"Gratulerer! Dette kan du!:D")
        elif tot_poeng>0.8*forventet_poeng or tot_poeng>0.5*self._antall:
            print("Du er på rett vei!:D Fortsett slik!")
        else:
            print("Herfra kan det bare gå oppover! Lykke til videre!:D")

    def sensurer_gloser(self, ord):
        valgt_ord = random.choice(ord)

        nye_ord = [valgt_ord]
        for annnet_ord in ord:
            if annnet_ord == valgt_ord:
                continue
            s = ""
            indekser = set(random.sample(range(len(annnet_ord)), len(annnet_ord)//2))
            for i,tegn in enumerate(annnet_ord):
                if tegn != " " and i in indekser:
                    s += "_"
                    continue
                s += tegn

            nye_ord.append(s)
        return nye_ord

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

    def korrekthet(self,ord,fasiter):
        avvik = min(self.avstand_fra_fasit(ord.lower(),fasit.lower())/len(fasit) for fasit in fasiter)
        
        korrekthet = max((0,1-avvik*2))
        return korrekthet

    def avstand_fra_fasit(self,ord,fasit):
        n = len(ord)
        m = len(fasit)

        D = np.full((n+1,m+1), np.nan)

        def avstand_rek(i,j):
            
            if not math.isnan(D[i,j]):
                return D[i,j]
        
            if i==0 or j==0:
                D[i,j] = max(i,j)
            elif ord[i-1]==fasit[j-1]:
                D[i,j] = avstand_rek(i-1,j-1)
            else:
                D[i,j] = min(
                    avstand_rek(i-1,j-1)+1,
                    avstand_rek(i,j-1)+1,
                    avstand_rek(i-1,j)+1,
                )

                if min(i,j)>=2 and ord[i-2:i]==fasit[j-1:j-3:-1]:
                    D[i,j] = min(
                        D[i,j],
                        avstand_rek(i-2,j-2)+1,
                    )

            return D[i,j]

        return avstand_rek(n,m)

    def forventet_ant_poeng(self,score):
        exp = (3.5-score+math.log(len(self._gloser)+5)/2)/2.5
        return 1/(1+10**exp)

    def ny_score(self,glose,korrekthet):
        score = glose.hent_elo(self._sprak_fra)
        poeng_score = 2.5*(korrekthet-self.forventet_ant_poeng(score))

        ny_score = round(max(min(poeng_score+score,10),1),1)
    
        if self._elo:
            glose.sett_elo(self._sprak_fra, ny_score)
    
        forbedring = ny_score - score
        if forbedring>0:
            return f"+{forbedring:.1f}"
        return f"{forbedring:.1f}"
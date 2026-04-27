import numpy as np
import math

class Score:

    @staticmethod
    def beregn_fornuftig_score(ord, fasiter):
        return max(
            Score.__bokstaver_unna_fasit_vektet(ord, fasiter),
            Score.__splittinger_unna_fasit_vektet(ord, fasiter),
        )
    
    @staticmethod
    def __bokstaver_unna_fasit_vektet(ord, fasiter):
        avvik = min(Score.__bokstaver_unna_fasit(ord.lower(), fasit.lower())/(len(fasit)*1.1) for fasit in fasiter)
        korrekthet = max((0,1-avvik*1.8))
        return korrekthet

    @staticmethod
    def __bokstaver_unna_fasit(ord, fasit):
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
        
    @staticmethod
    def __splittinger_unna_fasit_vektet(ord, fasiter):
        substringer = lambda *ls: set(s[start:slutt+1] for s in ls for start in range(len(s)) for slutt in range(start,len(s)))

        max_score = 0
        for fasit in fasiter:
            deler = Score.__splittinger_unna_fasit(substringer, ord, fasit)

            for (ant_umatch1, tot_umatch1), (ant_umatch2, tot_umatch2), (ant_match, tot_match) in deler:
                if ant_match == 0:
                    continue

                score = (1-ant_match/tot_match) - (ant_umatch1*tot_umatch1*0.75)/len(ord) - (0 if len(fasit) == 0 else (ant_umatch2*tot_umatch2*0.75)/len(fasit))
                max_score = max(max_score, score) 

        return min(1, max_score)
    
    @staticmethod
    def __splittinger_unna_fasit(substringer, ord, fasit):
        deler = []

        def _rek_(s1,s2, alle_felles): 
            felles = substringer(*s1).intersection(substringer(*s2))
            if len(felles) == 0:
                deler.append((
                    (len(s1), sum(len(e) for e in s1)),
                    (len(s2), sum(len(e) for e in s2)),
                    (len(alle_felles), sum(len(e) for e in alle_felles))
                ))
                return
            største = max(felles, key=len)

            s1pos = [(s_i,i) for s_i,s in enumerate(s1) for i in range(len(s)) if s[i:i+len(største)] == største]
            s2pos = [(s_i,i) for s_i,s in enumerate(s2) for i in range(len(s)) if s[i:i+len(største)] == største]

            for s1_i, i1 in s1pos:
                ny_s1 = s1.copy()
                ny_s1.append(ny_s1[s1_i][:i1])
                ny_s1.append(ny_s1[s1_i][i1+len(største):])
                ny_s1.pop(s1_i)
                for s2_i, i2 in s2pos:
                    ny_s2 = s2.copy()
                    ny_s2.append(ny_s2[s2_i][:i2])
                    ny_s2.append(ny_s2[s2_i][i2+len(største):])
                    ny_s2.pop(s2_i)

                    _rek_(
                        [e for e in ny_s1 if e != ''],
                        [e for e in ny_s2 if e != ''],
                        alle_felles+[største]
                    )

        _rek_([ord], [fasit], [])
        return deler

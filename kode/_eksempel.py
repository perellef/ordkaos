
class Eksempel:

    def __init__(self, eksempel):
        self._eksempel = eksempel

    def hent_eksempel(self, skjul_ord=False):

        if not skjul_ord:
            return self._eksempel
        
        eksempel = ""

        censored = False
        for character in self._eksempel:
            if character == "]":
                censored = False
                continue
            elif character=="[":
                eksempel += "______"
                censored = True
                continue
            elif censored:
                continue
            eksempel += character
        
        return eksempel

class Ordliste:

    def __init__(self, øvre_marg, ufullstendig_data, glosegrupper, parse_errors):
        self.__øvre_marg = øvre_marg
        self.__ufullstendig_data = ufullstendig_data
        self.__glosegrupper = glosegrupper
        self.__parse_errors = parse_errors

    def øvre_marg(self):
        return self.__øvre_marg
    
    def ufullstendig_data(self):
        return self.__ufullstendig_data
    
    def glosegrupper(self):
        return self.__glosegrupper
    
    def parse_errors(self):
        return self.__parse_errors

    def __iter__(self):
        return iter(self.__glosegrupper)
    
    def __len__(self):
        return len(self.__glosegrupper)
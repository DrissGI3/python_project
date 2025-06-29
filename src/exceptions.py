class LivreEmprunteError(Exception):
    def __init__(self, message):
        super().__init__(message)

class LivreRendreError(Exception) :
    def __init__(self, message):
        super().__init__(message)

class LivreAjoutError(Exception) :
    def __init__(self, message):
        super().__init__(message)

class LivreQuantityError(Exception) :
    def __init__(self, message):
        super().__init__(message)

class LivreSupprimerError(Exception) :
    def __init__(self, message):
        super().__init__(message)
        
class MembreAjoutError(Exception) :
    def __init__(self, message):
        super().__init__(message)

class MembreEmpruntError(Exception) :
    def __init__(self, message):
        super().__init__(message)

class MembreRendreError(Exception) :
    def __init__(self, message):
        super().__init__(message)

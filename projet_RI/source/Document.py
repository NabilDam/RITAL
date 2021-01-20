
class Info:
    """
    Une classe abstraite Info qui nous sert a stocker les element indispensable d'une page,
    C'est a dire un ID et un texte
    """

    def __init__(self):
        self.identifiant = -1 
        self.texte = ""
    
    def setID(self, identifiant):
        self.identifiant = identifiant
    
    def getID(self):
        return self.identifiant
    
    def setTexte(self, texte):
        self.texte = texte

    def addTexte(self, texte):
        self.texte += texte

    def getTexte(self):
        return self.texte


class Document(Info):
    """
        La classe qui permet de stocker un document, herite de la class Info,
    possède des liens entre les documents 
    """

    def __init__(self):
        super().__init__()
        self.linkTo = dict()
        self.linkFrom = list()

    def addLinkTo(self, idDoc):
        self.linkTo[idDoc] = self.linkTo.get(idDoc, 0) + 1

    def getHyperlinksTo(self):
        return self.linkTo

    def setLinkFrom(self, listFrom):
        self.linkFrom = listFrom

    def getHyperlinksFrom(self):
        return self.linkFrom


class Query(Info):
    """
        La classe qui permet de stocker une Query, herite de la class Info,
    possède une liste des resultat attendu pour la requête
    """


    def __init__(self):
        super().__init__()
        self.listPertinent = list()

    def addPertinent(self, idDoc):
        self.listPertinent.append(idDoc)

    def getPertinents(self):
        return self.listPertinent


class Document:
    def __init__(self):
        self.identifiant = -1 
        self.texte = ""
        
    
    def setID(self,identifiant):
        
        self.identifiant = identifiant
    
    def getID(self):
        return self.identifiant 
        
    
    def setTexte(self,texte):
        self.texte = texte
        
        
    def getTexte(self):
        return self.texte
    
    
    
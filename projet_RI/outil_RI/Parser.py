import re
from Document import Document 


class Parser:
    
    def buildDocCollectionSimple(fichier):
    
        resultat = dict()
        lireID = ""
        text =""
        inT = False
        d = Document()
        f = open(fichier,'r')
        for l in f.readlines():
            
            if inT:
                if l.startswith("."):
                    inT = False
                    d.setTexte(text)
                    resultat[lireID[:-1]] = d
                    lireID = ""
                else:
                    text = text + l 
                
            if len(lireID)>0:
                if l.startswith(".T"):
                    inT = True
                    text =""
                
            if l[:2] == ".I":
                lireID = l[3:]
                d = Document()
                d.setID(int(lireID))
                resultat[lireID[:-1]] = ""
            
    
        f.close()
        return resultat

    

    def buildDocumentCollectionRegex(self):
        
        resultat = dict()
        
        f = open(self.file,'r')
        doc = f.read()
        docs = doc.split(".I")
    
        for di in range(1,len(docs)):  
            d = Document()
            id_doc = re.search(r'(\d*|$)',docs[di][1:]).group(0)
            d.setID(int(id_doc))
            m = re.search(r'\.T(.*?)\.',docs[di],re.DOTALL)
            if m != None:
                d.setTexte( m.group(1).replace('\n',' '))
                
            else:
                d.setTexte("")
            
            resultat[id_doc]= d
        f.close()
        return resultat
        
        
            
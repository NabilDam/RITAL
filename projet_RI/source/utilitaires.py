from collections import Counter
import porter
import re
import math
from IndexerSimple import IndexerSimple
from Parser import Parser

doc1 = "the new home has been saled on top forecasts"
doc2 = "the home sales rise in july"
doc3 ="there is an increase in home sales in july"
doc4 ="july encounter a new home sales rise"
D = [doc1,doc2,doc3,doc4]
motvide = ["the", "a", "an", "on", "behind", "under", "there", "in", "on"]



"""   FONCTIONS UTILES TME1   """
def countWord(doc):
    return dict(Counter([porter.stem(i.lower()) for i in doc.split() if i.lower() not in motvide]))


def index(D):
    index=dict()
    index_inv=dict()
    
    for i in range(len(D)):
        
        index[i] = countWord(D[i])
        for j in index[i]:
            if j in index_inv:
                index_inv[j][str(i)] = str(index[i][j])
            else:
                index_inv[j] = {str(i):str(index[i][j])}
    
    return (index,index_inv)

def index_tfidf(D):
    
    index=dict()
    index_inv=dict()
    tf_idf = dict()
    for i in range(len(D)):
        
        index[i] = countWord(D[i])
        for j in index[i]:
            if j in index_inv:
                index_inv[j][str(i)] = str(index[i][j])
            else:
                index_inv[j] = {str(i):str(index[i][j])}
    
    for i in index:
       tf_idf[i] = {mot:(index[i][mot]/len(index[i]))*math.log((1+len(D))/(1+len(index_inv[mot]))) for mot in index[i]}
    
    return (index,index_inv,tf_idf)

ind = index_tfidf(D)

def buildDocCollectionSimple(nom):
    
    resultat = dict()
    lireID = ""
    inT = False
    
    f = open(nom,'r')
    for l in f.readlines():
        
        if inT:
            if l.startswith("."):
                inT = False
                lireID = ""
            else:
                resultat[lireID[:-1]] = resultat[lireID[:-1]] + l
            
        if len(lireID)>0:
            if l.startswith(".T"):
                inT = True
            
        if l[:2] == ".I":
            lireID = l[3:]
            resultat[lireID[:-1]] = ""
        

    f.close()
    return resultat
   
#r = buildDocCollectionSimple("cacmShort-good.txt")
    

def buildDocumentCollectionRegex(nom):
    
    resultat = dict()
    
    f = open(nom,'r')
    doc = f.read()
    docs = doc.split(".I")
    for d in range(1,len(docs)):        
        id_doc = re.search(r'(\d*|$)',docs[d][1:]).group(0)
        m = re.search(r'\.T(.*?)\.',docs[d],re.DOTALL)
        if m != None:
            resultat[id_doc] = m.group(1).replace('\n',' ')
        else:
            resultat[id_doc]=""
    
    return resultat
    
    
#r = buildDocumentCollectionRegex("cacmShort-good.txt")


"""   FONCTIONS UTILES TME2   """


"""Exercice 1 : Q1_ Quels index faut-il interroger pour avoir un calcul du score pertinent? 
              -> Il faut interroger l'index classique de la collection. Pour chaque doc on calcul le score de pertinence.
"""




def evaluation_modele_binaire(D,qry):
    
    ind = index(D)[0]
    
    score = dict()
    for i in ind:
        score[i]=0
        for j in qry.split():
            if porter.stem(j) in ind[i]:
                score[i]+=1
        if len(qry.split())==score[i]:
            score[i] = 1 
        else:
            score[i] = 0
    return score
    
print(evaluation_modele_binaire(D,"home sales top"))
    


def evaluation_modele_vectoriel(D,qry):
    
    qry = [porter.stem(mot) for mot in qry.split()]
    ind = index(D)
    
    score = dict()
    
    for doc in ind[0]:
        score[doc]=0
    
    for mot in qry:
        for docu in ind[1][mot]:
            score[int(docu)]+=int(ind[1][mot][docu])
            
    return score
    
    
    
print("evaluation_modele_vectoriel",end=" : ")
print(evaluation_modele_vectoriel(D,"home sales top"))
    

    
    
    
    












import re
import Document


class Parser:

    @staticmethod
    def buildDocCollectionSimple(fichier, baliseText='.T', pageRank=False):
        """
            Construit l'index a partir d'une base de documents contenus dans fichier,
        On lit les lignes du fichier une par une, et on repère les balises texte .T
        et les balises id .I (les balises texte pour une requete sont .W)

        :type fichier: String
        :param fichier: Le fichier qui contient les documents que l'on veut indexé

        :type baliseText: String
        :param baliseText: La balise que l'on va utilier pour recuperer le texte, .T pour un doc, .W pour une requête

        :type pageRank: boolean
        :param pageRank: Un boollean qui nous indique si l'on doit se préoccuper des balise .X, ie si on travail avec un Document

        :return: Un dictionnaire de d'object Document, dont les clef sont les id des
                Document.
                {"id1": Document1, "id2": Document2, ...}
        """

        resultat = dict()
        lireID = -1
        linkFrom = dict()
        inT = False  # Boolean qui nous indique si l'on est dans une balise texte
        inX = False  # Boolean qui nous indique si l'on est dans une balise link
        f = open(fichier, 'r')
        for l in f.readlines():  # Pour chaque ligne du fichier

            if l.startswith(baliseText):
                inT = True
                inX = False

            elif l.startswith('.X') and baliseText == '.T':
                inT = False
                inX = True

            elif l.startswith('.I'):
                lireID = int(l[3:])
                d = Document.Document() if baliseText == '.T' else Document.Query()
                d.setID(lireID)  # Auquel on lui donne son id
                resultat[lireID] = d
                inT = False
                inX = False

            elif l.startswith('.'):
                inT = False
                inX = False

            elif inT:  # Si on est dans une balise de texte
                resultat[lireID].addTexte(l)

            elif inX and l != '\n':  # Si on est dans une balise de link
                fromId = int(re.findall('\d+', l)[0])
                resultat[lireID].addLinkTo(fromId)
                linkFrom[fromId] = linkFrom.get(fromId, []) + [lireID]

        f.close()

        if not pageRank:
            return resultat
        else:
            for idDoc in linkFrom:
                resultat[idDoc].setLinkFrom(linkFrom[idDoc])
            return resultat

    @staticmethod
    def buildDocumentCollectionRegex(fichier):
        """
            Construit l'index a partir d'une base de documents contenus dans fichier,
        On lit le fichier en entier et on utilise des expressions régulières pour
        récupère le contenu des balises

        :type fichier: String
        :param fichier: Le fichier qui contient les documents que l'on veut indexé

        :return: Un dictionnaire de d'object Document, dont les clef sont les id des
                Document.
                {"id1": Document1, "id2": Document2, ...}
        """
        resultat = dict()
        
        f = open(fichier, 'r')
        doc = f.read()
        docs = doc.split(".I")
    
        for di in range(1, len(docs)):
            d = Document.Document()
            id_doc = re.search(r'(\d*|$)', docs[di][1:]).group(0)
            d.setID(int(id_doc))
            m = re.search(r'\.T(.*?)\.', docs[di], re.DOTALL)
            if m is not None:
                d.setTexte(m.group(1).replace('\n', ' '))
                
            else:
                d.setTexte("")
            
            resultat[id_doc] = d
        f.close()
        return resultat

    @staticmethod
    def buildQueryCollection(fichierQry, fichierRel=None):
        """
            On donne les fichiers query et rel en entrée et cette fonction en 
            construit une collection
        """

        if fichierRel is None:
            fichierRel = fichierQry + '.rel'
            fichierQry = fichierQry + '.qry'

        collection = Parser.buildDocCollectionSimple(fichierQry, ".W")
        Parser.buildPertinenceQuery(collection, fichierRel)

        return collection

    @staticmethod
    def buildPertinenceQuery(collection, fichierRel):
        """
            Lit ligne par ligne et ajoute à un objet query sa liste de documents pertinants. 
        """

        f = open(fichierRel, 'r')
        for ligne in f.readlines():  # Pour chaque ligne du fichier

            pertinence = [int(n) for n in re.findall('\d+', ligne)]
            collection[pertinence[0]].addPertinent(pertinence[1])



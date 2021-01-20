import IRModel
import EvalIRModel
import random


class PageRank(IRModel.IRModel):

    def __init__(self, weighter, model, damping=0.8, n=10, k=5):

        self.weighter = weighter
        self.model = model
        self.d = damping
        self.n = n
        self.k = k

    def getScores(self, Query, max_iter=200):

        seed = self.model.getRanking(Query)
        norm = sum([page[1] for page in seed[:min(self.n, len(seed))]])
        seed = {page[0]: (1 - self.d) * (page[1] / norm) for page in seed[:min(self.n, len(seed))]}

        graphe = self._initialiseGraphe(seed)
        resultat = dict.fromkeys(graphe.keys(), 0)

        for _ in range(max_iter):

            for page in resultat:
                score = 0

                for pageFrom in graphe[page]:
                    score += resultat.get(pageFrom, 0) / len(self.weighter.getHyperlinksTo(pageFrom))
                resultat[page] = seed.get(page, 0) + (self.d * score)

        return resultat

    def _initialiseGraphe(self, seed):
        """
            Fonction qui a partir des seed contruie le graphe que l'on va parcourir pour le pageRank
        On ajoute tout les page qui sont directement pointer par les pages seed, et on rajoute self.k
        page parmi toutes les pages qui pointe vers une page seed   
        
        :return: un dictionaire qui represente le graphe pour le pageRank
                {idPage: {idPage' qui sont pointer par idPage}}
        """

        graphe = dict()

        for idDoc in seed:
            graphe[idDoc] = set()
            for linkTo in self.weighter.getHyperlinksTo(idDoc):
                graphe[idDoc].add(linkTo)
                graphe[linkTo] = graphe.get(linkTo, set())

            linkFrom = self.weighter.getHyperlinksFrom(idDoc)

            for i in random.sample(linkFrom, min(len(linkFrom), self.k)):
                graphe[i] = graphe.get(i, set()) | {idDoc}

        return graphe
    
    def setParametre(self, damping):
        self.d = damping
    
    def findParametreOptimaux(self, listeParametre, Queries, metrique="FMesure"):
        """
           Optimise le parametre damping, en prenant la meuilleur valeur parmis les valeur de listeParametre
           
        :type listeParametre: list
        :param listeParametre: liste qui contient les differentes valeurs pour le damping

        :type Queries: dict = {id1: Query1, ...}
        :param Queries: Le dictionnaire des query qui nous serve d'entrainement

        :type metrique: String
        :param metrique: La metrique que l'on veux utiliser       
        """
        
        metriquePossible = {"Precision":0,  # La liste des metriques possible
                    "Rappel":1,
                    "FMesure":2,
                    "AvgP":3,
                    "reciprocalRank":4,
                    "Ndcg":5}
        
        metrique = metriquePossible[metrique]

        evaluation = EvalIRModel.EvalIRModel(Queries, self)
        
        scoreEvaluation = []
        for para in listeParametre:
            self.setParametre(para)
            scoreEvaluation.append(evaluation.evalModel())
        
        
        self.setParametre = listeParametre[scoreEvaluation.index(max(scoreEvaluation, key=lambda x: x[metrique][0]))]

    def __str__(self):
        return "Page Rank sur le " + str(self.model)


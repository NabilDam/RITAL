import Eval
import IndexerSimple
import IRModel
import PageRank
import Parser
import Weighter

import numpy as np


class EvalIRModel:

    def __init__(self, fichierQry, modelIR, k=5, beta=0.5, verbose=False):
        """
           Permet d'initialiser EvalIRModel
           
        :type fichierQry: String si fichier ou dict de Query = {id1: Query1, ...}
        :param fichierQry: le fichier ou sont stocker les queries, ou la collection qui contient tout les Queries 
                            qui vont nous servir pour evaluer le modèle
            
        :type modelIR: IRModel
        :param modelIR: Le modèle que l'on veux evaluer
    
        :type k: float
        :param k: parametre k pour les evaluations
        
        :type beta: float
        :param beta: parametre beta pour les FMesureAtK

        :type verbose: boolean
        :param verbose: boolean pour activer le mode verbeux
        """

        self.verbose = verbose
        self.k = k
        self.beta = beta

        self.model = modelIR

        self.collectionQry = Parser.Parser.buildQueryCollection(fichierQry) if type(fichierQry) is str else fichierQry
        self.print_verbose("Recuperation des queries effectué")

    def evalModel(self, k=None, beta=None):
        """
            Fontions qui nous permet d'evaluer le modèle self, un IRModel
        
        :type k: float
        :param k: parametre k pour les evaluations
        
        :type beta: float
        :param beta: parametre beta pour les FMesureAtK
        """

        if k is not None:
            self.k = k

        if beta is not None:
            self.beta = beta

        evaluation = [Eval.PrecisionAtK(self.k)
            , Eval.RappelAtK(self.k)
            , Eval.FMesureAtK(self.k, self.beta)
            , Eval.AvgP()
            , Eval.reciprocalRank()
            , Eval.Ndcg()]
        resultat = [[] for _ in range(len(evaluation))]

        for query in self.collectionQry:
            self.print_verbose('query =', self.collectionQry[query].getTexte())
            liste = [resultat[0] for resultat in self.model.getRanking(self.collectionQry[query].getTexte())]
            self.print_verbose(liste)
            for i in range(len(evaluation)):
                resultat[i].append(evaluation[i].evalQuery(liste, self.collectionQry[query]))
        self.print_verbose(resultat)
        return [(np.mean(l), np.std(l)) for l in resultat]

    def print_verbose(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)

    def __str__(self):
        return str(self.model)


class EvalAllIRModel:
    """
        Class qui va nous permettre d'evaluer, et d'optimiser, tous les modèles IRModel
    """

    def __init__(self, fichier, findParametre=False, metrique="FMesure", tailleTrain=0.65, verbose=False):
        """
           Permet d'initialiser EvalAllIRModel
           
        :type fichier: String 
        :param fichier: le fichier ou sont stocker les queries, 
            
        :type findParametre: boolean
        :param findParametre: boolean pour activer l'optimisation des parametres
        
        :type metrique: String
        :param metrique: La metrique que l'on veux utiliser  
                
        :type tailleTrain: float
        :param tailleTrain: la proportion de train sur l'ensemble des queries

        :type verbose: boolean
        :param verbose: boolean pour activer le mode verbeux
        """

        collection = Parser.Parser.buildDocCollectionSimple(fichier + '.txt', pageRank=True)
        self.collectionQry = Parser.Parser.buildQueryCollection(fichier)
        self.train = dict()
        self.verbose = verbose
        
        self.print_verbose("Initialisation")

        if findParametre:
            self.separeTrainTest(tailleTrain)

        index = IndexerSimple.IndexerSimple()
        index.indexation(collection)

        self.weighter = [Weighter.Weighter1(index), Weighter.Weighter2(index), Weighter.Weighter3(index),
                         Weighter.Weighter4(index), Weighter.Weighter5(index)]

        modelIR = [IRModel.Vectoriel, IRModel.Jelinek_Mercer, IRModel.Okapi]

        model = []

        for w in self.weighter:
            for m in range(len(modelIR)):
                
                if m == 1:  # pour le modèle Jelinek_Mercer
                    jelinek = modelIR[m](w)
                    if findParametre:
                        jelinek.findParametreOptimaux(np.arange(0, 1.4, 0.1), self.train, metrique)
                    model.append(jelinek)
                elif m == 2:  # pour le modèle Okapi
                    okapi = modelIR[m](w)
                    if findParametre:
                        okapi.findParametreOptimaux(np.arange(0, 0.5, 0.1), np.arange(1.5, 2, 0.1), self.train, metrique)
                    model.append(okapi)
                else:  # pour le modèle Vectoriel
                    model.append(modelIR[m](w))  # il n'y a pas de parametre a optimiser
                    model.append(modelIR[m](w,True))
        
        if findParametre:
            self.print_verbose("Tout les models Jelinek_Mercer et Okapi sont entrainer")
        self.model = []

        for m in model:
            self.model.append(EvalIRModel(self.collectionQry, m))
            
            pr = PageRank.PageRank(m.getWeighter(), m)
            if findParametre:
                pr.findParametreOptimaux(np.arange(0.85, 0.95, 0.05), self.train, metrique)
                
            self.model.append(EvalIRModel(self.collectionQry, pr))
        if findParametre:
            self.print_verbose("Tout les models PageRank sont entrainer")

        self.print_verbose("Initialisation terminer")



    def separeTrainTest(self, tailleTrain=0.8):
        """
            Permet de separe en deux groupes, teste et train les queries.
            
        :type tailleTrain: float
        :param tailleTrain: le pourcentage de query que l'on garde pour le train
        """
                
        tailleTrain = int(tailleTrain * len(self.collectionQry))

        for qry in self.collectionQry:
            self.train[qry] = self.collectionQry[qry]
            if len(self.train) > tailleTrain:
                break

        self.collectionQry = {k: v for k, v in self.collectionQry.items() if k not in self.train}

    def evalAllModel(self, k=1, beta=0.5):
        """
            Fontions qui nous permet d'evaluer tous les modèles qui sont dans self.model,
        c'est a dire tous les modèles IRModel
        
        :type k: float
        :param k: parametre k pour les evaluations
        
        :type beta: float
        :param beta: parametre beta pour les FMesureAtK
        """
        self.print_verbose("Evalutation")

        resultat = dict()
        for m in self.model:
            resultat[m] = m.evalModel(k, beta)


        precision = max(resultat.items(), key=lambda x: x[1][0][0])[0]
        rappel = max(resultat.items(), key=lambda x: x[1][1][0])[0]
        fmesure = max(resultat.items(), key=lambda x: x[1][2][0])[0]
        avgP = max(resultat.items(), key=lambda x: x[1][3][0])[0]
        reciprocalRank = max(resultat.items(), key=lambda x: x[1][4][0])[0]
        ndcg = max(resultat.items(), key=lambda x: x[1][5][0])[0]
        print('\nLe modèle qui a la plus grande Precision a', k, 'est le', precision, 'pour, \nprecision =', resultat[precision][0][0], "en moyenne\net std =", resultat[precision][0][1])
        print('\nLe modèle qui a le plus grand rappel a', k, 'est le', rappel, 'pour, \nrappel =', resultat[rappel][1][0], "en moyenne\net std =", resultat[rappel][1][1])
        print('\nLe modèle qui a la plus grande fmesure a', k, 'avec beta =', beta,'est le', fmesure, 'pour, \nfmesure =', resultat[fmesure][2][0], "en moyenne\net std =", resultat[fmesure][2][1])
        print('\nLe modèle qui a le plus grand avgP est le', avgP, 'pour, \navgP =', resultat[avgP][3][0], "en moyenne\net std =", resultat[avgP][3][1])
        print('\nLe modèle qui a le plus grand reciprocalRank est le', reciprocalRank, 'pour, \nreciprocalRank =', resultat[reciprocalRank][4][0], "en moyenne\net std =", resultat[reciprocalRank][4][1])
        print('\nLe modèle qui a le plus grand ndcg est le', ndcg, 'pour, \nndcg =', resultat[ndcg][5][0], "en moyenne\net std =", resultat[ndcg][5][1])

        return resultat
    
    def print_verbose(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)
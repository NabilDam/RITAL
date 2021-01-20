#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Parser import Parser

import EvalIRModel
import IndexerSimple
import IRModel
import PageRank
import Weighter


qry = "Computers in Inspection Procedures Science"

if __name__ == "__main__":

    data = "../data/cacm/cacm"
    data2 = "../data/cisi/cisi"

    evalue = EvalIRModel.EvalAllIRModel(data, findParametre=False, tailleTrain=0.5, verbose=True)
    evalue.evalAllModel(5)

    evalue = EvalIRModel.EvalAllIRModel(data, findParametre=True, tailleTrain=0.5, verbose=True)
    evalue.evalAllModel(5)

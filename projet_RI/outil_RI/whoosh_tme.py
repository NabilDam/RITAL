
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import whoosh
import whoosh.index
import os,os.path
from Parser import Parser
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.qparser import QueryParser
import shutil



schema = Schema(title=TEXT(stored=True), content=TEXT, path=ID(stored=True), tags=KEYWORD, icon=STORED)
shutil.rmtree('indexdir')
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = whoosh.index.create_in("indexdir",schema)

writer = ix.writer()
path = '../cacmShort-good.txt'





resultat = Parser.buildDocCollectionSimple(path)
for doc in resultat:

    writer.add_document(title=str(resultat[doc].getID()),content=resultat[doc].getTexte())

writer.commit()

searcher = ix.searcher()


parser = QueryParser("content", ix.schema)
myquery = parser.parse("Matrix")
results = searcher.search(myquery)


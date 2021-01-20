#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import elasticsearch as es
import elasticsearch.helpers as helpers

def bulking(texts, titles):
    bulk_data = []
    for i, (txt, title) in enumerate(zip(texts, titles)):
        data_dict = {
                    '_index': 'test-toto',
                    '_type': 'trec',
                    '_id': str(i),
                    '_source': {
                        "text": txt,
                        "title": title
                    }
                }
        bulk_data.append(data_dict)
    return bulk_data


engine = es.Elasticsearch()
index_name = "test-toto"
b = 0.5
k1 = 1
settings = {"settings": {
                "number_of_shards": 1,
                "index": {
                    "similarity": {
                        "default": {
                            "type":"BM25",
                            "b": b,
                            "k1": k1}
                            }
                        }
                    }
                }

engine.indices.create("{index_name}", body=settings) # commenter cette ligne après le premier lancement
                        
                        
texts = ['toto is now gone',
         'toto has left the place',
         "toto went to his parent's place",
         "toto's place is quite far away"]

titles = ["Toto's life", 
          "Toto leaving",
          "Toto's trip",
          "Toto is far"]

helpers.bulk(engine, bulking(texts, titles))

d= engine.search("test-toto", {"query": {"match": {"text": "toto place"}}})
hits = d['hits']['hits']

for h in hits :
    source = h['_source']
    title = source['text']
    score = h['_score']
    print(title, score)
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import sys



"""
#check if its valid in the server
print(es.ping())
#check all index mappings
valid_index = es.indices.get_alias("*")
for index_name in valid_index:
    print(index_name)
#view documents
curl 'localhost:9200/_cat/indices?v'
#search mapping
body =
    {
        "settings:" : {'number_of_shards' : 1, 'number_of_replicas' : 0 }
        "query" :
        {
            "match" : 
            {
                "mesh_headings" : mesh_term
            }
        }
    }
    USE THIS TO CHANGE THE NUMBER OF RESPONSES IN FUNCTION
    #splice out how many hits we want
    s = s[0:docs]
    response = s.execute()
    #change this to specify depth
    return response.to_dict()['hits']['hits']
"""

es = Elasticsearch()

def elasticsearch_query(mesh_term:str, docs:int) -> list:
    """ 
    generator: returns docs from elasticsearch given mesh term
    @param mesh_term is the mesh term that is going to be looked up
    @param docs is the batch
    @return dict is the publications with the mesh term
    """
    request_body = {
                "query":
                {
                    "match" :
                    {
                        "MeSH" : mesh_term
                    }
                }
            }


    #use search from elastic search dsl
    s = Search(index="pubmed",using=es).update_from_dict(request_body)

    data = []

    #unpack the scan
    for index, hit in enumerate(s.scan()):

        #if the list is not yet full with the specified docs number
        if index % docs != 0 or index == 0:
            data.append(hit.to_dict())

        # index % docs = 0 means index is a multiple of docs (in this case it is docs)
        else:
            yield json.dumps(data) + "\n"
            data = []
            data.append(hit.to_dict())
            print('sent')


    #if batch is 300 and we only have 280, modulo is not zero, but the for loop breaks
    if data:
        yield json.dumps(data) + "\n"


if __name__ == "__main__":
    for index, i in enumerate(elasticsearch_query("Cardiomyopathies", 3)):
        if index < 5:
            print(len(i))
            print("\n")
        else:
            break

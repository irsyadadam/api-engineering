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

"""

es = Elasticsearch()

def elasticsearch_query(mesh_term:str, docs:int) -> list:
    """ 
    looks at elasticsearch and returns the first instance of the search
    @param mesh_term is the mesh term that is going to be looked up
    @param docs is the batch
    @return list is the list of pubmeds specified in query
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
    s = s[0:docs]
    response = s.execute()

    #change this to specify depth
    return response.to_dict()['hits']['hits']

if __name__ == "__main__":
    hello = elasticsearch_query("Cardiomyopathies", 2)
    print(str(hello))

from flask import Flask, request, jsonify
import requests
import ast
import json

from libs.extract_mesh import read_mesh_data, extract_mesh_term_and_id
from libs.elasticsearch_lookup import elasticsearch_query

"""
Notes:
@shell:
conda env list
On virtual environment, only library installed is flask + dependencies
    @shell:
    conda list
Everything is to run on shell. To run app:
    @shell:
    export FLASK_APP=flask_app.py 
    flask run 
NOTE: Make sure you aeete in directory of flask app to export it!!
---------------------------------
client -- requests library --> flask server <-- http response --> view function {return data}
"""

#init the app
app = Flask(__name__)
#app.debug = True

#import the mesh data in dict
print("---loading mesh terms---")
mesh_data = read_mesh_data("mesh_data.xml")
mesh_id_to_term_map = extract_mesh_term_and_id(mesh_data)
assert mesh_id_to_term_map["D009202"] == "Cardiomyopathies"
print("----------done----------")

def check_mesh(mesh_term:str) -> bool:
    """
    check if a mesh term is in mesh dict
    @param the mesh_term
    @returns bool
    """
    return mesh_term in mesh_id_to_term_map

def check_docs(docs:int) -> bool:
    """
    checks batch request
    @param int is the batch request
    @return bool if valid request
    """
    return docs >= 1 and docs <= 500    

def batch_elasticsearch(mesh_request:str, doc_request:int) -> dict:
    """
    returns a number of documents from the elasticsearch query
    @param mesh_request is the mesh tmer
    @param docs is the batch request
    @returns a list of docs
    """
    return elasticsearch_query(mesh_id_to_term_map[mesh_request], doc_request)


#valid request is http://34.217.174.15:5000/api/data/pubmed_central?mesh=100&docs=10
@app.route("/api/data/pubmed_central/", methods=["GET"])
def mesh_docs():
    """
    returns data associated with mesh term
    @param mesh term specified by enpoint
    @param docs is the batch request specified by the endpoint
    @returns the document mapping associated with the mesh term
    """
    #parse request
    mesh = request.args.get("mesh")
    doc = request.args.get("docs")

    #checks if valid mesh term and batch request
    if check_mesh(mesh) and check_docs(int(doc)):
        #return data using elasticsearch
        return jsonify(batch_elasticsearch(mesh, int(doc)))

    else:
        #return str("sad :(")
        return "invalid mesh term/batch request"

#if the request didn't go through
@app.errorhandler(404)
def error(error):
    return "invalid url/endpoint, request url: http://34.217.174.15:5000/api/data/pubmed_central", 404

if __name__ == "__main__":
    #run python file while app is running to run debug mode
    app.run(host='0.0.0.0', port=5000)

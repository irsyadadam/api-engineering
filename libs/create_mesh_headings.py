import os
import json
import ast

filename = "/home/ubuntu/caseolap/data/mesh_headings_in_pubmed.txt"


def create_dict(filename) -> dict:
    """
    creates a json file of headings
    """
    index = 1
    #create empty dict
    dict_headings = {}
    with open(filename, 'r') as f:
        #line is a list
        for line in f:
            #string representation of a list to a list
            line = ast.literal_eval(line)
            for i in line:
                dict_headings[i] = index 
                index += 1
    with open('mesh_headings.json', 'w') as fp:
        json.dump(dict_headings, fp)


if __name__ == "__main__":
    hello = create_dict(filename)

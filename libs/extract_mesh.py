"""
Script to download and parse all the mesh terms hosted by nih.
All of the mesh terms are download from 
'https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/desc2021.xml',
if there is a new release you should check the file listing at 
'https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/', for a new version.
The script works in the following way:
1. A get request is sent to the first url and the text contents are
 saved to a file with the name "mesh_data.xml"
2. The data is then read into an ElementTree using the python xml 
library that is included with python. More information can be found
on the xml library that comes with python at
 'https://docs.python.org/3/library/xml.etree.elementtree.html'
3. We iterate over every element that has a 'DescriptorRecord' tag
and grab every mesh term and id from the element.
The data we are interested specfically has a format located toward
 the bottom of this doc string. This was inferred by looking through
 a few tags in the browser and verifying that the element had a mesh
 term and id that we could search.
EXAMPLE XML ELEMENT WE ARE INTERESTED IN:
<DescriptorRecord DescriptorClass = "1">
  <DescriptorUI>D000001</DescriptorUI>
  <DescriptorName>
   <String>Calcimycin</String>
  </DescriptorName>
.
.
.
The rest of the xml tag is omitted.
  
"""

import requests as req
from xml.etree import ElementTree


def download_mesh_data(file_name):
    zipped_data = req.get("https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/desc2021.xml")
    with open(file_name, "w") as xml_file:
        xml_file.write(zipped_data.text)

def read_mesh_data(file_name):
    with open(file_name, "r") as xml_file:
        xml_data = ElementTree.parse(file_name)
        elements = [elem for elem in xml_data.iter()]
        descriptor_tags = filter(lambda x: x.tag == "DescriptorName", elements)
        descriptor_tags = list(descriptor_tags)
        return xml_data

def extract_mesh_term_and_id(xml_data):
    data = {}
    for elem in xml_data.iterfind("DescriptorRecord"):
        descriptor_name_tag = elem.find("DescriptorName")
        descriptor_name_text_tag = descriptor_name_tag.find("String")
        descriptor_id_tag = elem.find("DescriptorUI")
        mesh_term = descriptor_name_text_tag.text
        mesh_term_id = descriptor_id_tag.text
        data[mesh_term_id] = mesh_term
    return data
    
if __name__ == "__main__":
    #download_mesh_data("mesh_data.xml")
    mesh_data = read_mesh_data("mesh_data.xml")
    mesh_id_to_term_map = extract_mesh_term_and_id(mesh_data)
    assert mesh_id_to_term_map["D009202"] == "Cardiomyopathies"
    

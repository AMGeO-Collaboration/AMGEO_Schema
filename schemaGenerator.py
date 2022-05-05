import os
import xarray
from SchemaBuilder import *
import xml.etree.cElementTree as ET
from datetime import date



def autoSchemaGenerator(rootName,folder,urlBase):
    files = []
    
    
    root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    today = date.today().strftime("%Y-%m-%d")
    
    for file in os.listdir(folder):
        if file.endswith(".nc"):
            files.append(file)

    for file in files:
        currdata = xarray.open_dataset(folder+"/"+file)
        schema = SchemaBuilder(data=currdata)
        schema.add_url( urlBase+"/static/data/"+file[:file.index('.nc')]+".html"
                       ,urlBase+"/static/data/"+file)
        html = schema.to_html(template="google/visual-dataset.html")
        filew = open(folder+"/data-"+file[:file.index('.nc')]+".html","w")
        html = html.replace('"@context": "https://www.schema.org"','"@context": "https://schema.org/"')
        filew.write(html)
        filew.close()
       
        doc = ET.SubElement(root, "url")
        
        ET.SubElement(doc, "loc").text = urlBase+"/static/data/data-"+file[:file.index('.nc')]+".html"
        ET.SubElement(doc, "lastmod").text = today
        


    tree = ET.ElementTree(root)
    #ET.indent(tree, space="\t", level=0)
    tree.write( rootName+"/sitemap.xml",encoding = "UTF-8", xml_declaration = True)

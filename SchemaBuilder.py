import numpy as np
from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema
from schemaorg.templates.google import make_dataset

default_properties = {
        "about": "Test AMGeO Schema",
        "citation": "Matsuo, T., Kilcommons, L. M., Ruohoniemi, J. M., and Anderson, B. J., “Assimilative Mapping of Geospace Observations (AMGeO): Data Science Tools for Collaborative Geospace Systems Science”, vol. 2019, 2019.",
        "url": "https://amgeo.colorado.edu",
        "name": "AMGeO Result"
}


class SchemaBuilder:
    def __init__(self,data=None):
        self.schema = Schema("Dataset")
        self.add_property_set(default_properties)
        self.data = data
        if(data):
            dataTime = str(data.coords['time'].values[0])
            self.add_property("temporalCoverage",dataTime)
            
            
            dumSpatialMin = Schema("Place")
            dumSpatialMax = Schema("Place")
            minLat = min(data.coords['lat'].values)
            minLon = min(data.coords['lon'].values)
            
            maxLat = max(data.coords['lat'].values)
            maxLon = max(data.coords['lon'].values)
            
            dumSpatialMin.add_property("latitude",minLat)
            dumSpatialMin.add_property("longitude",minLon)

            dumSpatialMax.add_property("latitude",maxLat)
            dumSpatialMax.add_property("longitude",maxLon)

            
            

            self.add_property("name",data.attrs['description']+ " for " + dataTime)
            self.add_property("version",data.attrs['version'])
            self.add_property("about",data.attrs['description'])
            self.add_property("spatialCoverage",[dumSpatialMin,dumSpatialMax])
            variable_list =  list(data.keys())
            
            variable_Schema = []
            for variable in variable_list:
                dumS = Schema("PropertyValue");
                dumS.add_property("name",variable)
                variable_Schema.append(dumS)
            
            self.add_property("variableMeasured",variable_Schema)

    def add_property(self,name,value):
        self.schema.add_property(name,value)

    def add_property_set(self,property_set):
        for key,value in property_set.items():
            self.add_property(key,value)
    
    def to_html(self,name="index.html",template="google/dataset-table.html"):
        dataset = make_dataset(self.schema, name,template=template)
        return dataset

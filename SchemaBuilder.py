import numpy as np
from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema
from schemaorg.templates.google import make_dataset
import yaml


class SchemaBuilder:
    def __init__(self,data=None):
        self.schema = Schema("Dataset")

        with open("default_properties.yml", "r") as file:
            default_properties = yaml.safe_load(file)
        
        author = default_properties['author']
        del default_properties['author']
        
        authorSchema = Schema("Organization");

        for authorprop in author:
            authorSchema.add_property(authorprop,author[authorprop])
        
        self.add_property("author",authorSchema)
        self.add_property_set(default_properties)
        self.data = data
        if(data):
            dataTime = str(data.coords['time'].values[0])
            dataTime = dataTime[:dataTime.index('.')]
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
            self.add_property("description",data.attrs['description'])
            self.add_property("spatialCoverage",[dumSpatialMin,dumSpatialMax])
            variable_list =  list(data.keys())
            
            variable_Schema = []
            for variable in variable_list:
                dumS = Schema("PropertyValue");
                dumS.add_property("name",data.data_vars.get(variable).attrs['longname'])
                dumS.add_property("unitText",data.data_vars.get(variable).attrs['units'])
                variable_Schema.append(dumS)
            
            self.add_property("variableMeasured",variable_Schema)

    def add_property(self,name,value):
        self.schema.add_property(name,value)
    
    def add_url(self,siteurl,dataurl):
        self.schema.add_property("url",siteurl)
        distribution = Schema("DataDownload")
        distribution.add_property("contentUrl",dataurl)
        distribution.add_property("encodingFormat","application/x-netcdf")
        self.add_property("distribution",distribution)
       
    def add_property_set(self,property_set):
        for key,value in property_set.items():
            self.add_property(key,value)
    
    def to_html(self,name="index.html",template="google/dataset-table.html"):
        dataset = make_dataset(self.schema, name,template =template)
        return dataset

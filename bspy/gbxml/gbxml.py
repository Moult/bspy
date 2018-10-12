# -*- coding: utf-8 -*-

from lxml import etree
from .gbxsd import Gbxsd
#from pkg_resources import resource_filename
import pkgutil
from io import BytesIO

class Gbxml():
    "An object that represents a gbXML dataset"
    
    def __init__(self,
                 xml_fp=None,
                 xsd_fp=None):
        """Initialises a new Gbxml instance
        
        Arguments:
            xml_fp (str): filepath to a gbXML file. This is read in as an 
                lxml._ElementTree object. If not supplied then a 
                new lxml._ElementTree object with only a root element is created.
                
            xsd_fp (str): filepath to a gbXML schema file. If not supplied 
                then a default gbXMl schema file is used.
                
        """
        if xml_fp: 
            self._ElementTree=self._read(xml_fp)
        else:
            st = pkgutil.get_data(__package__, 'blank.xml')
            self._ElementTree=self._read(BytesIO(st))
            
        self.ns={'gbxml':'http://www.gbxml.org/schema'}
        
        if xsd_fp:
            self.gbxsd=Gbxsd(xsd_fp)
        else:
            st = pkgutil.get_data(__package__, 'GreenBuildingXML_Ver6.01.xsd')
            self.gbxsd=Gbxsd(BytesIO(st))
        
    
    def _read(self,fp):
        """Reads a xml file and returns an etree object
        
        Arguments:
            fp (str): the filepath or a file-like object
        """
        return etree.parse(fp)

    
# OUTPUT
    
    
    def xmlstring(self,element=None):
        """Returns a string of an xml element
        
        Arguments:
            - element (lxml.etree._Element): default is root node
        
        """
        if not element: element=self.root()
        return etree.tostring(element,pretty_print=True).decode()
    
    
    def xpath(self,st_xpath,element=None):
        """Returns the result of an xpath operation on the gbXML file
        
        Arguments
            - st_xpath (str): the xpath string
            - element (lxml.etree._Element): the element for the xpath operation. The 
                default is the root element
        
        """
        if not element: element=self.root()
        return element.xpath(st_xpath,namespaces=self.ns)
    
    
    def write(self,fp):
        """Writes the gbXML file to disc
        
        Arguments:
            fp (str): the filepath
        """
        st=etree.tostring(self.root(),xml_declaration=True)
        with open(fp,'wb') as f:
            f.write(st)
       
# VALIDATION
            
    def validate(self):
        """Validates the gbXMl file using the schema
        
        Returns True if the gbXML file is valid, otherwise False
        
        """
        xmlschema = etree.XMLSchema(self.gbxsd._ElementTree)
        result=xmlschema.validate(self._ElementTree)
        return result
        
# EDITING
        
    def add_element(self,parent_element,label):
        """Adds an element to the gbXML
        
        Returns the newly created element
        
        Arguments:
            - parent_element (lxml._Element or str): the parent element that the
                new element is added to. This can be either a lxml._Element object
                or a string with the element id.
            - label (str): the label or tag of the new element
                
        """
        if isinstance(parent_element,str):
            parent_element=self.element(parent_element)
        return etree.SubElement(parent_element,'{%s}%s' % (self.ns['gbxml'],label))
    
    
    def set_attribute(self,element,key,value):
        """Sets the attribute of an element
        
        Returns the modified element
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
            - key (str): the name of the attribute
            - value (str): the value of the attribute
        
        """
        if isinstance(element,str):
            element=self.element(element)
        element.set(key,value)
        return element
    
    
    def set_text(self,element,text):
        """Sets the text of an element
        
        Returns the modified element
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.
            - text (str): the text
        
        """
        if isinstance(element,str):
            element=self.element(element)
        element.text=text
        return element
    
    
    def remove_element(self,element):
        pass
    
    def remove_attribute(self,element,key):
        pass
        
    def remove_text(self,element):
        pass
    
    
    
# QUERYING
    
    def elements(self):
        "Returns all elements of the gbXML file"
        st='//gbxml:*'
        return self.xpath(st)
    
    
    def root(self):
        "Returns the root element"
        return self._ElementTree.getroot()
    
    
    def element(self,id,label='*'):
        """Returns an element from the gbXML file
        
        Arguments:
            - id (str): the id of the element
            - label (str): the label of the element
        
        """
        st='//gbxml:%s[@id="%s"]' % (label,id)
        return self.xpath(st)[0]

    
    def label(self,element):
        """Returns the label of an element
        
        Arguments:
            - element (lxml._Element or str): This a lxml._Element object
                or a string with the element id.        
        """
        if isinstance(element,str):
            element=self.element(element)
        return  element.tag.split('}')[1]
            
    
    def attributes(self,element):
        pass

    
    def text(self,element):
        pass
    
    
    def text_value(self,element):
        pass
    
    
    def child_elements(self,element,label='*'):
        pass
    
    
    def descendent_elements(self,element,label='*'):
        pass
    
  
    
# FUNCTIONS - SURFACE
    
    
    def surface_coordinates(self,id):
        """Returns a list of coordinate tuples
        """

    
    def surface_inner_space(self,id):
        """Returns the inner Space element of a Surface, or None
        """
        
    def surface_outer_space(self,id):
        """Returns the outer Space element of a Surface, or None
        """
        
        
    
# FUNCTIONS - ZONE
        
    def zone_add_element(self,id):
        """Adds a zone to the gbXML file.
        """
        
    def zone_detach_delete(self,id):
        """Removes a Zone element and all IdRef links to the zone.
        """
        pass
        
    
    
    
    
    
    
    
    
    
    
    def child_node_text(self,id,label='*'):
        """Returns a dictionary listing any child nodes which have text
        
        Return values is {tag:text}
                
        """
        e=self._element(id,label)
        d={}
        for e1 in e:
            if e1.text:
                label=e1.tag.split('}')[1]
                d[label]=e1.text
        return d
    
    
    def child_node_values(self,id,label='*'):
        """Returns a dictionary listing any child nodes which have text
        
        Node text values are converted from strings into their datatype
            i.e. the text from an 'Area' node is converted into a float
        
        Return values is {label:value}
                
        """
        d=self.xml.child_node_text(id=id,label=label)
        d1={}
        for k,v in d.items():
            xml_type=self.xsd.element_type(k)
            #print(xml_type)
            if xml_type=='xsd:string':
                value=v
            elif xml_type=='xsd:decimal':
                value=float(v)
            else:
                raise Exception(xml_type)
            d1[k]=value
        return d1

           
    
    def node_attributes(self,id,label='*'):
        "Returns the attribute dict of node with id 'id'"
        e=self._element(id,label)
        return dict(e.attrib)
    
    
    def node_ids(self,label='*'):
        """Returns the ids of all nodes
        
        Arguments:
            label (str): the node tag to filter on
            
        """
        #filter by label
        st='//a:%s' % (label)
        l=self._ElementTree.getroot().xpath(st,namespaces=self.ns)
        return [x.get('id') for x in l]
    
    
    def parent_object(self,id,label='*'):
        """Returns the parent of an element
        
        Return value is a dictionary {'id':value,'label':value}
        
        """
        e=self._element(id,label)
        parent=e.getparent()
        return {'id':self._id(parent),
                'label':self._label(parent)}
        
    
    
    
    
    def surface_adjacent_objects(self,id):
        """Returns the objects adjacent to the surface
        
        Return value is a 2 item list of dictionaries [{'id':value,'label':value}]
        
        """
        label='Surface'
        e=self._element(id,label)
        st='./a:AdjacentSpaceId/@spaceIdRef'
        l=e.xpath(st,namespaces=self.ns)
        l=l+[None]*(2-len(l))
        surfaceType=e.get('surfaceType')
        d=\
            {'InteriorWall':None,
             'ExteriorWall':{'id':'Climate1','label':'Climate'},
             'Roof':{'id':'Climate1','label':'Climate'},
             'InteriorFloor':None,
             'ExposedFloor':{'id':'Climate1','label':'Climate'},
             'Shade':{'id':'Climate1','label':'Climate'},
             'UndergroundWall':{'id':'Ground1','label':'Ground'},
             'UndergroundSlab':{'id':'Ground1','label':'Ground'},
             'Ceiling':None,
             'Air':None,
             'UndergroundCeiling':{'id':'Ground1','label':'Ground'},
             'RaisedFloor':{'id':'Climate1','label':'Climate'},
             'SlabOnGrade':{'id':'Ground1','label':'Ground'},
             'FreestandingColumn':None,
             'EmbeddedColumn':None
             }
        l1=[]
        for x in l:
            if not x is None:
                l1.append({'id':x,'label':'Space'})
            else:
                l1.append(d[surfaceType])
        return l1


    def surface_building_ids(self,id):
        """Returns a list of building ids that the surface belongs to
        """
        l=self.surface_adjacent_objects(id)
        l=[self.parent_object(x['id'])['id'] for x in l if x['label']=='Space']
        return l
        
    
    

#    def elements(xml, tag='*'):
#        """Returns a list of lxml elements, filtered by tag
#        
#        Arguments:
#            xml (lxml.etree._ElementTree): the gbXML instance
#            tag (str): the tag name, not including the namespace
#    
#        """
#        st='//a:%s' % (tag)
#        #print(st)
#        return xml.getroot().xpath(st,namespaces=ns)
    


# -*- coding: utf-8 -*-

from lxml import etree
from .gbxsd import Gbxsd


class Gbxml():
    "An object that represents a gbXML dataset"
    
    def __init__(self,
                 xml_fp,
                 xsd_fp):
        self._ElementTree=self.read(xml_fp)
        self.ns={'a':'http://www.gbxml.org/schema'}
        self.Gbxsd=Gbxsd(xsd_fp)
        

    def _element(self,id,label='*'):
        "Returns the element"
        st='//a:%s[@id="%s"]' % (label,id)
        return self._ElementTree.getroot().xpath(st,namespaces=self.ns)[0]

    
    def _id(self,e):
        "Returns the id of an element"
        return e.get('id')
    
    
    def _label(self,e):
        "Returns the label of an element"
        return  e.tag.split('}')[1]
        
    
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
        
    
    def read(self,fp):
        """Reads a refitxml file and returns an etree object
        
        Arguments:
            fp (str): the filepath 
        
        """
        #print('READING XML FILE...')
        #print(fp)
        return etree.parse(fp)
    
    
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
    


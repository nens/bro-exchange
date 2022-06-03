# -*- coding: utf-8 -*-

from .sourcedocs import *
from gwmpy.broxml.mappings import ns_regreq_map_gmn1, ns_regreq_map_gmn2, xsi_regreq_map_gmn1, codespace_map_gmn1  # mappings
from gwmpy.checks import check_missing_args

from lxml import etree
import os


#%%

class gmn_registration_request():
    
    """
    Class for generating gmw registration requests. Check 
    allowed_srcdos for currently available possibilities. 
    """
    
    def __init__(self, srcdoc, **kwargs):
        """
        
        Parameters
        ----------
        srcdoc : string
            sourcedoc type (check allowed srcdoc types)
        **kwargs : -
            request-specific attribute data (method-specific)
            sourcedocument-specific attribute data
    
        Returns
        -------
        None, saves generated registration request xml to output directory

        """
        
        # NOTE: IN PROGRESS, MORE SOURCEDOCUMENTS TYPES WILL BE INCLUDED
        
        self.allowed_srcdocs = ['GMN_StartRegistration','GMN_MeasuringPoint']
        
        if srcdoc not in self.allowed_srcdocs:
            raise Exception("Sourcedocument type not allowed")   

        self.srcdoc = srcdoc
        self.kwargs = kwargs   
        self.request = None
        
        # Request arguments:
        arglist = {
                   'deliveryAccountableParty':'optional',
                   'broId':'optional',
                   'qualityRegime':'obligated',
                   'requestReference':'obligated',
                   'srcdocdata':'obligated',
                   }
        
        # Check wether all obligated registration request arguments for method 'initialize' are in kwargs
        check_missing_args(self.kwargs, arglist, 'gmw_registration with method initialize')
         
    def generate(self):
               
        # Generate xml document base:
        req = etree.Element("registrationRequest",nsmap=ns_regreq_map_gmn2,
            attrib={
            'xmlns':ns_regreq_map_gmn1['xmlns'],            
            ("{%s}" % ns_regreq_map_gmn2['xsi'])+'schemaLocation': xsi_regreq_map_gmn1['schemaLocation']
            })
    

        # Define registration request arguments:
        requestReference=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmn2['brocom']) + "requestReference")
        requestReference.text = self.kwargs['requestReference']

        try:
            self.kwargs['deliveryAccountableParty']
            deliveryAccountableParty=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmn2['brocom']) + "deliveryAccountableParty")
            deliveryAccountableParty.text = self.kwargs['deliveryAccountableParty']
        except:
            pass

        try:
            self.kwargs['broId']
            broId=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmn2['brocom']) + "broId")
            broId.text = self.kwargs['broId']
        except:
            pass

        qualityRegime=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmn2['brocom']) + "qualityRegime")
        qualityRegime.text = self.kwargs['qualityRegime']
                
        # Create sourcedocument and add to registrationrequest:
        if self.srcdoc == 'GMN_StartRegistration':
            
            if 'broId' in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' not allowed in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmn_startregistartion(self.kwargs['srcdocdata'])
                req.append(sourceDocument)
        
        if self.srcdoc == 'GMN_MeasuringPoint':
            
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmn_measuringpoint(self.kwargs['srcdocdata'])
                req.append(sourceDocument)

        #print(etree.tostring(req, pretty_print=True,encoding='unicode'))
        
        self.requesttree = etree.ElementTree(req)
        self.request = etree.tostring(self.requesttree, encoding='utf8', method='xml')
        #print(etree.tostring(req, pretty_print=True,encoding='unicode'))

    def write_xml(self, filename, output_dir=None):
    
        if output_dir == None:
            self.requesttree.write(filename, pretty_print = True)
        else:
            self.requesttree.write(os.path.join(output_dir,filename), pretty_print=True)



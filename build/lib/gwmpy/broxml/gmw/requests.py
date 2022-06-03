# -*- coding: utf-8 -*-

from .sourcedocs import *
from gwmpy.broxml.mappings import ns_regreq_map_gmw1, codespace_map_gmw1 # mappings
from gwmpy.checks import check_missing_args

from lxml import etree
import os


# =============================================================================
# General info
# =============================================================================

# https://schema.broservices.nl/xsd/isgmw/1.1/isgmw-messages.xsd


#%%

class gmw_registration_request():
    
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
        
        self.allowed_srcdocs = ['GMW_Construction','GMW_WellHeadProtector','GMW_Lengthening',
                                'GMW_GroundLevel','GMW_Owner','GMW_Shortening','GMW_Positions',
                                'GMW_ElectrodeStatus','GMW_Maintainer','GMW_TubeStatus',
                                'GMW_Insertion','GMW_Shift','GMW_Removal','GMW_GroundLevelMeasuring',
                                'GMW_PositionsMeasuring','GMW_ConstructionWithHistory']
        
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
                   'underPrivilege':'optional',
                   }
        
        # Check wether all obligated registration request arguments for method 'initialize' are in kwargs
        check_missing_args(self.kwargs, arglist, 'gmw_registration with method initialize')
         
    def generate(self):
               
        # Generate xml document base:
        req = etree.Element(("{%s}" % ns_regreq_map_gmw1['ns']) + "registrationRequest", nsmap=ns_regreq_map_gmw1)
            
        # Define registration request arguments:
        requestReference=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "requestReference", nsmap=ns_regreq_map_gmw1)
        requestReference.text = self.kwargs['requestReference']

        try:
            self.kwargs['deliveryAccountableParty']
            deliveryAccountableParty=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "deliveryAccountableParty", nsmap=ns_regreq_map_gmw1)
            deliveryAccountableParty.text = self.kwargs['deliveryAccountableParty']
        except:
            pass

        try:
            self.kwargs['broId']
            broId=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "broId", nsmap=ns_regreq_map_gmw1)
            broId.text = self.kwargs['broId']
        except:
            pass

        qualityRegime=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "qualityRegime", nsmap=ns_regreq_map_gmw1)
        qualityRegime.text = self.kwargs['qualityRegime']
        
        try:
            self.kwargs['underPrivilege']
            underPrivilege=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "underPrivilege", nsmap=ns_regreq_map_gmw1)
            underPrivilege.text = self.kwargs['underPrivilege']
        except:
            pass
        
        # Create sourcedocument and add to registrationrequest:
        if self.srcdoc == 'GMW_Construction':
            
            if 'broId' in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' not allowed in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_construction(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)
        
        if self.srcdoc == 'GMW_Owner':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_owner(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)           
    
        if self.srcdoc == 'GMW_WellHeadProtector':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_wellheadprotector(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)            
            
        if self.srcdoc in ['GMW_Lengthening','GMW_Shortening']:
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_lengthening_shortening(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)    

        if self.srcdoc == 'GMW_GroundLevel':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_groundlevel(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 

        if self.srcdoc == 'GMW_Positions':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_positions(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 

        if self.srcdoc == 'GMW_ElectrodeStatus':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_electrodestatus(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_Maintainer':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_maintainer(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_TubeStatus':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_tubestatus(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_Insertion':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_insertion(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)                

        if self.srcdoc == 'GMW_Shift':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_shift(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)    

        if self.srcdoc == 'GMW_Removal':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_removal(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)    
                
        if self.srcdoc == 'GMW_GroundLevelMeasuring':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_groundlevelmeasuring(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)                  

        if self.srcdoc == 'GMW_PositionsMeasuring':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_positionsmeasuring(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)   

        if self.srcdoc == 'GMW_ConstructionWithHistory':
            if 'broId' in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' not allowed in combination with given sourcedocument")
            else:
                 sourceDocument=gen_gmw_constructionwithhistory(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)  
                
        self.requesttree = etree.ElementTree(req)
        self.request = etree.tostring(self.requesttree, encoding='utf8', method='xml')
        #print(etree.tostring(req, pretty_print=True,encoding='unicode'))

    def write_xml(self, filename, output_dir=None):
    
        if output_dir == None:
            self.requesttree.write(filename, pretty_print = True)
        else:
            self.requesttree.write(os.path.join(output_dir,filename), pretty_print=True)



class gmw_replace_request():
    
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
        
        self.allowed_srcdocs = ['GMW_Construction','GMW_WellHeadProtector','GMW_Lengthening',
                                'GMW_GroundLevel','GMW_Owner','GMW_Shortening','GMW_Positions',
                                'GMW_ElectrodeStatus','GMW_Maintainer','GMW_TubeStatus',
                                'GMW_Insertion','GMW_Shift','GMW_GroundLevelMeasuring',
                                'GMW_PositionsMeasuring']
        
        if srcdoc not in self.allowed_srcdocs:
            raise Exception("Sourcedocument type not allowed")   
        
        self.srcdoc = srcdoc
        self.kwargs = kwargs   
        self.request = None
        
        # Request arguments:
        arglist = {
                   'requestReference':'obligated',
                   'deliveryAccountableParty':'optional',
                   'broId':'obligated',
                   'qualityRegime':'obligated',
                   'correctionReason':'obligated',
                   'srcdocdata':'obligated',
                   'underPrivilege':'optional',
                   }
        
        # Check wether all obligated registration request arguments for method 'initialize' are in kwargs
        check_missing_args(self.kwargs, arglist, 'gmw_registration with method initialize')
         
    def generate(self):
               
        # Generate xml document base:
        req = etree.Element(("{%s}" % ns_regreq_map_gmw1['ns']) + "replaceRequest", nsmap=ns_regreq_map_gmw1)
            
        # Define registration request arguments:
        requestReference=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "requestReference", nsmap=ns_regreq_map_gmw1)
        requestReference.text = self.kwargs['requestReference']

        try:
            self.kwargs['deliveryAccountableParty']
            deliveryAccountableParty=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "deliveryAccountableParty", nsmap=ns_regreq_map_gmw1)
            deliveryAccountableParty.text = self.kwargs['deliveryAccountableParty']
        except:
            pass


        broId=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "broId", nsmap=ns_regreq_map_gmw1)
        broId.text = self.kwargs['broId']

        qualityRegime=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "qualityRegime", nsmap=ns_regreq_map_gmw1)
        qualityRegime.text = self.kwargs['qualityRegime']

        correctionReason=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns']) + "correctionReason", nsmap=ns_regreq_map_gmw1, codeSpace = codespace_map_gmw1['correctionReason'])
        correctionReason.text = self.kwargs['correctionReason']
        
        try:
            self.kwargs['underPrivilege']
            underPrivilege=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "underPrivilege", nsmap=ns_regreq_map_gmw1)
            underPrivilege.text = self.kwargs['underPrivilege']
        except:
            pass
        
        # Create sourcedocument and add to registrationrequest:
        if self.srcdoc == 'GMW_Construction':
            
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_construction(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)
        
        if self.srcdoc == 'GMW_Owner':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_owner(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)           
    
        if self.srcdoc == 'GMW_WellHeadProtector':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_wellheadprotector(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)            
            
        if self.srcdoc in ['GMW_Lengthening','GMW_Shortening']:
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_lengthening_shortening(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)    

        if self.srcdoc == 'GMW_GroundLevel':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_groundlevel(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 

        if self.srcdoc == 'GMW_Positions':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_positions(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 

        if self.srcdoc == 'GMW_ElectrodeStatus':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_electrodestatus(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_Maintainer':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_maintainer(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_TubeStatus':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_tubestatus(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_Insertion':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_insertion(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)                

        if self.srcdoc == 'GMW_Shift':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_shift(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)    
                
        if self.srcdoc == 'GMW_GroundLevelMeasuring':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_groundlevelmeasuring(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)                  

        if self.srcdoc == 'GMW_PositionsMeasuring':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_positionsmeasuring(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)   
                
        self.requesttree = etree.ElementTree(req)
        self.request = etree.tostring(self.requesttree, encoding='utf8', method='xml')
        #print(etree.tostring(req, pretty_print=True,encoding='unicode'))

    def write_xml(self, filename, output_dir=None):
    
        if output_dir == None:
            self.requesttree.write(filename, pretty_print = True)
        else:
            self.requesttree.write(os.path.join(output_dir,filename), pretty_print=True)




class gmw_move_request():
    
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
        
        self.allowed_srcdocs = ['GMW_Construction','GMW_WellHeadProtector','GMW_Lengthening',
                                'GMW_GroundLevel','GMW_Owner','GMW_Shortening','GMW_Positions',
                                'GMW_ElectrodeStatus','GMW_Maintainer','GMW_TubeStatus',
                                'GMW_Insertion','GMW_Shift','GMW_GroundLevelMeasuring',
                                'GMW_PositionsMeasuring','GMW_Removal']
        
        if srcdoc not in self.allowed_srcdocs:
            raise Exception("Sourcedocument type not allowed")   
        
        self.srcdoc = srcdoc
        self.kwargs = kwargs   
        self.request = None
        
        # Request arguments:
        arglist = {
                   'requestReference':'obligated',
                   'deliveryAccountableParty':'optional',
                   'broId':'obligated',
                   'qualityRegime':'obligated',
                   'correctionReason':'obligated',
                   'srcdocdata':'obligated',
                   'dateToBeCorrected':'obligated',
                   'underPrivilege':'optional',
                   }
        
        # Check wether all obligated registration request arguments for method 'initialize' are in kwargs
        check_missing_args(self.kwargs, arglist, 'gmw_registration with method initialize')
         
    def generate(self):
               
        # Generate xml document base:
        req = etree.Element(("{%s}" % ns_regreq_map_gmw1['ns']) + "moveRequest", nsmap=ns_regreq_map_gmw1)
            
        # Define registration request arguments:
        requestReference=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "requestReference", nsmap=ns_regreq_map_gmw1)
        requestReference.text = self.kwargs['requestReference']

        try:
            self.kwargs['deliveryAccountableParty']
            deliveryAccountableParty=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "deliveryAccountableParty", nsmap=ns_regreq_map_gmw1)
            deliveryAccountableParty.text = self.kwargs['deliveryAccountableParty']
        except:
            pass


        broId=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "broId", nsmap=ns_regreq_map_gmw1)
        broId.text = self.kwargs['broId']

        qualityRegime=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "qualityRegime", nsmap=ns_regreq_map_gmw1)
        qualityRegime.text = self.kwargs['qualityRegime']

        correctionReason=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns']) + "correctionReason", nsmap=ns_regreq_map_gmw1, codeSpace = codespace_map_gmw1['correctionReason'])
        correctionReason.text = self.kwargs['correctionReason']
        
        dateToBeCorrected=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns']) + "dateToBeCorrected", nsmap=ns_regreq_map_gmw1)
        dateToBeCorrected.text = self.kwargs['dateToBeCorrected']      
        
        try:
            self.kwargs['underPrivilege']
            underPrivilege=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "underPrivilege", nsmap=ns_regreq_map_gmw1)
            underPrivilege.text = self.kwargs['underPrivilege']
        except:
            pass
        
        # Create sourcedocument and add to registrationrequest:
        if self.srcdoc == 'GMW_Construction':
            
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_construction(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)
        
        if self.srcdoc == 'GMW_Owner':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_owner(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)           
    
        if self.srcdoc == 'GMW_WellHeadProtector':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_wellheadprotector(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)            
            
        if self.srcdoc in ['GMW_Lengthening','GMW_Shortening']:
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_lengthening_shortening(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)    

        if self.srcdoc == 'GMW_GroundLevel':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_groundlevel(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 

        if self.srcdoc == 'GMW_Positions':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_positions(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 

        if self.srcdoc == 'GMW_ElectrodeStatus':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_electrodestatus(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_Maintainer':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_maintainer(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_TubeStatus':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_tubestatus(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_Insertion':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_insertion(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)                

        if self.srcdoc == 'GMW_Shift':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_shift(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)    
                
        if self.srcdoc == 'GMW_GroundLevelMeasuring':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_groundlevelmeasuring(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)                  

        if self.srcdoc == 'GMW_PositionsMeasuring':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_positionsmeasuring(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)   

        if self.srcdoc == 'GMW_Removal':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_removal(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)    
                
        self.requesttree = etree.ElementTree(req)
        self.request = etree.tostring(self.requesttree, encoding='utf8', method='xml')
        #print(etree.tostring(req, pretty_print=True,encoding='unicode'))

    def write_xml(self, filename, output_dir=None):
    
        if output_dir == None:
            self.requesttree.write(filename, pretty_print = True)
        else:
            self.requesttree.write(os.path.join(output_dir,filename), pretty_print=True)


class gmw_delete_request():
    
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
        
        self.allowed_srcdocs = ['GMW_WellHeadProtector','GMW_Lengthening',
                                'GMW_GroundLevel','GMW_Owner','GMW_Shortening','GMW_Positions',
                                'GMW_ElectrodeStatus','GMW_Maintainer','GMW_TubeStatus',
                                'GMW_Insertion','GMW_Shift','GMW_GroundLevelMeasuring',
                                'GMW_PositionsMeasuring','GMW_Removal']
        
        if srcdoc not in self.allowed_srcdocs:
            raise Exception("Sourcedocument type not allowed")   
        
        self.srcdoc = srcdoc
        self.kwargs = kwargs   
        self.request = None
        
        # Request arguments:
        arglist = {
                   'requestReference':'obligated',
                   'deliveryAccountableParty':'optional',
                   'broId':'obligated',
                   'qualityRegime':'obligated',
                   'correctionReason':'obligated',
                   'srcdocdata':'obligated',
                   'underPrivilege':'optional',
                   }
        
        # Check wether all obligated registration request arguments for method 'initialize' are in kwargs
        check_missing_args(self.kwargs, arglist, 'gmw_registration with method initialize')
         
    def generate(self):
               
        # Generate xml document base:
        req = etree.Element(("{%s}" % ns_regreq_map_gmw1['ns']) + "deleteRequest", nsmap=ns_regreq_map_gmw1)
            
        # Define registration request arguments:
        requestReference=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "requestReference", nsmap=ns_regreq_map_gmw1)
        requestReference.text = self.kwargs['requestReference']

        try:
            self.kwargs['deliveryAccountableParty']
            deliveryAccountableParty=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "deliveryAccountableParty", nsmap=ns_regreq_map_gmw1)
            deliveryAccountableParty.text = self.kwargs['deliveryAccountableParty']
        except:
            pass


        broId=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "broId", nsmap=ns_regreq_map_gmw1)
        broId.text = self.kwargs['broId']

        qualityRegime=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "qualityRegime", nsmap=ns_regreq_map_gmw1)
        qualityRegime.text = self.kwargs['qualityRegime']

        correctionReason=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns']) + "correctionReason", nsmap=ns_regreq_map_gmw1, codeSpace = codespace_map_gmw1['correctionReason'])
        correctionReason.text = self.kwargs['correctionReason']
        
        try:
            self.kwargs['underPrivilege']
            underPrivilege=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "underPrivilege", nsmap=ns_regreq_map_gmw1)
            underPrivilege.text = self.kwargs['underPrivilege']
        except:
            pass
        
        # Create sourcedocument and add to registrationrequest:        
        if self.srcdoc == 'GMW_Owner':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_owner(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)           
    
        if self.srcdoc == 'GMW_WellHeadProtector':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_wellheadprotector(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)            
            
        if self.srcdoc in ['GMW_Lengthening','GMW_Shortening']:
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_lengthening_shortening(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)    

        if self.srcdoc == 'GMW_GroundLevel':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_groundlevel(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 

        if self.srcdoc == 'GMW_Positions':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_positions(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 

        if self.srcdoc == 'GMW_ElectrodeStatus':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_electrodestatus(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_Maintainer':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_maintainer(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_TubeStatus':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_tubestatus(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_Insertion':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_insertion(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)                

        if self.srcdoc == 'GMW_Shift':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_shift(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)    
                
        if self.srcdoc == 'GMW_GroundLevelMeasuring':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_groundlevelmeasuring(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)                  

        if self.srcdoc == 'GMW_PositionsMeasuring':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_positionsmeasuring(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)   

        if self.srcdoc == 'GMW_Removal':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_removal(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)    
                
        self.requesttree = etree.ElementTree(req)
        self.request = etree.tostring(self.requesttree, encoding='utf8', method='xml')
        #print(etree.tostring(req, pretty_print=True,encoding='unicode'))

    def write_xml(self, filename, output_dir=None):
    
        if output_dir == None:
            self.requesttree.write(filename, pretty_print = True)
        else:
            self.requesttree.write(os.path.join(output_dir,filename), pretty_print=True)


class gmw_insert_request():
    
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
        
        self.allowed_srcdocs = ['GMW_WellHeadProtector','GMW_Lengthening',
                                'GMW_GroundLevel','GMW_Owner','GMW_Shortening','GMW_Positions',
                                'GMW_ElectrodeStatus','GMW_Maintainer','GMW_TubeStatus',
                                'GMW_Insertion','GMW_Shift','GMW_GroundLevelMeasuring',
                                'GMW_PositionsMeasuring']
        
        if srcdoc not in self.allowed_srcdocs:
            raise Exception("Sourcedocument type not allowed")   
        
        self.srcdoc = srcdoc
        self.kwargs = kwargs   
        self.request = None
        
        # Request arguments:
        arglist = {
                   'requestReference':'obligated',
                   'deliveryAccountableParty':'optional',
                   'broId':'obligated',
                   'qualityRegime':'obligated',
                   'correctionReason':'obligated',
                   'srcdocdata':'obligated',
                   'underPrivilege':'optional',
                   }
        
        # Check wether all obligated registration request arguments for method 'initialize' are in kwargs
        check_missing_args(self.kwargs, arglist, 'gmw_registration with method initialize')
         
    def generate(self):
               
        # Generate xml document base:
        req = etree.Element(("{%s}" % ns_regreq_map_gmw1['ns']) + "insertRequest", nsmap=ns_regreq_map_gmw1)
            
        # Define registration request arguments:
        requestReference=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "requestReference", nsmap=ns_regreq_map_gmw1)
        requestReference.text = self.kwargs['requestReference']

        try:
            self.kwargs['deliveryAccountableParty']
            deliveryAccountableParty=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "deliveryAccountableParty", nsmap=ns_regreq_map_gmw1)
            deliveryAccountableParty.text = self.kwargs['deliveryAccountableParty']
        except:
            pass


        broId=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "broId", nsmap=ns_regreq_map_gmw1)
        broId.text = self.kwargs['broId']

        qualityRegime=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "qualityRegime", nsmap=ns_regreq_map_gmw1)
        qualityRegime.text = self.kwargs['qualityRegime']

        correctionReason=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns']) + "correctionReason", nsmap=ns_regreq_map_gmw1, codeSpace = codespace_map_gmw1['correctionReason'])
        correctionReason.text = self.kwargs['correctionReason']
        
        try:
            self.kwargs['underPrivilege']
            underPrivilege=etree.SubElement(req, ("{%s}" % ns_regreq_map_gmw1['ns1']) + "underPrivilege", nsmap=ns_regreq_map_gmw1)
            underPrivilege.text = self.kwargs['underPrivilege']
        except:
            pass
        
        # Create sourcedocument and add to registrationrequest:        
        if self.srcdoc == 'GMW_Owner':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_owner(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)           
    
        if self.srcdoc == 'GMW_WellHeadProtector':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_wellheadprotector(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)            
            
        if self.srcdoc in ['GMW_Lengthening','GMW_Shortening']:
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_lengthening_shortening(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument)    

        if self.srcdoc == 'GMW_GroundLevel':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_groundlevel(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 

        if self.srcdoc == 'GMW_Positions':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_positions(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 

        if self.srcdoc == 'GMW_ElectrodeStatus':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_electrodestatus(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_Maintainer':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_maintainer(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_TubeStatus':
            if 'broId' not in list(self.kwargs.keys()):
                raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
            else:
                sourceDocument=gen_gmw_tubestatus(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                req.append(sourceDocument) 
                
        if self.srcdoc == 'GMW_Insertion':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_insertion(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)                

        if self.srcdoc == 'GMW_Shift':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_shift(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)    
                
        if self.srcdoc == 'GMW_GroundLevelMeasuring':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_groundlevelmeasuring(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)                  

        if self.srcdoc == 'GMW_PositionsMeasuring':
             if 'broId' not in list(self.kwargs.keys()):
                 raise Exception("Registration request argument 'broId' required in combination with given sourcedocument")
             else:
                 sourceDocument=gen_gmw_positionsmeasuring(self.kwargs['srcdocdata'], ns_regreq_map_gmw1, codespace_map_gmw1, self.srcdoc)
                 req.append(sourceDocument)   
                
        self.requesttree = etree.ElementTree(req)
        self.request = etree.tostring(self.requesttree, encoding='utf8', method='xml')
        #print(etree.tostring(req, pretty_print=True,encoding='unicode'))

    def write_xml(self, filename, output_dir=None):
    
        if output_dir == None:
            self.requesttree.write(filename, pretty_print = True)
        else:
            self.requesttree.write(os.path.join(output_dir,filename), pretty_print=True)
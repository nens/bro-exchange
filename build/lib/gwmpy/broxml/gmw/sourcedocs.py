# -*- coding: utf-8 -*-

from .constructables import *
from gwmpy import check_missing_args

from lxml import etree

# =============================================================================
# General info
# =============================================================================

# https://schema.broservices.nl/xsd/isgmw/1.1/isgmw-messages.xsd


#%%

def gen_gmw_construction(data, nsmap, codespacemap):
    
    arglist =  {'objectIdAccountableParty':'obligated',
                'deliveryContext':'obligated',        
                'constructionStandard':'obligated',        
                'initialFunction':'obligated',        
                'numberOfMonitoringTubes':'obligated',        
                'groundLevelStable':'obligated',        
                'wellStability':'optional', # only if groundLevelStabel = nee       
                'NITGCode':'optional',        
                #'putcode':'optional', it exists in documentation, not in the official xml schema's
                'owner':'obligated',        
                'maintenanceResponsibleParty':'optional',        
                'wellHeadProtector':'obligated',        
                'wellConstructionDate':'obligated',        
                'deliveredLocation':'obligated',        #
                'deliveredVerticalPosition':'obligated', #     
                'monitoringTubes':'obligated',        #
                }    
    
    # Note: mapSheetCode is a valid optional argument that hasn't been included yet
    
    constructables = ['wellConstructionDate','deliveredLocation','deliveredVerticalPosition','monitoringTubes']
      
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_construction')
    
    sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
    GMW_Construction = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + "GMW_Construction", nsmap=nsmap)

    # GMW_Construction subelements:
    GMW_Construction_subelements = {}
    for arg in data.keys():
        if arg not in constructables:
            if arg in codespacemap.keys():  
                GMW_Construction_subelements[arg] = etree.SubElement(GMW_Construction, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                GMW_Construction_subelements[arg].text = str(data[arg])
            else:
                GMW_Construction_subelements[arg] = etree.SubElement(GMW_Construction, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                GMW_Construction_subelements[arg].text = str(data[arg])

        else:
            
            if arg == 'wellConstructionDate':

                GMW_Construction_subelements[arg] = gen_wellconstructiondate(data, nsmap)
                GMW_Construction.append(GMW_Construction_subelements[arg])

            elif arg == 'deliveredLocation':

                GMW_Construction_subelements[arg] = gen_deliveredlocation(data, nsmap, codespacemap)
                GMW_Construction.append(GMW_Construction_subelements[arg])                
                
            elif arg == 'deliveredVerticalPosition':

                GMW_Construction_subelements[arg] = gen_deliveredverticalposition(data, nsmap, codespacemap)
                GMW_Construction.append(GMW_Construction_subelements[arg])  
                
            elif arg == 'monitoringTubes':
                
                if len(data['monitoringTubes'])<1:
                    raise Exception("No monitoring tubes provided in input, at least 1 monitoringtube should be provided")
                else:
                    for tube in range(len(data[arg])):
                        GMW_Construction_subelements['monitoringTube{}'.format(str(tube))] = gen_monitoringtube(data, tube, nsmap, codespacemap)
                        GMW_Construction.append(GMW_Construction_subelements['monitoringTube{}'.format(str(tube))])
                
    return(sourceDocument)
    
    
    
    
    
    
    
    
    

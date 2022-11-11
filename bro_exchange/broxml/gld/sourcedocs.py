# -*- coding: utf-8 -*-

from .constructables import *
from bro_exchange import check_missing_args

from lxml import etree
import uuid as uuid_gen
import pandas as pd

# =============================================================================
# General info
# =============================================================================


#%%

def gen_gld_startregistration(data, nsmap, codespacemap):
    
    count = 2
    
    arglist =  {'objectIdAccountableParty':'optional',
                'groundwaterMonitoringNets':'optional', #     
                'monitoringPoints':'obligated',        #
                }    
    
    # Note: mapSheetCode is a valid optional argument that hasn't been included yet
    
    constructables = ['groundwaterMonitoringNets','monitoringPoints']
      
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gld_startregistration')
    
    sourceDocument = etree.Element("sourceDocument") 
    GLD_StartRegistration  = etree.SubElement(sourceDocument, "GLD_StartRegistration", 
                                        attrib = {            
                                        ("{%s}" % nsmap['gml'])+'id': 'id_0001'})

    # GMW_Construction subelements:
    GLD_StartRegistration_subelements = {}
    for arg in data.keys():
        if arg not in constructables:
            if arg in codespacemap.keys():  
                GLD_StartRegistration_subelements[arg] = etree.SubElement(GLD_StartRegistration, arg, codeSpace = codespacemap[arg])
                GLD_StartRegistration_subelements[arg].text = str(data[arg])
            else:
                GLD_StartRegistration_subelements[arg] = etree.SubElement(GLD_StartRegistration, arg)
                GLD_StartRegistration_subelements[arg].text = str(data[arg])

        else:
                           
            if arg == 'groundwaterMonitoringNets':
                
                if len(data[arg])<1:
                    pass
                else:
                    for net in range(len(data[arg])):
                        GLD_StartRegistration_subelements['groundwaterMonitoringNet{}'.format(str(net))],count = gen_groundwatermonitoringnet(data, net, nsmap, count)
                        GLD_StartRegistration.append(GLD_StartRegistration_subelements['groundwaterMonitoringNet{}'.format(str(net))])
        
            elif arg == 'monitoringPoints':
                
                if len(data[arg])!=1:
                    raise Exception("One monitoringpoint should be provided, no more or no less")
                else:
                    for point in range(len(data[arg])):
                        GLD_StartRegistration_subelements['monitoringPoint{}'.format(str(point))],count = gen_monitoringpoint(data, point, nsmap, count)
                        GLD_StartRegistration.append(GLD_StartRegistration_subelements['monitoringPoint{}'.format(str(point))])
                
    return(sourceDocument)
    
#%%

def gen_gld_addition(data, nsmap, codespacemap):
    
    count = 2
    
    arglist =  {'metadata':'obligated',
                'phenomenonTime':'fixed', # fixed: automatically generated, all input will be neglected
                'resultTime':'obligated', # fixed: automatically generated, all input will be neglected
                'procedure':'obligated',
                'observedProperty':'fixed',
                'featureOfInterest':'fixed',
                'result':'obligated', # Note, timeseries input in datetime string with format %Y-%m-%dT%H:%M:%S
                }      
    
    # Note: mapSheetCode is a valid optional argument that hasn't been included yet
    
    constructables = ['metadata','procedure','result']
      
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gld_addition')
    
    sourceDocument = etree.Element("sourceDocument") 
    GLD_Addition  = etree.SubElement(sourceDocument, "GLD_Addition", 
                                        attrib = {            
                                        ("{%s}" % nsmap['gml'])+'id': 'id_0001'})
    
    observation = etree.SubElement(GLD_Addition, "observation")
    
    # Unique for every observation!
    OM_Observation  = etree.SubElement(observation, ("{%s}" % nsmap['om']) + 'OM_Observation', nsmap=nsmap,
                                       attrib = {            
                                       ("{%s}" % nsmap['gml'])+'id': '_{}'.format(uuid_gen.uuid4())})
    
    type_ = etree.SubElement(OM_Observation, ("{%s}" % nsmap['om']) + 'type', nsmap=nsmap,
                                       attrib = {            
                                       ("{%s}" % nsmap['xlink'])+'href': "http://www.opengis.net/def/observationType/waterml/2.0/MeasurementTimeseriesTVPObservation"})    
    
    # =============================================================================
    # NOTE: Related observation references not yet supported 
    # =============================================================================
    
    OM_Observation_subelements = {}
    for arg in arglist.keys():
        if arg in data.keys():

            if arg == 'metadata':
                OM_Observation_subelements['metadata'] = gen_metadata(data, nsmap, codespacemap)
                OM_Observation.append(OM_Observation_subelements['metadata'])
            elif arg == 'phenomenonTime':
                OM_Observation_subelements['phenomenonTime'], count = gen_phenomenontime(data, nsmap, codespacemap, count)
                OM_Observation.append(OM_Observation_subelements['phenomenonTime'])
            elif arg == 'resultTime':
                OM_Observation_subelements['resultTime'],count = gen_resulttime(data, nsmap, codespacemap, count)
                OM_Observation.append(OM_Observation_subelements['resultTime'])
            elif arg == 'procedure':
                
                # 1: reference to excisting procedure (observation process gmlid):
                
                if type(data['procedure'])==str:
                    OM_Observation_subelements['procedure'] = etree.SubElement(OM_Observation, ("{%s}" % nsmap['om']) + 'procedure', nsmap=nsmap,
                                                       attrib = {            
                                                       ("{%s}" % nsmap['xlink'])+'href': data['procedure']})  
                
                # 2: creation of new procedure with given input
                
                elif type(data['procedure'])==dict:
                    OM_Observation_subelements['procedure'] = gen_procedure(data, nsmap, codespacemap)
                    OM_Observation.append(OM_Observation_subelements['procedure'])   
                else:
                    raise Exception("Error: invalid input type for procedure, should be 'dict' or 'str' ")
                                         
            elif arg == 'observedProperty':
                observedProperty  = etree.SubElement(OM_Observation, ("{%s}" % nsmap['om']) + 'observedProperty', nsmap=nsmap)
            elif arg == 'featureOfInterest':
                observedProperty  = etree.SubElement(OM_Observation, ("{%s}" % nsmap['om']) + 'featureOfInterest', nsmap=nsmap) 
            elif arg == 'result':
                #try:
                    if type(data['result'])!=list:
                        raise Exception("Error: invalid input type for result, should be list with dictionaries")
                    elif list(pd.DataFrame(data['result']).columns)!=['time','value','metadata']:
                        raise Exception("Error: invalid input fields for result, fields should be ['time','value','qualifiers']")
                    else:
                        OM_Observation_subelements['result'], count = gen_result(data, nsmap, codespacemap, count)
                        OM_Observation.append(OM_Observation_subelements['result'])    
                #except:
                    #raise Exception("Error: failed to compose timeseriesdata, probably due to input format")
                    
                
        
                                                 
        else: # fixed arguments (in case not in data)
        
            if arg == 'phenomenonTime':
                OM_Observation_subelements['phenomenonTime'], count = gen_phenomenontime(data, nsmap, codespacemap, count)
                OM_Observation.append(OM_Observation_subelements['phenomenonTime'])
            elif arg == 'resultTime':
                OM_Observation_subelements['resultTime'], count = gen_resulttime(data, nsmap, codespacemap, count)
                OM_Observation.append(OM_Observation_subelements['resultTime']) 
            elif arg == 'observedProperty':
                observedProperty  = etree.SubElement(OM_Observation, ("{%s}" % nsmap['om']) + 'observedProperty', nsmap=nsmap)
            elif arg == 'featureOfInterest':
                observedProperty  = etree.SubElement(OM_Observation, ("{%s}" % nsmap['om']) + 'featureOfInterest', nsmap=nsmap)                                   
                    
                
    return(sourceDocument)

#%%


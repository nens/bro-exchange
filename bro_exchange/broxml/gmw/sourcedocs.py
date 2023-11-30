
from lxml import etree

from bro_exchange import check_missing_args

from .constructables import *

# =============================================================================
# General info
# =============================================================================

# https://schema.broservices.nl/xsd/isgmw/1.1/isgmw-messages.xsd


#%%

def gen_gmw_construction(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {'objectIdAccountableParty':'obligated',
                'deliveryContext':'obligated',        
                'constructionStandard':'obligated',        
                'initialFunction':'obligated',        
                'numberOfMonitoringTubes':'obligated',        
                'groundLevelStable':'obligated',        
                'wellStability':'optional', # only if groundLevelStabel = nee       
                'nitgCode':'optional',        
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
    
    if sourcedoctype == "GMW_Construction": 
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_Construction = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)
    
    else:
        GMW_Construction = etree.Element(("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)
        
    # GMW_Construction subelements:
    GMW_Construction_subelements = {}
    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:
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
                                GMW_Construction_subelements[f'monitoringTube{str(tube)}'] = gen_monitoringtube(data, tube, nsmap, codespacemap, sourcedoctype)
                                GMW_Construction.append(GMW_Construction_subelements[f'monitoringTube{str(tube)}'])
            
    if sourcedoctype == "GMW_Construction": 
                
        return(sourceDocument)
    
    else:
        
        return(GMW_Construction)
    
def gen_gmw_wellheadprotector(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {'eventDate':'obligated',       
                'wellHeadProtector':'obligated',              #
                }    
    
    # Note: mapSheetCode is a valid optional argument that hasn't been included yet
    
    constructables = ['eventDate']
      
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_wellheadprotector')
    if sourcedoctype ==  "GMW_WellHeadProtector":
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_WellHeadProtector = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)
    else:
        GMW_WellHeadProtector = etree.Element(("{%s}" % nsmap['ns']) +sourcedoctype , nsmap=nsmap)

    # GMW_WellHeadProtector subelements:
    GMW_WellHeadProtector_subelements = {}
    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:
                if arg not in constructables:

                    if arg in codespacemap.keys():  
                        GMW_WellHeadProtector_subelements[arg] = etree.SubElement(GMW_WellHeadProtector, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                        GMW_WellHeadProtector_subelements[arg].text = str(data[arg])
                    else:
                        GMW_WellHeadProtector_subelements[arg] = etree.SubElement(GMW_WellHeadProtector, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                        GMW_WellHeadProtector_subelements[arg].text = str(data[arg])
        
                else:
                    
                    if arg == 'eventDate':
        
                        GMW_WellHeadProtector_subelements[arg] = gen_eventdate(data, nsmap)
                        GMW_WellHeadProtector.append(GMW_WellHeadProtector_subelements[arg])
    
    if sourcedoctype ==  "GMW_WellHeadProtector":

        return(sourceDocument)
    
    else:
        
        return(GMW_WellHeadProtector)
        
    
def gen_gmw_lengthening_shortening(data, nsmap, codespacemap, sourcedoctype):
    
    if sourcedoctype in ['GMW_Lengthening','lengthening']:

        arglist =  {'eventDate':'obligated',       
                    'wellHeadProtector':'optional', 
                    'numberOfTubesLengthened':'obligated',
                    'monitoringTubes':'obligated'#
                    }    

    elif sourcedoctype in ['GMW_Shortening','shortening']:
        
        arglist =  {'eventDate':'obligated',       
                        'wellHeadProtector':'optional', 
                        'numberOfTubesShortened':'obligated',
                        'monitoringTubes':'obligated'#
                        } 
        
    # Note: mapSheetCode is a valid optional argument that hasn't been included yet
    constructables = ['eventDate','monitoringTubes']
      
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_lenghtening - gen_gmw_lenghtening')
    
    if sourcedoctype == 'GMW_Lengthening':
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_Lengthening_Shortening = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + "GMW_Lengthening", nsmap=nsmap)
        ammount = data['numberOfTubesLengthened']
        
    elif sourcedoctype == 'GMW_Shortening':
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_Lengthening_Shortening = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + "GMW_Shortening", nsmap=nsmap)        
        ammount = data['numberOfTubesShortened']
    
    elif sourcedoctype == 'shortening':
        GMW_Lengthening_Shortening = etree.Element(("{%s}" % nsmap['ns']) + "shortening", nsmap=nsmap)        
        ammount = data['numberOfTubesShortened']

    elif sourcedoctype == 'shortening':
        GMW_Lengthening_Shortening = etree.Element(("{%s}" % nsmap['ns']) + "lengthening", nsmap=nsmap)        
        ammount = data['numberOfTubesLengthened']
        
    # GMW_Lengthening subelements:
    GMW_Lengthening_Shortening_subelements = {}
    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:    
                if arg not in constructables:
                    if arg in codespacemap.keys():  
                        GMW_Lengthening_Shortening_subelements[arg] = etree.SubElement(GMW_Lengthening_Shortening, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                        GMW_Lengthening_Shortening_subelements[arg].text = str(data[arg])
                    else:
                        GMW_Lengthening_Shortening_subelements[arg] = etree.SubElement(GMW_Lengthening_Shortening, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                        GMW_Lengthening_Shortening_subelements[arg].text = str(data[arg])
        
                else:
                    
                    if arg == 'eventDate':
        
                        GMW_Lengthening_Shortening_subelements[arg] = gen_eventdate(data, nsmap)
                        GMW_Lengthening_Shortening.append(GMW_Lengthening_Shortening_subelements[arg])
        
                    elif arg == 'monitoringTubes':
                        
                        if len(data['monitoringTubes'])<ammount:
                            raise Exception("Ammount of monitoringtubes should be equal to numberOfTubesLengthened")
                        else:
                            for tube in range(len(data[arg])):
                                GMW_Lengthening_Shortening_subelements[f'monitoringTube{str(tube)}'] = gen_monitoringtube(data, tube, nsmap, codespacemap, sourcedoctype)
                                GMW_Lengthening_Shortening.append(GMW_Lengthening_Shortening_subelements[f'monitoringTube{str(tube)}'])
                        
    if sourcedoctype in ['GMW_Lengthening','GMW_Shortening']:
        return(sourceDocument)    
    elif sourcedoctype in ['lengthening','shortening']:
        return(GMW_Lengthening_Shortening)
    
def gen_gmw_groundlevel(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {'eventDate':'obligated',       
                'wellStability':'obligated', 
                'groundLevelStable':'obligated',
                'deliveredVerticalPosition':'obligated'#
                }    
    
    # Note: mapSheetCode is a valid optional argument that hasn't been included yet
    constructables = ['eventDate','deliveredVerticalPosition']
      
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_groundlevel')
    
    if sourcedoctype == "GMW_GroundLevel":
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_GroundLevel = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)
    else:
        GMW_GroundLevel = etree.Element(("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)
        

    # GMW_GroundLevel subelements:
    GMW_GroundLevel_subelements = {}
    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:
                if arg not in constructables:
                    if arg in codespacemap.keys():  
                        GMW_GroundLevel_subelements[arg] = etree.SubElement(GMW_GroundLevel, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                        GMW_GroundLevel_subelements[arg].text = str(data[arg])
                    else:
                        GMW_GroundLevel_subelements[arg] = etree.SubElement(GMW_GroundLevel, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                        GMW_GroundLevel_subelements[arg].text = str(data[arg])
        
                else:
                    
                    if arg == 'eventDate':
        
                        GMW_GroundLevel_subelements[arg] = gen_eventdate(data, nsmap)
                        GMW_GroundLevel.append(GMW_GroundLevel_subelements[arg])
        
                    elif arg == 'deliveredVerticalPosition':
                        
                        if 'groundLevelPosition' in list(data['deliveredVerticalPosition'].keys()):
                            groundLevelPosition = etree.SubElement(GMW_GroundLevel, ("{%s}" % nsmap['ns']) + 'groundLevelPosition', nsmap = nsmap, uom = "m")
                            groundLevelPosition.text = str(data['deliveredVerticalPosition']['groundLevelPosition'])        
                        
                        if 'groundLevelPositioningMethod' in list(data['deliveredVerticalPosition'].keys()):                        
                            groundLevelPositioningMethod = etree.SubElement(GMW_GroundLevel, ("{%s}" % nsmap['ns']) + 'groundLevelPositioningMethod', nsmap = nsmap, codeSpace = codespacemap['groundLevelPositioningMethod'])
                            groundLevelPositioningMethod.text = data['deliveredVerticalPosition']['groundLevelPositioningMethod']        

    if sourcedoctype == "GMW_GroundLevel":
        
        return(sourceDocument)     
    
    else:
        
        return(groundLevelPositioningMethod)

def gen_gmw_owner(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {'eventDate':'obligated',       
                'owner':'obligated',      
                }    
    
    # Note: mapSheetCode is a valid optional argument that hasn't been included yet
    constructables = ['eventDate']
      
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_owner')
    
    if sourcedoctype == 'GMW_Owner':
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_Owner = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) +sourcedoctype, nsmap=nsmap)
    else:
        GMW_Owner =  etree.Element(("{%s}" % nsmap['ns']) +sourcedoctype, nsmap=nsmap)

        
    # GMW_Owner subelements:
    GMW_Owner_subelements = {}
    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:        
                if arg not in constructables:
                    if arg in codespacemap.keys():  
                        GMW_Owner_subelements[arg] = etree.SubElement(GMW_Owner, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                        GMW_Owner_subelements[arg].text = str(data[arg])
                    else:
                        GMW_Owner_subelements[arg] = etree.SubElement(GMW_Owner, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                        GMW_Owner_subelements[arg].text = str(data[arg])
        
                else:
                    
                    if arg == 'eventDate':
        
                        GMW_Owner_subelements[arg] = gen_eventdate(data, nsmap)
                        GMW_Owner.append(GMW_Owner_subelements[arg])
    
    if sourcedoctype == 'GMW_Owner':
        
        return(sourceDocument)     
    else:
        
        return(GMW_Owner)

def gen_gmw_positions(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {'eventDate':'obligated',       
                'wellStability':'obligated', 
                'groundLevelStable':'obligated',
                'numberOfMonitoringTubes':'obligated',
                'deliveredVerticalPosition':'obligated',
                'monitoringTubes':'obligated'
                }    
    
    # Note: mapSheetCode is a valid optional argument that hasn't been included yet
    constructables = ['eventDate','deliveredVerticalPosition','monitoringTubes']
      
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_positions')
    
    
    if sourcedoctype == "GMW_Positions":
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_Positions = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)
    else:
        GMW_Positions = etree.Element(("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)

    # GMW_GroundLevel subelements:
    GMW_Positions_subelements = {}
    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:        
                if arg not in constructables:
                    if arg in codespacemap.keys():  
                        GMW_Positions_subelements[arg] = etree.SubElement(GMW_Positions, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                        GMW_Positions_subelements[arg].text = str(data[arg])
                    else:
                        GMW_Positions_subelements[arg] = etree.SubElement(GMW_Positions, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                        GMW_Positions_subelements[arg].text = str(data[arg])
        
                else:
                    
                    if arg == 'eventDate':
        
                        GMW_Positions_subelements[arg] = gen_eventdate(data, nsmap)
                        GMW_Positions.append(GMW_Positions_subelements[arg])
        
                    elif arg == 'deliveredVerticalPosition':
                        
                        if 'groundLevelPosition' in list(data['deliveredVerticalPosition'].keys()):
                            groundLevelPosition = etree.SubElement(GMW_Positions, ("{%s}" % nsmap['ns']) + 'groundLevelPosition', nsmap = nsmap, uom = "m")
                            groundLevelPosition.text = str(data['deliveredVerticalPosition']['groundLevelPosition'])        
                        
                        if 'groundLevelPositioningMethod' in list(data['deliveredVerticalPosition'].keys()):                        
                            groundLevelPositioningMethod = etree.SubElement(GMW_Positions, ("{%s}" % nsmap['ns']) + 'groundLevelPositioningMethod', nsmap = nsmap, codeSpace = codespacemap['groundLevelPositioningMethod'])
                            groundLevelPositioningMethod.text = data['deliveredVerticalPosition']['groundLevelPositioningMethod']        
                    
                    elif arg == 'monitoringTubes':
                        
                        ammount = data['numberOfMonitoringTubes']
        
                        if len(data['monitoringTubes'])<ammount:
                            raise Exception("Ammount of monitoringtubes should be equal to numberOfTubesLengthened")
                        else:
                            for tube in range(len(data[arg])):
                                GMW_Positions_subelements[f'monitoringTube{str(tube)}'] = gen_monitoringtube(data, tube, nsmap, codespacemap, sourcedoctype)
                                GMW_Positions.append(GMW_Positions_subelements[f'monitoringTube{str(tube)}'])
            
    if sourcedoctype == "GMW_Positions":
                        
        return(sourceDocument)

    else:
        
        return(GMW_Positions)



def gen_gmw_electrodestatus(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {'eventDate':'obligated',       
                'numberOfElectrodesChanged':'obligated', 
                'electrodes':'obligated',
                }    
        
    # Note: mapSheetCode is a valid optional argument that hasn't been included yet
    constructables = ['eventDate','electrodes']
      
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_electrodestatus')
    
    if sourcedoctype == "GMW_ElectrodeStatus":
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_ElectrodeStatus = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)
        
    else:
        GMW_ElectrodeStatus = etree.Element(("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)

        
    # GMW_GroundLevel subelements:
    GMW_ElectrodeStatus_subelements = {}
    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:
                if arg not in constructables:
                    if arg in codespacemap.keys():  
                        GMW_ElectrodeStatus_subelements[arg] = etree.SubElement(GMW_ElectrodeStatus, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                        GMW_ElectrodeStatus_subelements[arg].text = str(data[arg])
                    else:
                        GMW_ElectrodeStatus_subelements[arg] = etree.SubElement(GMW_ElectrodeStatus, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                        GMW_ElectrodeStatus_subelements[arg].text = str(data[arg])
        
                else:
                    
                    if arg == 'eventDate':
        
                        GMW_ElectrodeStatus_subelements[arg] = gen_eventdate(data, nsmap)
                        GMW_ElectrodeStatus.append(GMW_ElectrodeStatus_subelements[arg])
        
                        
                    elif arg == 'electrodes':
                        
                        ammount = data['numberOfElectrodesChanged']
        
                        if len(data['electrodes'])<ammount:
                            raise Exception("Ammount of electrodes should be equal to numberOfElectrodesChanged")
                        else:
                            for electrode in range(len(data[arg])):
                                GMW_ElectrodeStatus_subelements[f'electrode{str(electrode)}'] = adjust_electrode(data, electrode, nsmap, codespacemap)
                                GMW_ElectrodeStatus.append(GMW_ElectrodeStatus_subelements[f'electrode{str(electrode)}'])
            
    if sourcedoctype == "GMW_ElectrodeStatus":
                        
        return(sourceDocument)   

    else:
        
        return(GMW_ElectrodeStatus)   


def gen_gmw_maintainer(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {'eventDate':'obligated',       
                'maintenanceResponsibleParty':'obligated', 
                }    
              
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_maintainer')
    
    if sourcedoctype == "GMW_Maintainer":
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_Maintainer = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)

    else:
        GMW_Maintainer =  etree.Element(("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)


    constructables = ['eventDate']

    # GMW_GroundLevel subelements:
    GMW_Maintainer_subelements = {}
    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:        
                if arg not in constructables:
        
                    if arg in codespacemap.keys():  
                        GMW_Maintainer_subelements[arg] = etree.SubElement(GMW_Maintainer, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                        GMW_Maintainer_subelements[arg].text = str(data[arg])
                    else:
                        GMW_Maintainer_subelements[arg] = etree.SubElement(GMW_Maintainer, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                        GMW_Maintainer_subelements[arg].text = str(data[arg])
                else:
                    
                    if arg == 'eventDate':
        
                        GMW_Maintainer_subelements[arg] = gen_eventdate(data, nsmap)
                        GMW_Maintainer.append(GMW_Maintainer_subelements[arg])
    if sourcedoctype == "GMW_Maintainer":
              
        return(sourceDocument)   

    else:
        
        return(GMW_Maintainer)   


def gen_gmw_tubestatus(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {'eventDate':'obligated',       
                'numberOfTubesChanged':'obligated', 
                'monitoringTubes':'obligated', 
                }    
              
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_tubestatus')
    
    if sourcedoctype== "GMW_TubeStatus":
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_TubeStatus = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)
    else:
        GMW_TubeStatus = etree.Element(("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)


    constructables = ['eventDate','monitoringTubes']

    # GMW_GroundLevel subelements:
    GMW_TubeStatus_subelements = {}
    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:        
                if arg not in constructables:
        
                    if arg in codespacemap.keys():  
                        GMW_TubeStatus_subelements[arg] = etree.SubElement(GMW_TubeStatus, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                        GMW_TubeStatus_subelements[arg].text = str(data[arg])
                    else:
                        GMW_TubeStatus_subelements[arg] = etree.SubElement(GMW_TubeStatus, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                        GMW_TubeStatus_subelements[arg].text = str(data[arg])
                else:
                    
                    if arg == 'eventDate':
        
                        GMW_TubeStatus_subelements[arg] = gen_eventdate(data, nsmap)
                        GMW_TubeStatus.append(GMW_TubeStatus_subelements[arg])
                        
                    elif arg == 'monitoringTubes':
                        
                        ammount = data['numberOfTubesChanged']
        
                        if len(data['monitoringTubes'])<ammount:
                            raise Exception("Ammount of monitoringtubes should be equal to numberOfTubesLengthened")
                        else:
                            for tube in range(len(data[arg])):
                                GMW_TubeStatus_subelements[f'monitoringTube{str(tube)}'] = gen_monitoringtube(data, tube, nsmap, codespacemap, sourcedoctype)
                                GMW_TubeStatus.append(GMW_TubeStatus_subelements[f'monitoringTube{str(tube)}'])       
    if sourcedoctype== "GMW_TubeStatus":
                        
        return(sourceDocument)   

    else:
        return(GMW_TubeStatus)   
      
        

def gen_gmw_insertion(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {'tubeNumber':'obligated',  
                'eventDate':'obligated',       
                'tubeTopPosition':'obligated', 
                'tubeTopPositioningMethod':'obligated', 
                'insertedPartLength':'obligated', 
                'insertedPartDiameter':'obligated', 
                'insertedPartMaterial':'obligated',                 
                }    
              
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_insertion')
    
    
    if sourcedoctype == "GMW_Insertion":
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_Insertion = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)

    else:
        GMW_Insertion = etree.Element(("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)


    constructables = ['eventDate','tubeTopPosition','insertedPartLength','insertedPartDiameter','insertedPartMaterial']

    # GMW_GroundLevel subelements:
    GMW_Insertion_subelements = {}

    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:
                if arg not in constructables:
        
                    if arg in codespacemap.keys():  
                        GMW_Insertion_subelements[arg] = etree.SubElement(GMW_Insertion, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                        GMW_Insertion_subelements[arg].text = str(data[arg])
                    else:
                        GMW_Insertion_subelements[arg] = etree.SubElement(GMW_Insertion, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                        GMW_Insertion_subelements[arg].text = str(data[arg])
                else:
                    
                    if arg == 'eventDate':
        
                        GMW_Insertion_subelements[arg] = gen_eventdate(data, nsmap)
                        GMW_Insertion.append(GMW_Insertion_subelements[arg])
                             
                    if arg == 'tubeTopPosition':        
                        tubeTopPosition = etree.SubElement(GMW_Insertion, ("{%s}" % nsmap['ns']) + 'tubeTopPosition', nsmap = nsmap, uom = 'm')
                        tubeTopPosition.text = str(data['tubeTopPosition']) 
                    
                    if arg == 'insertedPartLength':        
                        insertedPartLength = etree.SubElement(GMW_Insertion, ("{%s}" % nsmap['ns']) + 'insertedPartLength', nsmap = nsmap, uom = 'm')
                        insertedPartLength.text = str(data['insertedPartLength']) 
                        
                    if arg == 'insertedPartDiameter':        
                        insertedPartDiameter = etree.SubElement(GMW_Insertion, ("{%s}" % nsmap['ns']) + 'insertedPartDiameter', nsmap = nsmap, uom = 'mm')
                        insertedPartDiameter.text = str(data['insertedPartDiameter']) 
                    
                    if arg == 'insertedPartMaterial':       
                        insertedPartMaterial = etree.SubElement(GMW_Insertion, ("{%s}" % nsmap['ns']) + 'insertedPartMaterial', nsmap = nsmap, codeSpace=codespacemap['tubeMaterial'])
                        insertedPartMaterial.text = str(data['insertedPartMaterial'])

    if sourcedoctype == "GMW_Insertion":
                   
        return(sourceDocument)   

    else:
                   
        return(insertedPartMaterial)   


def gen_gmw_shift(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {
                'eventDate':'obligated',       
                'deliveredVerticalPosition':'obligated'             
                }    
              
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_shift')
    
    if sourcedoctype == "GMW_Shift":
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_Shift = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)
    else:
        GMW_Shift = etree.Element(("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)


    constructables = ['eventDate','deliveredVerticalPosition']

    # GMW_GroundLevel subelements:
    GMW_Shift_subelements = {}

    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:
                if arg not in constructables:
        
                    if arg in codespacemap.keys():  
                        GMW_Shift_subelements[arg] = etree.SubElement(GMW_Shift, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                        GMW_Shift_subelements[arg].text = str(data[arg])
                    else:
                        GMW_Shift_subelements[arg] = etree.SubElement(GMW_Shift, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                        GMW_Shift_subelements[arg].text = str(data[arg])
                else:
                    
                    if arg == 'eventDate':
        
                        GMW_Shift_subelements[arg] = gen_eventdate(data, nsmap)
                        GMW_Shift.append(GMW_Shift_subelements[arg])
                             
                    if arg == 'deliveredVerticalPosition':        
                        if 'groundLevelPosition' in list(data['deliveredVerticalPosition'].keys()):
                            groundLevelPosition = etree.SubElement(GMW_Shift, ("{%s}" % nsmap['ns']) + 'groundLevelPosition', nsmap = nsmap, uom = "m")
                            groundLevelPosition.text = str(data['deliveredVerticalPosition']['groundLevelPosition'])        
                        
                        if 'groundLevelPositioningMethod' in list(data['deliveredVerticalPosition'].keys()):                        
                            groundLevelPositioningMethod = etree.SubElement(GMW_Shift, ("{%s}" % nsmap['ns']) + 'groundLevelPositioningMethod', nsmap = nsmap, codeSpace = codespacemap['groundLevelPositioningMethod'])
                            groundLevelPositioningMethod.text = data['deliveredVerticalPosition']['groundLevelPositioningMethod']        
    
    if sourcedoctype == "GMW_Shift":
            
        return(sourceDocument)   
    else:
        
        return(groundLevelPositioningMethod)   



def gen_gmw_removal(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {
                'wellRemovalDate':'obligated',       
                }    
              
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_removal')
    
    
    if sourcedoctype == "GMW_Removal":
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_Removal = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)
        
    else:
        GMW_Removal = etree.Element(("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)

    constructables = ['wellRemovalDate']

    # GMW_GroundLevel subelements:
    GMW_Removal_subelements = {}

    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:
                if arg not in constructables:
        
                    if arg in codespacemap.keys():  
                        GMW_Removal_subelements[arg] = etree.SubElement(GMW_Removal, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                        GMW_Removal_subelements[arg].text = str(data[arg])
                    else:
                        GMW_Removal_subelements[arg] = etree.SubElement(GMW_Removal, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                        GMW_Removal_subelements[arg].text = str(data[arg])
                else:
                    
                    if arg == 'wellRemovalDate':
        
                        GMW_Removal_subelements[arg] = gen_removaldate(data, nsmap)
                        GMW_Removal.append(GMW_Removal_subelements[arg])

    if sourcedoctype == "GMW_Removal":
            
        return(sourceDocument)   

    else:
        
        return(GMW_Removal)   


def gen_gmw_groundlevelmeasuring(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {
                'eventDate':'obligated',       
                'deliveredVerticalPosition':'obligated'             
                }    
                           
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_groundlevelmeasuring')
    
    
    if sourcedoctype =="GMW_GroundLevelMeasuring":
        
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_GroundLevelMeasuring = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) +sourcedoctype, nsmap=nsmap)
    else:
        GMW_GroundLevelMeasuring = etree.Element(("{%s}" % nsmap['ns']) +sourcedoctype, nsmap=nsmap)

    constructables = ['eventDate','deliveredVerticalPosition']

    # GMW_GroundLevel subelements:
    GMW_GroundLevelMeasuring_subelements = {}

    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:
                if arg not in constructables:
        
                    if arg in codespacemap.keys():  
                        GMW_GroundLevelMeasuring_subelements[arg] = etree.SubElement(GMW_GroundLevelMeasuring, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                        GMW_GroundLevelMeasuring_subelements[arg].text = str(data[arg])
                    else:
                        GMW_GroundLevelMeasuring_subelements[arg] = etree.SubElement(GMW_GroundLevelMeasuring, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                        GMW_GroundLevelMeasuring_subelements[arg].text = str(data[arg])
                else:
                    
                    if arg == 'eventDate':
        
                        GMW_GroundLevelMeasuring_subelements[arg] = gen_eventdate(data, nsmap)
                        GMW_GroundLevelMeasuring.append(GMW_GroundLevelMeasuring_subelements[arg])
                             
                    if arg == 'deliveredVerticalPosition':        
                        if 'groundLevelPosition' in list(data['deliveredVerticalPosition'].keys()):
                            groundLevelPosition = etree.SubElement(GMW_GroundLevelMeasuring, ("{%s}" % nsmap['ns']) + 'groundLevelPosition', nsmap = nsmap, uom = "m")
                            groundLevelPosition.text = str(data['deliveredVerticalPosition']['groundLevelPosition'])        
                        
                        if 'groundLevelPositioningMethod' in list(data['deliveredVerticalPosition'].keys()):                        
                            groundLevelPositioningMethod = etree.SubElement(GMW_GroundLevelMeasuring, ("{%s}" % nsmap['ns']) + 'groundLevelPositioningMethod', nsmap = nsmap, codeSpace = codespacemap['groundLevelPositioningMethod'])
                            groundLevelPositioningMethod.text = data['deliveredVerticalPosition']['groundLevelPositioningMethod']        
                    
    if sourcedoctype =="GMW_GroundLevelMeasuring":
            
        return(sourceDocument)   
    
    else:
            
        return(groundLevelPositioningMethod)   




def gen_gmw_positionsmeasuring(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {'eventDate':'obligated',       
                'numberOfMonitoringTubes':'obligated',
                'deliveredVerticalPosition':'obligated',
                'monitoringTubes':'obligated'
                }    
    
    # Note: mapSheetCode is a valid optional argument that hasn't been included yet
    constructables = ['eventDate','deliveredVerticalPosition','monitoringTubes']
      
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_positionsmeasuring')
    
    if sourcedoctype == "GMW_PositionsMeasuring":
        sourceDocument = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
        GMW_PositionsMeasuring = etree.SubElement(sourceDocument, ("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)
    else:
        GMW_PositionsMeasuring = etree.Element(("{%s}" % nsmap['ns']) + sourcedoctype, nsmap=nsmap)



    # GMW_GroundLevel subelements:
    GMW_PositionsMeasuring_subelements = {}

    for ordered_arg in arglist.keys():
        for arg in data.keys():
            if arg == ordered_arg:
                if arg not in constructables:
                    if arg in codespacemap.keys():  
                        GMW_PositionsMeasuring_subelements[arg] = etree.SubElement(GMW_PositionsMeasuring, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap, codeSpace = codespacemap[arg])
                        GMW_PositionsMeasuring_subelements[arg].text = str(data[arg])
                    else:
                        GMW_PositionsMeasuring_subelements[arg] = etree.SubElement(GMW_PositionsMeasuring, ("{%s}" % nsmap['ns']) + arg, nsmap=nsmap)
                        GMW_PositionsMeasuring_subelements[arg].text = str(data[arg])
        
                else:
                    
                    if arg == 'eventDate':
        
                        GMW_PositionsMeasuring_subelements[arg] = gen_eventdate(data, nsmap)
                        GMW_PositionsMeasuring.append(GMW_PositionsMeasuring_subelements[arg])
        
                    elif arg == 'deliveredVerticalPosition':
                        
                        if 'groundLevelPosition' in list(data['deliveredVerticalPosition'].keys()):
                            groundLevelPosition = etree.SubElement(GMW_PositionsMeasuring, ("{%s}" % nsmap['ns']) + 'groundLevelPosition', nsmap = nsmap, uom = "m")
                            groundLevelPosition.text = str(data['deliveredVerticalPosition']['groundLevelPosition'])        
                        
                        if 'groundLevelPositioningMethod' in list(data['deliveredVerticalPosition'].keys()):                        
                            groundLevelPositioningMethod = etree.SubElement(GMW_PositionsMeasuring, ("{%s}" % nsmap['ns']) + 'groundLevelPositioningMethod', nsmap = nsmap, codeSpace = codespacemap['groundLevelPositioningMethod'])
                            groundLevelPositioningMethod.text = data['deliveredVerticalPosition']['groundLevelPositioningMethod']        
                    
                    elif arg == 'monitoringTubes':
                        
                        ammount = data['numberOfMonitoringTubes']
        
                        if len(data['monitoringTubes'])<ammount:
                            raise Exception("Ammount of monitoringtubes should be equal to numberOfTubesLengthened")
                        else:
                            for tube in range(len(data[arg])):
                                GMW_PositionsMeasuring_subelements[f'monitoringTube{str(tube)}'] = gen_monitoringtube(data, tube, nsmap, codespacemap, sourcedoctype)
                                GMW_PositionsMeasuring.append(GMW_PositionsMeasuring_subelements[f'monitoringTube{str(tube)}'])
            
    if sourcedoctype == "GMW_PositionsMeasuring":
                        
        return(sourceDocument)   

    else:
        return(GMW_PositionsMeasuring)   



def gen_gmw_constructionwithhistory(data, nsmap, codespacemap, sourcedoctype):
    
    arglist =  {'construction':'obligated',       
                'events':'obligated',
                'removal':'optional',
                }    
    
      
    # Check wether all obligated arguments are in data
    check_missing_args(data, arglist, 'gen_gmw_constructionwithhistory')
    
    sourceDocument_main = etree.Element(("{%s}" % nsmap['ns']) + "sourceDocument", nsmap=nsmap) 
    GMW_ConstructionWithHistory = etree.SubElement(sourceDocument_main, ("{%s}" % nsmap['ns']) + "GMW_ConstructionWithHistory", nsmap=nsmap)

    
    # Step 1: create construction 
    construction=gen_gmw_construction(data['construction'], nsmap, codespacemap, 'construction')
    GMW_ConstructionWithHistory.append(construction)

    # Step 2: add events in chronological order
    
    intermediate_events = {}
    
    for event in range(len(data['events'])):
        
        intermediate_events[str(event)] = etree.SubElement(GMW_ConstructionWithHistory, ("{%s}" % nsmap['ns']) + 'intermediateEvent', nsmap=nsmap)

        if data['events'][event]['srcdoc'] == 'GMW_Owner':
            sourceDocument=gen_gmw_owner(data['events'][event]['eventdata'], nsmap, codespacemap, 'owner')
            intermediate_events[str(event)].append(sourceDocument)  
            GMW_ConstructionWithHistory.append(intermediate_events[str(event)])
    
        if data['events'][event]['srcdoc'] == 'GMW_WellHeadProtector':
            sourceDocument=gen_gmw_wellheadprotector(data['events'][event]['eventdata'], nsmap, codespacemap, 'wellHeadProtector')
            intermediate_events[str(event)].append(sourceDocument)            
            GMW_ConstructionWithHistory.append(intermediate_events[str(event)])
            
        if data['events'][event]['srcdoc'] in ['GMW_Lengthening','GMW_Shortening']:
            if data['events'][event]['srcdoc'] == 'GMW_Lengthening':
                sourceDocument=gen_gmw_lengthening_shortening(data['events'][event]['eventdata'], nsmap, codespacemap, 'lengthening')
            elif data['events'][event]['srcdoc'] == 'GMW_Shortening':
                sourceDocument=gen_gmw_lengthening_shortening(data['events'][event]['eventdata'], nsmap, codespacemap, 'shortening')

            intermediate_events[str(event)].append(sourceDocument)    
            GMW_ConstructionWithHistory.append(intermediate_events[str(event)])

        if data['events'][event]['srcdoc'] == 'GMW_GroundLevel':
            sourceDocument=gen_gmw_groundlevel(data['events'][event]['eventdata'], nsmap, codespacemap, 'groundLevel')
            intermediate_events[str(event)].append(sourceDocument) 
            GMW_ConstructionWithHistory.append(intermediate_events[str(event)])

        if data['events'][event]['srcdoc'] == 'GMW_Positions':
            sourceDocument=gen_gmw_positions(data['events'][event]['eventdata'], nsmap, codespacemap, 'positions')
            intermediate_events[str(event)].append(sourceDocument) 
            GMW_ConstructionWithHistory.append(intermediate_events[str(event)])

        if data['events'][event]['srcdoc'] == 'GMW_ElectrodeStatus':
            sourceDocument=gen_gmw_electrodestatus(data['events'][event]['eventdata'], nsmap, codespacemap, 'electrodeStatus')
            intermediate_events[str(event)].append(sourceDocument) 
            GMW_ConstructionWithHistory.append(intermediate_events[str(event)])
               
        if data['events'][event]['srcdoc'] == 'GMW_Maintainer':
            sourceDocument=gen_gmw_maintainer(data['events'][event]['eventdata'], nsmap, codespacemap, 'maintainer')
            intermediate_events[str(event)].append(sourceDocument) 
            GMW_ConstructionWithHistory.append(intermediate_events[str(event)])
                
        if data['events'][event]['srcdoc'] == 'GMW_TubeStatus':
            sourceDocument=gen_gmw_tubestatus(data['events'][event]['eventdata'], nsmap, codespacemap, 'tubeStatus')
            intermediate_events[str(event)].append(sourceDocument) 
            GMW_ConstructionWithHistory.append(intermediate_events[str(event)])
                
        if data['events'][event]['srcdoc'] == 'GMW_Insertion':
            sourceDocument=gen_gmw_insertion(data['events'][event]['eventdata'], nsmap, codespacemap, 'insertion')
            intermediate_events[str(event)].append(sourceDocument)                
            GMW_ConstructionWithHistory.append(intermediate_events[str(event)])

        if data['events'][event]['srcdoc'] == 'GMW_Shift':
            sourceDocument=gen_gmw_shift(data['events'][event]['eventdata'], nsmap, codespacemap, 'shift')
            intermediate_events[str(event)].append(sourceDocument)    
            GMW_ConstructionWithHistory.append(intermediate_events[str(event)])
                
        if data['events'][event]['srcdoc'] == 'GMW_GroundLevelMeasuring':
            sourceDocument=gen_gmw_groundlevelmeasuring(data['events'][event]['eventdata'], nsmap, codespacemap, 'groundLevelMeasuring')
            intermediate_events[str(event)].append(sourceDocument)                  
            GMW_ConstructionWithHistory.append(intermediate_events[str(event)])

        if data['events'][event]['srcdoc'] == 'GMW_PositionsMeasuring':
            sourceDocument=gen_gmw_positionsmeasuring(data['events'][event]['eventdata'], nsmap, codespacemap, 'positionsMeasuring')
            intermediate_events[str(event)].append(sourceDocument)           
            GMW_ConstructionWithHistory.append(intermediate_events[str(event)])

    if 'removal' in list(data.keys()):

        removal=gen_gmw_removal(data['removal'], nsmap, codespacemap, 'removal')
        GMW_ConstructionWithHistory.append(removal)
   
    return(sourceDocument_main)   


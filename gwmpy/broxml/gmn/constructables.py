# -*- coding: utf-8 -*-

#from gwmpy.broxml.mappings import ns_regreq_map # mappings
from gwmpy import check_missing_args

from lxml import etree
import uuid


#%%

def gen_startdatemonitoring(data, nsmap):
    
    startDateMonitoring = etree.Element('startDateMonitoring') 
    
    choice = data['startDateMonitoring'][1]
    text = data['startDateMonitoring'][0]
    
    if choice == 'date':
        date = etree.SubElement(startDateMonitoring, ("{%s}" % nsmap['brocom']) + 'date', nsmap=nsmap)
        date.text = text
    elif choice == 'year':
        date = etree.SubElement(startDateMonitoring, ("{%s}" % nsmap['brocom']) + 'year', nsmap=nsmap)
        date.text = text      
    elif choice == 'yearMonth':
        date = etree.SubElement(startDateMonitoring, ("{%s}" % nsmap['brocom']) + 'yearMonth', nsmap=nsmap)
        date.text = text  
    elif text == None:
        date = etree.SubElement(startDateMonitoring, ("{%s}" % nsmap['brocom']) + 'voidReason', nsmap=nsmap)
        date.text = choice 
        
    return(startDateMonitoring)

#%%


def gen_measuringpoint(data, mp, nsmap):
    """

    Parameters
    ----------
    data : dictionary, with measuringpoints item.
        The measuringpoints item consits of a list with dictionaries, 
        in which each dictionary contains the attribute data of a single
        monitoringtube. The required and optional items are listed within
        the arglist in this function.
    tube : int
        measuringpoint index in list of available measuringpoint. A 
        measuringpoint element will be created for the selected 
        measuringpoint.
    nsmap : dictionary
        namespace mapping
    codespacemap: dictionary
        codespace mapping

    Returns
    -------
    subelement structure to pass in the measuringpoint element for the 
    selected measuringpoint

    """
    
    arglist = { 
                'measuringPointCode':'obligated',
                'monitoringTube':'obligated'}
    
    check_missing_args(data['measuringPoints'][mp], arglist, 'gen_monitoringtube, tube with index {}'.format(str(mp)))

    measuringpoint = etree.Element('measuringPoint')
    
    measuringpoint_ = etree.SubElement(measuringpoint,'MeasuringPoint',  attrib = {            
                                        ("{%s}" % nsmap['gml'])+'id': 'id_mp{}'.format(str(mp))})
    
    measuringpointcode =  etree.SubElement(measuringpoint_,'measuringPointCode')
    measuringpointcode.text = data['measuringPoints'][mp]['measuringPointCode']
    
    monitoringTube = etree.SubElement(measuringpoint_,'monitoringTube')
    
    GroundwaterMonitoringTube = etree.SubElement(monitoringTube,'GroundwaterMonitoringTube',  attrib = {            
                                        ("{%s}" % nsmap['gml'])+'id': 'id_mpgwmt{}'.format(str(mp))})
    
    broId = etree.SubElement(GroundwaterMonitoringTube,'broId')  
    broId.text = str(data['measuringPoints'][mp]['monitoringTube']['broId'])
    
    tubeNumber = etree.SubElement(GroundwaterMonitoringTube,'tubeNumber') 
    tubeNumber.text = str(data['measuringPoints'][mp]['monitoringTube']['tubeNumber'])
    
    return(measuringpoint)
    

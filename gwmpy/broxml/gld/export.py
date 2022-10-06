import requests
import xmltodict
import pandas as pd
from datetime import datetime

def get_gld_json_data(startDate, endDate, objectID, fullObservationPeriod=True):
    """

    Parameters
    ----------
    startDate: string
        Startdate of period of interest
    endDate: string
        Enddate of period of interest
    objectID: string
        Het BRO-ID van het object. 
    fullObservationPeriod: Boolean
        Default is True. If True, the full observation period in which the start and enddate lie in are returned. If False, these periods are filtered to the exact specified dates.


    """

    #Get the XML data
    URL = f"https://publiek.broservices.nl/gm/gld/v1/objects/{objectID}?observationPeriodBeginDate={startDate}&observationPeriodEndDate={endDate}"
    r = requests.get(url=URL) 

    #Transform data to dictionary and clean the data
    output_raw = xmltodict.parse(r.content)

    cleaned_data = []

    observations = output_raw["ns11:dispatchDataResponse"]["ns11:dispatchDocument"]["ns11:GLD_O"]["ns11:observation"]

    for i in observations:
        for j in i["om:OM_Observation"]["om:result"]["waterml:MeasurementTimeseries"]["waterml:point"]:
            timestamp = datetime.strptime(j["waterml:MeasurementTVP"]["waterml:time"], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
            cleaned_data.append(
                {
                    "timestamp":timestamp,
                    "value":j["waterml:MeasurementTVP"]["waterml:value"]["#text"],
                    "gml_id":i["om:OM_Observation"]["@gml:id"],
                    "procedure":i["om:OM_Observation"]["om:procedure"]["@xlink:href"],
                    "status":j["waterml:MeasurementTVP"]["waterml:metadata"]["waterml:TVPMeasurementMetadata"]["waterml:qualifier"]["swe:Category"]["swe:value"]
                }
            )

    #Transform to pd dataframe
    df = pd.DataFrame.from_records(cleaned_data)
    df = df.sort_values(by=['timestamp'])


    #Return data, depending on fullObservationPeriod value. If False, the data is filtered on the exact period between startDate and endDate
    if fullObservationPeriod == False:
        startDate = datetime.strptime(startDate, '%Y-%m-%d')
        endDate = datetime.strptime(endDate, '%Y-%m-%d')
        df = df[(df['timestamp'] >= startDate) & (df['timestamp'] < endDate)]
        
    
    return df
        





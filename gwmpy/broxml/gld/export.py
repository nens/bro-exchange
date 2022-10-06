import requests
import xmltodict
import pandas as pd

def get_gld_json_data(startDate, endDate, objectID, dataFrameFormat=False):
    URL = f"https://publiek.broservices.nl/gm/gld/v1/objects/{objectID}?observationPeriodBeginDate={startDate}&observationPeriodEndDate={endDate}"
    r = requests.get(url=URL)  
    output_raw = xmltodict.parse(r.content)

    output_cleaned = {}

    output_cleaned["metadata"] = {
    "dispatch_time":output_raw["ns11:dispatchDataResponse"]["brocom:dispatchTime"],
    "broID":output_raw["ns11:dispatchDataResponse"]["ns11:dispatchDocument"]["ns11:GLD_O"]["brocom:broId"],
    "kvk_accountable_party":output_raw["ns11:dispatchDataResponse"]["ns11:dispatchDocument"]["ns11:GLD_O"]["brocom:deliveryAccountableParty"],
    "qualitiy_regime":output_raw["ns11:dispatchDataResponse"]["ns11:dispatchDocument"]["ns11:GLD_O"]["brocom:qualityRegime"]
    }

    observations = output_raw["ns11:dispatchDataResponse"]["ns11:dispatchDocument"]["ns11:GLD_O"]["ns11:observation"]
    data = []

    for i in observations:
        for j in i["om:OM_Observation"]["om:result"]["waterml:MeasurementTimeseries"]["waterml:point"]:
            data.append(
                {
                    "timestamp":j["waterml:MeasurementTVP"]["waterml:time"],
                    "value":j["waterml:MeasurementTVP"]["waterml:value"]["#text"],
                    "gml_id":i["om:OM_Observation"]["@gml:id"],
                    "procedure":i["om:OM_Observation"]["om:procedure"]["@xlink:href"],
                    "status":j["waterml:MeasurementTVP"]["waterml:metadata"]["waterml:TVPMeasurementMetadata"]["waterml:qualifier"]["swe:Category"]["swe:value"]
                }
            )

    output_cleaned["data"] = data

    if dataFrameFormat == False:
        return_data = output_cleaned
    else:
        return_data = pd.DataFrame.from_records(output_cleaned["data"])

    return return_data

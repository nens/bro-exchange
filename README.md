<img src=bro_exchange/logo/bro_exchange.png width="140">

# bro-exchange
This package contains tools for retrieving data from or sending data to the Dutch National Key Registry of the Subsurface (Basis Registratie Ondergrond). 
 
# Installation
 
 `pip install git+https://github.com/nens/bro-exchange#egg=bro-exchange`

# Usage
bro-exchange contains data exchange tools for the following BRO-services:

## Innameservice
### Tools:
- Request and sourcedocument generators: these can be used to generate registration object oriented requests in xml from json input
- Requests handlers: these can be used for validating requests and sending them to the innamewebservice.

### Examples:
Notebooks for demonstrating how to generate and send registration object oriented requests are included in examples\innamewebservice

### Note:
Data exchange related to the following registration objects is supported at this moment:

- Groundwatermonitoringwell (GMW)
- Groundwatermonitoringnetwork (GMN)
- Groundwaterlevelresearch (GLD)


## Uitgifteservice
- Handlers for downloading data from the uitgifteservice. These tools are still in development at the moment.
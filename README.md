# bro-exchange

This package contains tools for retrieving data from or sending data to the
Dutch National Key Registry of the Subsurface (Basis Registratie Ondergrond).
The following components:
- Groundwatermonitoringwell (GMW)
- Groundwatermonitoringnetwork (GMN)
- Groundwaterleveldossier (GLD)
- Formationresistancedossier (FRD)

## Installation

 `pip install git+https://github.com/nens/bro-exchange#egg=bro-exchange`

## Usage

**TODO** The usage instructions are still a work in progress. Stay tuned for updates!

## `bro_exchange/`
This module contains the following components working with the 
inname- en uitgifteservice:
- Request and sourcedocument generators: These tools allow you to create
  registration object oriented requests in XML from JSON input.
- Requests handlers: These handlers can be used for validating requests and sending
  them to the innamewebservice.
- Handlers for downloading data from the uitgifteservice. These tools are
  still in development at the moment.

## `examples/`

Notebooks for demonstrating how to generate and send registration object
oriented requests are included in examples\innamewebservice

## Development

Local dev installation:

    $ pip3 install ruff
	$ python3 -m venv .
	$ bin/pip install -e .

Syntax checks:

	$ ruff check .
	$ ruff check . --fix

Formatting ("black"):

	$ ruff format .

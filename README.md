# Proof of concept for Survival Analysis Microservice

A simple proof-of-concept Flask app, implementing the API as documented [here](https://github.com/chicagopcdc/Documents/blob/master/GEN3/table-one-tool/requirements.md). This repo's goal is to prototype features that will be integrated into the [PcdcAnalysisTools](https://github.com/chicagopcdc/PcdcAnalysisTools) repo.

## Design

This proof-of-concept should:

## Project setup

1. Download and install Python(^3.6) and pip
2. Run `pip install -r requirements.txt` to install dependencies
3. run `export FLASK_APP=app.py`
4. Run `flask run`
5. Service is now running on port 5000

## Dependendcies

- `flask` for creating simple API server application
- `pandas` for fetching and parsing JSON data as data frame


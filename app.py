from flask import Flask, jsonify, abort, request, make_response
import numpy as np
import pandas as pd

DATA_URL = ""  # source data API endpoint

app = Flask(__name__)  # default port 5000


def fetch_data(url, args):
    """Fetches the source data (pandas.DataFrame) from url based on request body

    Args:
        url(str): A URL path to data source
        args(dict): Request body parameters and values
    """
    # TODO
    return


def fetch_fake_data(args):
    """Fetches the mocked source data (pandas.DataFrame) based on request body

    Args:
        args(dict): Request body parameters and values
    """

    return (
        pd.read_json("./data.json", orient="records")
    )


def get_tableone_result(data, args):
    """Returns the onetable results (dict) based on data and request body

    Args:
        data(pandas.DataFrame): Source data
        args(dict): Request body parameters and values

    Returns:
        A dict of survival result consisting of "pval", "risktable", and "survival" data
        example:

    """
    groupingVariable = args["groupingVariable"] #groupingVariable now set to groupingVariable object from JSON
    covariates = args["covariates"] 
    grouping_operator = groupingVariable["trueIf"]["operator"]     # groupingVariable operator
    grouping_query_operator = { "eq" :"==" , "gt" : ">" , "gte" : ">=", "lt" : "<" , "lte" : "<=",}
    grouping_value = groupingVariable["trueIf"]["value"]
    query_data_true = data.query(f" {groupingVariable['name']} {grouping_query_operator[grouping_operator]} {grouping_value} ") #only 'true (+)' objects/patients
    query_data_false = data[~data.index.isin(query_data_true.index)] #false (-) patients
    total = len(data)                                              # total patients number
    true_number = len(query_data_true)                             #total true patients number
    
    response_headers={"size": 'Sample size (' + groupingVariable['name'] + ')',"true": groupingVariable['label']['true'],"false": groupingVariable['label']['false']}

    response_variables=[]
    for covariate in covariates: #traverses through each element of covariates array 
        keys=[]
        if covariate["type"] == "continuous":
            true_mean = format((query_data_true[covariate['name']].mean())/int(covariate['unit']), '0.0f' )
            false_mean = format((query_data_false[covariate['name']].mean())/int(covariate['unit']), '0.0f' )
            keys = [{"name" : "" , "data" : {"true" : true_mean, "false" : false_mean } }]
            
        if covariate["type"] == "categorical":
            cats = dict(zip(covariate["keys"],covariate["values"]))
            
            for k,v in cats.items():
                cat_true = '{:.1%}'.format( len(query_data_true.query(f"{covariate['name']} == '{v}' ")) / len(query_data_true) )
                cat_false = '{:.1%}'.format( len(query_data_false.query(f"{covariate['name']} == '{v}' ")) / len(query_data_false) )
                key={"name" : k , "data" : {"true" : cat_true, "false" : cat_false} }
                keys.append(key)

        if covariate["type"] == "bucketized":
            covariate["cutoffs"] = [int(i) for i in covariate["cutoffs"]] #traverses cutoffs array
            buck_value = [ covariate["range"][0] ] + list( covariate["cutoffs"] ) + [ covariate["range"][1] ]  #buck_value is a list, #buck stands for bucketized           
            for i in range(len(buck_value)-1): 
                buck_true = '{:.1%}'.format( len(query_data_true.query(f"{covariate['name']} >= {buck_value[i]*int(covariate['unit'])} & {covariate['name']} < {buck_value[i+1] * int(covariate['unit'])}  ")) / len(query_data_true) )                
                #format percentage with 1 decimal point 
                #buck_true is % of patients with SMN that are < 18 mo
                buck_false = '{:.1%}'.format( len(query_data_false.query(f"{covariate['name']} >= {buck_value[i]*int(covariate['unit'])} & {covariate['name']} < {buck_value[i+1] * int(covariate['unit'])}  ")) / len(query_data_false) )
                key={"name" : covariate["keys"][i] , "data" : {"true" : buck_true, "false" : buck_false} }                
                keys.append(key)

        varible={
        "name" : covariate["label"],
        "size" : { "total" : total ,"true" : true_number  },
        "pval" : None,
        "keys"  : keys
        }
        response_variables.append(varible)    

    return    {
        "headers": response_headers,
        "variables": response_variables,
    }


@app.route("/", methods=["OPTIONS", "POST"])
def root():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response


    elif request.method == "POST":
        args = request.get_json()
        data = (
            fetch_fake_data(args)
        )
        response = jsonify(get_tableone_result(data, args))
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

'''
July 8th, 2022
added auto-run lines below with debug and auto reloader
'''

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

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
    efs_flag = args.get("efsFlag", False)
    factor_var = args.get("factorVariable", "")
    stratification_var = args.get("stratificationVariable", "")
    start_time = args.get("startTime", 0)
    end_time = args.get("endTime", 0)

    status_col, time_col = (
        ("EFSCENS", "EFSTIME")
        if efs_flag
        else ("SCENS", "STIME")
    )
    time_range_query = (
        f"time >= {start_time} and time <= {end_time}"
        if end_time > 0
        else f"time >= {start_time}"
    )

    return (
        pd.read_json("./data.json", orient="records")
        .query(f"{time_col} >= 0")
        .assign(status=lambda x: x[status_col] == 1,
                time=lambda x: x[time_col] / 365.25)
        .filter(items=[factor_var, stratification_var, "status", "time"])
        .query(time_range_query)
    )


def get_onetable_result(data, args):
    """Returns the onetable results (dict) based on data and request body

    Args:
        data(pandas.DataFrame): Source data
        args(dict): Request body parameters and values

    Returns:
        A dict of survival result consisting of "pval", "risktable", and "survival" data
        example:

        {"pval": 0.1,
         "risktable": [{ "nrisk": 30, "time": 0}],
         "survival": [{"prob": 1.0, "time": 0.0}]}
    """


    return [
{"name":"Clinical Characteristic", "sampleSize":null, "SMN":null, "category":[]},
]


@app.route("/", methods=["OPTIONS", "POST"])
def root():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    elif request.method == "POST":
        response = jsonify({
    "headers": {
        "size": "Sample size (SMN)",
        "true": "SMN Formed",
        "false": "No SMN Formed"
    },
    "variables": [
        {
            "name": "Mean age at diagnosis (mo)",
            "size": {
                "total": 5327,
                "true": 47
            },
            "pval": 0.23,
            "keys": [
                {
                    "name": "",
                    "data": {
                        "true": 27.5,
                        "false": 18.0
                    }
                }
            ]
        },
        {
            "name": "Age at diagnosis",
            "size": {
                "total": 5787,
                "true": 42
            },
            "pval": 0.27,
            "keys": [
                {
                    "name": "< 18 mo",
                    "data": {
                        "true": 41.9,
                        "false": 51.3
                    }
                },
                {
                    "name": ">= 18 mo",
                    "data": {
                        "true": 58.1,
                        "false": 50.0
                    }
                }
            ]
        },
        {
            "name": "Sex",
            "size": {
                "total": 2001,
                "true": 51
            },
            "pval": 0.07,
            "keys": [
                {
                    "name": "Female",
                    "data": {
                        "true": 62.8,
                        "false": 46.6
                    }
                },
                {
                    "name": "Male",
                    "data": {
                        "true": 37.2,
                        "false": 53.4
                    }
                }
            ]
        }
    ]
})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

 

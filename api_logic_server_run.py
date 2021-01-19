#!/usr/bin/env python3
"""
  ApiLogicServer hello

  $ python3 api_logic_server_run.py [Listener-IP]

  This will run the example on http://Listener-Ip:5000

"""
import sys

import logic_bank_utils.util as logic_bank_utils

(did_fix_path, sys_env_info) = \
    logic_bank_utils.add_python_path(project_dir="replace_project_name", my_file=__file__)

from flask import render_template
from safrs import ValidationError

import app as app  # database opened here

# address where the api will be hosted, change this if you're not running the app on localhost!
host = sys.argv[1] if sys.argv[
                      1:] else "localhost"  # 127.0.0.1 check in swagger or your lient what is used you wight need cors support
app = app.create_app(host=host)


@app.route('/')
def welcome():
    return render_template('index.html')


@app.errorhandler(ValidationError)
def handle_exception(e: ValidationError):

    res = {'code': e.status_code,
           'errorType': 'Validation Error',
           'errorMessage': e.message}
#    if debug:
#        res['errorMessage'] = e.message if hasattr(e, 'message') else f'{e}'

    return res, 400

@app.after_request
def after_request(response):
    """
    Enable CORS. Disable it if you don't need CORS or instal Cors Libaray
    https://parzibyte.me/blog
    """
    response.headers[
        "Access-Control-Allow-Origin"] = "*"  # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE, PATCH"
    response.headers["Access-Control-Allow-Headers"] = \
        "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response


if __name__ == "__main__":
    app.run(host=host, threaded=False)

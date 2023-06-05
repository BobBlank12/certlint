from flask import Blueprint, render_template, request, flash
import os
import sys
import subprocess
from certlint import *

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    # if request.method == 'POST': 
    return render_template("index.html")

@views.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        certfile = f.filename
        f.save(f.filename)
        f.close
        fileformat = "unknown"
        key_type = "n/a"

        # Determine the file format I've been given
        fileformat, key_type = determine_file_format(f.filename, fileformat, key_type)

        # Convert to PEM from whatever I've received
        if fileformat == "der":
            try:
                convert_der_to_pem(f.filename)
            except Exception as e:
                print("Error converting DER to PEM {:}".format(e))
            else:
                print(f"\tI've created a {f.filename}-converted.pem file for you.")

        if fileformat == "p12":
            try:
                convert_p12_to_pem(f.filename)
            except Exception as e:
                print("Error converting P12 to PEM {:}".format(e))
            else:
                print(f"\tI've created a {filename}-converted.pem file for you.")

        if fileformat == "p7b":
            try:
                convert_p7b_to_pem(f.filename)
            except Exception as e:
                print("Error converting P7B to PEM {:}".format(e))
            else:
                print(f"\tI've created a {f.filename}-converted.pem file for you.")

        if fileformat == "p7b":
            try:
                convert_p7b_to_pem(f.filename)
            except Exception as e:
                print("Error converting P7B to PEM {:}".format(e))
            else:
                print(f"\tI've created a {f.filename}-converted.pem file for you.")

        return render_template("uploadsuccess.html", name = certfile, fileformat = fileformat, key_type = key_type)
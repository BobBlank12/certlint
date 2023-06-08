from flask import request, Blueprint, render_template, request, flash, url_for, send_file
from werkzeug.utils import secure_filename
import os
import sys
import subprocess
from certlint import *

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'uploads/'

@views.route('/', methods=['GET', 'POST'])
def home():
    # if request.method == 'POST': 
    return render_template("index.html")

@views.route("/uploads/<filename>-converted-to.pem", methods=['GET', 'POST'])
def getFile(filename):
    return send_file(UPLOAD_FOLDER+filename+"-converted-to.pem", as_attachment=True)

@views.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        #print ("saving file: website/" + UPLOAD_FOLDER + secure_filename(f.filename))
        f.save("website/" + UPLOAD_FOLDER + secure_filename(f.filename))
        f.close
        fileformat = "unknown"
        key_type = "n/a"

        # Determine the file format I've been given
        fileformat, key_type = determine_file_format("website/" + UPLOAD_FOLDER+f.filename, fileformat, key_type)

        #print(f"fileformat={fileformat}")

        # Convert to PEM from whatever I've received

        links = []

        links.append(
            {
                "Original file: " : f.filename,
                "Original file format:" : fileformat,
                "Original key format:" : key_type
            }
        )

        if fileformat == "pem":
            try:
                convert_pem_to_pem("website/" + UPLOAD_FOLDER+f.filename)
            except Exception as e:
                print("Error converting PEM to PEM {:}".format(e))
            else:
                #print(f"\tI've created a {f.filename}-converted-to.pem file for you.")
                links.append(
                    {
                        f.filename+"-converted-to.pem:" : '<a href="'+UPLOAD_FOLDER+f.filename+'-converted-to.pem">'+f.filename+'-converted-to.pem</a>'
                    }
                )

        if fileformat == "der":
            try:
                convert_der_to_pem("website/" + UPLOAD_FOLDER+f.filename)
            except Exception as e:
                print("Error converting DER to PEM {:}".format(e))
            else:
                #print(f"\tI've created a {f.filename}-converted-to.pem file for you.")
                links.append(
                    {
                        f.filename+"-converted-to.pem:" : '<a href="'+UPLOAD_FOLDER+f.filename+'-converted-to.pem">'+f.filename+'-converted-to.pem</a>'
                    }
                )

        if fileformat == "p12":
            try:
                convert_p12_to_pem("website/" + UPLOAD_FOLDER+f.filename)
            except Exception as e:
                print("Error converting P12 to PEM {:}".format(e))
            else:
                #print(f"\tI've created a {f.filename}-converted-to.pem file for you.")
                links.append(
                    {
                        f.filename+"-converted-to.pem:" : '<a href="'+UPLOAD_FOLDER+f.filename+'-converted-to.pem">'+f.filename+'-converted-to.pem</a>'
                    }
                )

        if fileformat == "p7b":
            try:
                convert_p7b_to_pem("website/" + UPLOAD_FOLDER+f.filename)
            except Exception as e:
                print("Error converting P7B to PEM {:}".format(e))
            else:
                #print(f"\tI've created a {f.filename}-converted.pem file for you.")
                links.append(
                    {
                        f.filename+"-converted-to.pem:" : '<a href="'+UPLOAD_FOLDER+f.filename+'-converted-to.pem">'+f.filename+'-converted-to.pem</a>'
                    }
                )

        # Get the cert details from the converted pem file
        certdetails = get_pem_cert_details("website/" + UPLOAD_FOLDER + f.filename+"-converted-to.pem")

        return render_template("uploadsuccess.html", links=links, certdetails=certdetails)
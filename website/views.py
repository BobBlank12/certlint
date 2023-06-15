from flask import request, Blueprint, render_template, request, flash, url_for, send_file, session
from werkzeug.utils import secure_filename
import os
import sys
import subprocess
from certlint import *
import glob
import secrets

views = Blueprint('views', __name__)

def make_token():
    return secrets.token_urlsafe(32)

@views.route('/', methods=['GET', 'POST'])
def home():
    if not 'mysessionid' in session:
        print ("Creating mysessionid...")
        session['mysessionid'] = make_token()
        print(f"mysessionid={session['mysessionid']}")
    else:
        print(f"mysessionid already exists:{session['mysessionid']}")
    return render_template("index.html")

# Link to download "converted-to-pem file"
@views.route("/"+getuploadfolder()+"<filename>-converted-to.pem", methods=['GET', 'POST'])
def getFilePem(filename):
    return send_file(getuploadfolder()+session['mysessionid']+"/"+filename+"-converted-to.pem", as_attachment=True)

# Link to download "converted-to-der file"
@views.route("/"+getuploadfolder()+"<filename>-converted-to.der", methods=['GET', 'POST'])
def getFileDer(filename):
    return send_file(getuploadfolder()+session['mysessionid']+"/"+filename+"-converted-to.der", as_attachment=True)

# Link to download "ca extracted from P12/P7B file"
@views.route("/"+getuploadfolder()+"<filename>-extraxted-ca-certs.pem", methods=['GET', 'POST'])
def getFileP12ca(filename):
    return send_file(getuploadfolder()+session['mysessionid']+"/"+filename+"-extraxted-ca-certs.pem", as_attachment=True)

@views.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':
        # Cleanup any former posts/files
        oldfiles = glob.glob('website/'+ getuploadfolder() + session['mysessionid'] + "/*")
        for f in oldfiles:
            os.remove(f)

        if not os.path.exists('website/'+ getuploadfolder() + session['mysessionid'] + "/"):
            os.makedirs('website/'+ getuploadfolder() + session['mysessionid'], exist_ok=True)

        f = request.files['file']
        print ("saving file: website/" + getuploadfolder() + session['mysessionid'] + "/" + secure_filename(f.filename))
        f.save("website/" + getuploadfolder() + session['mysessionid'] + "/" + secure_filename(f.filename))
        f.close
        fileformat = "unknown"
        key_type = "n/a"

        # Determine the file format I've been given
        fileformat, key_type = determine_file_format("website/" + getuploadfolder() + session['mysessionid'] + "/" + f.filename, fileformat, key_type)

        #print(f"fileformat={fileformat}")

        # Convert to PEM from whatever I've received

        orig = []
        links = []
        certdetails = []

        orig.append(
            {
                "Original file: " : f.filename,
                "Original file format:" : fileformat,
                "Original key format:" : key_type
            }
        )

        if fileformat == "pem":
            try:
                convert_pem_to_pem("website/" + getuploadfolder() + session['mysessionid'] + "/" + f.filename)
            except Exception as e:
                print("Error converting PEM to PEM {:}".format(e))
            else:
                #print(f"\tI've created a {f.filename}-converted-to.pem file for you.")
                links.append(
                    {
                        f.filename+"-converted-to.pem:" : '<a href="'+getuploadfolder()+f.filename+'-converted-to.pem">'+f.filename+'-converted-to.pem</a>'
                    }
                )
        # End if fileformat = pem

        if fileformat == "der":
            try:
                convert_der_to_pem("website/" + getuploadfolder() + session['mysessionid'] + "/" + f.filename)
            except Exception as e:
                print("Error converting DER to PEM {:}".format(e))
            else:
                #print(f"\tI've created a {f.filename}-converted-to.pem file for you.")
                links.append(
                    {
                        f.filename+"-converted-to.pem:" : '<a href="'+getuploadfolder()+f.filename+'-converted-to.pem">'+f.filename+'-converted-to.pem</a>'
                    }
                )
        # End if fileformat = der

        if fileformat == "p12":
            try:
                convert_p12_to_pem("website/" + getuploadfolder() + session['mysessionid'] + "/" + f.filename)
            except Exception as e:
                print("Error converting P12 to PEM {:}".format(e))
            else:
                #print(f"\tI've created a {f.filename}-converted-to.pem file for you.")
                links.append(
                    {
                        f.filename+"-converted-to.pem:" : '<a href="'+getuploadfolder()+f.filename+'-converted-to.pem">'+f.filename+'-converted-to.pem</a>'
                    }
                )
            #Get the CAs out of the P12 file
            try:
                extract_ca_from_p12("website/" + getuploadfolder() + session['mysessionid'] + "/" + f.filename)
            except Exception as e:
                print("Error extracting the CA certs from the P12 file {:}".format(e))
            else:
                print(f"\tI've exctracted the ca certs from {f.filename} and saved into {f.filename}-extraxted-ca-certs.pem file for you.")
                links.append(
                    {
                        f.filename+"-extraxted-ca-certs.pem:" : '<a href="'+getuploadfolder()+f.filename+'-extraxted-ca-certs.pem">'+f.filename+'-extraxted-ca-certs.pem</a>'
                    }
                )
        # End if fileformat = p12

        if fileformat == "p7b":
            try:
                convert_p7b_to_pem("website/" + getuploadfolder() + session['mysessionid'] + "/" + f.filename)
            except Exception as e:
                print("Error converting P7B to PEM {:}".format(e))
            else:
                #print(f"\tI've created a {f.filename}-converted.pem file for you.")
                links.append(
                    {
                        f.filename+"-converted-to.pem:" : '<a href="'+getuploadfolder()+f.filename+'-converted-to.pem">'+f.filename+'-converted-to.pem</a>'
                    }
                )
            #Get the CAs out of the P7B file
            try:
                found_ca = extract_ca_from_p7b("website/" + getuploadfolder() + session['mysessionid'] + "/" + f.filename, session)
            except Exception as e:
                print("Error extracting all the certs from the P7B file {:}".format(e))
            else:
                if found_ca:
                    print(f"\tI've exctracted the ca certs from {f.filename} and saved into {f.filename}-extraxted-ca-certs.pem file for you.")
                    links.append(
                        {
                            f.filename+"-extraxted-ca-certs.pem:" : '<a href="'+getuploadfolder()+f.filename+'-extraxted-ca-certs.pem">'+f.filename+'-extraxted-ca-certs.pem</a>'
                        }
                    )
        # End if fileformat = p7b

        if fileformat != "key":
            # At this point I should have a clean PEM file I can create all of the other formats from...
            try:
                convert_pem_to_der("website/" + getuploadfolder() + session['mysessionid'] + "/" + f.filename)
            except Exception as e:
                print("Error converting PEM to DER {:}".format(e))
            else:
                #print(f"\tI've created a {f.filename}-converted-to.der file for you.")
                links.append(
                    {
                        f.filename+"-converted-to.der:" : '<a href="'+getuploadfolder()+f.filename+'-converted-to.der">'+f.filename+'-converted-to.der</a>'
                    }
                )
            # Get the cert details from the converted pem file
            certdetails = get_pem_cert_details("website/" + getuploadfolder() + session['mysessionid'] + "/" + f.filename+"-converted-to.pem")
        # End if fileformat != key

        return render_template("uploadsuccess.html", orig=orig, links=links, certdetails=certdetails)
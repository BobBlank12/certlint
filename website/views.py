from flask import request, Blueprint, render_template, flash, url_for, send_file, session
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

@views.route('/getcertdetails', methods=['GET', 'POST'])
def getcertdetails():
    return render_template("getcertdetails.html")

@views.route('/getcadetails', methods=['GET', 'POST'])
def getcadetails():
    return render_template("getcadetails.html")

@views.route('/createcert', methods=['GET','POST'])
def createcert():
    if request.method == 'POST':
        # Cleanup any former posts/files
        oldfiles = glob.glob('website/'+ getuploadfolder() + session['mysessionid'] + "/*")
        for f in oldfiles:
            os.remove(f)

        if not os.path.exists('website/'+ getuploadfolder() + session['mysessionid'] + "/"):
            os.makedirs('website/'+ getuploadfolder() + session['mysessionid'], exist_ok=True)

        links1 = []
        #links 2 will be used for the CA chain file(s)
        links2 = []

        cert_file_name = request.form.get("cert_file_name")
        cert_c = request.form.get("cert_c")
        cert_st = request.form.get("cert_st")
        cert_l = request.form.get("cert_l")
        cert_o = request.form.get("cert_o")
        cert_ou = request.form.get("cert_ou")
        cert_cn = request.form.get("cert_cn")
        cert_ip = request.form.get("cert_ip")
        cert_dns = request.form.get("cert_dns")

        intermediate_ca_key = request.files['intermediate_ca_key']
        if not intermediate_ca_key:
            return render_template("getcertdetails.html")
        intermediate_ca_key.save("website/" + getuploadfolder() + session['mysessionid'] + "/" + intermediate_ca_key.filename)
        intermediate_ca_key.close

        intermediate_ca_pem = request.files['intermediate_ca_pem']
        if not intermediate_ca_pem:
            return render_template("getcertdetails.html")
        intermediate_ca_pem.save("website/" + getuploadfolder() + session['mysessionid'] + "/" + intermediate_ca_pem.filename)
        intermediate_ca_pem.close

        root_ca_pem = request.files['root_ca_pem']
        if not root_ca_pem:
            return render_template("getcertdetails.html")
        root_ca_pem.save("website/" + getuploadfolder() + session['mysessionid'] + "/" + root_ca_pem.filename)
        root_ca_pem.close


# I should add a FLASH message here if the user doesn't select any CA files... right now it just reposts.

        try:
            create_certificate("website/" + getuploadfolder() + session['mysessionid'] + "/" + cert_file_name, cert_c, cert_st, cert_l, cert_o, cert_ou, cert_cn, cert_ip, cert_dns, "website/" + getuploadfolder() + session['mysessionid'] + "/" + intermediate_ca_pem.filename, "website/" + getuploadfolder() + session['mysessionid'] + "/" + intermediate_ca_key.filename,"website/" + getuploadfolder() + session['mysessionid'] + "/" + root_ca_pem.filename)
        except Exception as e:
            print("Error creating certificate {:}".format(e))
        else:
            print(f"\tI've created your certificate {cert_file_name}.key and {cert_file_name}.pem files for you.")
            links1.append(
                {
                    cert_file_name+".key:" : '<a href="'+getuploadfolder()+ cert_file_name+'.key">'+cert_file_name+'.key</a>',
                    cert_file_name+".pem:" : '<a href="'+getuploadfolder()+ cert_file_name+'.pem">'+cert_file_name+'.pem</a>'
                }
            )

        return render_template("certcreated.html", links1=links1)
       
    
@views.route('/createcachain', methods=['GET','POST'])
def createcachain():
    if request.method == 'POST':
        root_file_name = request.form.get("root_file_name")
        root_c = request.form.get("root_c")
        root_st = request.form.get("root_st")
        root_l = request.form.get("root_l")
        root_o = request.form.get("root_o")
        root_ou = request.form.get("root_ou")
        root_cn = request.form.get("root_cn")
        intermediate_file_name = request.form.get("intermediate_file_name")
        intermediate_c = request.form.get("intermediate_c")
        intermediate_st = request.form.get("intermediate_st")
        intermediate_l = request.form.get("intermediate_l")
        intermediate_o = request.form.get("intermediate_o")
        intermediate_ou = request.form.get("intermediate_ou")
        intermediate_cn = request.form.get("intermediate_cn")

        # Cleanup any former posts/files
        oldfiles = glob.glob('website/'+ getuploadfolder() + session['mysessionid'] + "/*")
        for f in oldfiles:
            os.remove(f)

        if not os.path.exists('website/'+ getuploadfolder() + session['mysessionid'] + "/"):
            os.makedirs('website/'+ getuploadfolder() + session['mysessionid'], exist_ok=True)

        links1 = []
        links2 = []

        try:
            create_cachain("website/" + getuploadfolder() + session['mysessionid'] + "/" + root_file_name, root_c, root_st, root_l, root_o, root_ou, root_cn, "website/" + getuploadfolder() + session['mysessionid'] + "/" + intermediate_file_name, intermediate_c, intermediate_st, intermediate_l, intermediate_o, intermediate_ou, intermediate_cn)
        except Exception as e:
            print("Error creating ca chain {:}".format(e))
        else:
            print(f"\tI've created your ROOT CA {root_file_name}.key and {root_file_name}.pem files for you.")
            links1.append(
                {
                    root_file_name+".key:" : '<a href="'+getuploadfolder()+ root_file_name+'.key">'+root_file_name+'.key</a>',
                    root_file_name+".pem:" : '<a href="'+getuploadfolder()+ root_file_name+'.pem">'+root_file_name+'.pem</a>'
                }
            )
            print(f"\tI've created your INTERMEDIATE CA {intermediate_file_name}.key and {intermediate_file_name}.pem files for you.")
            links2.append(
                {
                    intermediate_file_name+".key:" : '<a href="'+getuploadfolder()+ intermediate_file_name+'.key">'+intermediate_file_name+'.key</a>',
                    intermediate_file_name+".pem:" : '<a href="'+getuploadfolder()+ intermediate_file_name+'.pem">'+intermediate_file_name+'.pem</a>'
                }
            )
            
        return render_template("cachaincreated.html", links1=links1, links2=links2)
    
# End of createcachain()

@views.route('/validatekeypair', methods=['GET','POST'])
def validatekeypair():  
    return render_template("validatekeypair.html")

@views.route('/verifycertwithca', methods=['GET','POST'])
def verifycertwithca():  
    return render_template("verifycertwithca.html")

@views.route('/viewservercert', methods=['GET','POST'])
def viewservercert():  
    return render_template("viewservercert.html")

# Link to download "user created root ca key file"
@views.route("/"+getuploadfolder()+"<root_file_name>.key", methods=['GET', 'POST'])
def getRootCAFileKey(root_file_name):
    return send_file(getuploadfolder()+session['mysessionid']+"/"+root_file_name+".key", as_attachment=True)

# Link to download "user created root ca pem file"
@views.route("/"+getuploadfolder()+"<root_file_name>.pem", methods=['GET', 'POST'])
def getRootCAFilePem(root_file_name):
    return send_file(getuploadfolder()+session['mysessionid']+"/"+root_file_name+".pem", as_attachment=True)

# Link to download "user created intermediate ca key file"
@views.route("/"+getuploadfolder()+"<intermediate_file_name>.key", methods=['GET', 'POST'])
def getIntermediateCAFileKey(intermediate_file_name):
    return send_file(getuploadfolder()+session['mysessionid']+"/"+intermediate_file_name+".key", as_attachment=True)

# Link to download "user created intermediate ca pem file"
@views.route("/"+getuploadfolder()+"<intermediate_file_name>.pem", methods=['GET', 'POST'])
def getIntermediateCAFilePem(intermediate_file_name):
    return send_file(getuploadfolder()+session['mysessionid']+"/"+intermediate_file_name+".pem", as_attachment=True)

# Link to download "user created certificate key file"
@views.route("/"+getuploadfolder()+"<cert_file_name>.key", methods=['GET', 'POST'])
def getCertFileKey(cert_file_name):
    return send_file(getuploadfolder()+session['mysessionid']+"/"+cert_file_name+".key", as_attachment=True)

# Link to download "user created certificate pem file"
@views.route("/"+getuploadfolder()+"<cert_file_name>.pem", methods=['GET', 'POST'])
def getCertFilePem(cert_file_name):
    return send_file(getuploadfolder()+session['mysessionid']+"/"+cert_file_name+".pem", as_attachment=True)

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
        password=""
        password = request.form.get("pwd")
        
        # Cleanup any former posts/files
        oldfiles = glob.glob('website/'+ getuploadfolder() + session['mysessionid'] + "/*")
        for f in oldfiles:
            os.remove(f)

        if not os.path.exists('website/'+ getuploadfolder() + session['mysessionid'] + "/"):
            os.makedirs('website/'+ getuploadfolder() + session['mysessionid'], exist_ok=True)

        f = request.files['file']

        if not f:
            return render_template("index.html")

        print ("saving file: website/" + getuploadfolder() + session['mysessionid'] + "/" + secure_filename(f.filename))
        f.save("website/" + getuploadfolder() + session['mysessionid'] + "/" + secure_filename(f.filename))
        f.close
        fileformat = "unknown"
        key_type = "n/a"

        # Determine the file format I've been given
        fileformat, key_type = determine_file_format("website/" + getuploadfolder() + session['mysessionid'] + "/" + f.filename, fileformat, key_type, password)

        #print(f"fileformat={fileformat}")

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

            #Get the CAs out of the pem file
            try:
                found_ca = extract_ca_from_pem("website/" + getuploadfolder() + session['mysessionid'] + "/" + f.filename, session)
            except Exception as e:
                print("Error extracting all the certs from the PEM file {:}".format(e))
            else:
                if found_ca:
                    print(f"\tI've exctracted the ca certs from {f.filename} and saved into {f.filename}-extraxted-ca-certs.pem file for you.")
                    links.append(
                        {
                            f.filename+"-extraxted-ca-certs.pem:" : '<a href="'+getuploadfolder()+f.filename+'-extraxted-ca-certs.pem">'+f.filename+'-extraxted-ca-certs.pem</a>'
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
                convert_p12_to_pem("website/" + getuploadfolder() + session['mysessionid'] + "/" + f.filename, password)
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

        if fileformat in ("pem", "p12", "p7b", "der"): 
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
        # End if fileformat != key and not unknown

        return render_template("uploadsuccess.html", orig=orig, links=links, certdetails=certdetails)
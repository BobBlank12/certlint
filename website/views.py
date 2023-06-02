from flask import Blueprint, render_template, request, flash
import os
import subprocess

def determine_cert_type(filename, fileformat, key_format):
    #print (f"Determining the file type of: {filename}")

    # Order matters here since P12 files also show valid keys and DER formats
    # so P12 HAS to be last in this check.

    #Test for PEM format
    #print (f"Testing PEM format...")
    result = subprocess.call(["openssl", "x509", "-inform", "pem", "-in", filename, "-text", "-noout"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        fileformat = "pem"

    #Test for P7B format
    #print (f"Testing P7B format...")
    result = subprocess.call(["openssl", "pkcs7", "-in", filename, "-print_certs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        fileformat = "p7b"

    #Test for DER format
    #print (f"Testing DER format...")
    result = subprocess.call(["openssl", "x509", "-inform", "DER", "-in", filename, "-text", "-noout"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        fileformat = "der"

    #Test to see if it is a key, not a cert (that has no password for the key)
    #print (f"Testing if it is a key...")
    result= subprocess.call(["openssl", "rsa", "-in", filename, "-check", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        fileformat = "key"


    #Test for P12 (that has no password for the cert)
    #print (f"Testing P12 format...")
    result = subprocess.call(["openssl", "pkcs12", "-info", "-in", filename, "-nokeys", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        fileformat = "p12"

    # Notes on keys...
    #-----BEGIN PRIVATE KEY----- = pkcs8
    #-----BEGIN ENCRYPTED PRIVATE KEY----- pkcs8 encrypted
    #-----BEGIN RSA PRIVATE KEY----- = pkcs1

    # ??? Need to add a test for PFX?  If PFX doesn't store certs in DER format?

    #  JKS files?

    #print (f"\tIt appears you've given me a file that is in {format} format.")

    if fileformat == "key":
        with open(filename) as f:
            contents = f.readlines()
        key_format = "unknown"
        for line in contents:
            result= line.find("-----BEGIN PRIVATE KEY-----")
            if result != -1:
                key_format = "pkcs8"
                break
            result = line.find("-----BEGIN ENCRYPTED PRIVATE KEY-----")
            if result != -1:
                key_format = "pkcs8-encrypted"
                break
            result= line.find("-----BEGIN RSA PRIVATE KEY-----")
            if result != -1:
                key_format = "pkcs1"
                break
            result= line.find("-----BEGIN ENCRYPTED PRIVATE KEY-----")
            if result != -1:
                key_format = "pkcs8-encrypted"
                break
        # End of for loop through key file
        #print (f"\tThe key file appears to be in {key_format} format.")
    # End of key file checks
# End of determine_cert_type

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
        key_format = "n/a"
        fileformat = "unknown"

        #print (f"Determining the file type of: {filename}")

        # Order matters here since P12 files also show valid keys and DER formats
        # so P12 HAS to be last in this check.

        #Test for PEM format
        #print (f"Testing PEM format...")
        result = subprocess.call(["openssl", "x509", "-inform", "pem", "-in", certfile, "-text", "-noout"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
        if result == 0:
            fileformat = "pem"

        #Test for P7B format
        #print (f"Testing P7B format...")
        result = subprocess.call(["openssl", "pkcs7", "-in", certfile, "-print_certs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
        if result == 0:
            fileformat = "p7b"

        #Test for DER format
        #print (f"Testing DER format...")
        result = subprocess.call(["openssl", "x509", "-inform", "DER", "-in", certfile, "-text", "-noout"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
        if result == 0:
            fileformat = "der"

        #Test to see if it is a key, not a cert (that has no password for the key)
        #print (f"Testing if it is a key...")
        result= subprocess.call(["openssl", "rsa", "-in", certfile, "-check", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
        if result == 0:
            fileformat = "key"

        #Test for P12 (that has no password for the cert)
        #print (f"Testing P12 format...")
        result = subprocess.call(["openssl", "pkcs12", "-info", "-in", certfile, "-nokeys", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
        if result == 0:
            fileformat = "p12"

        # Notes on keys...
        #-----BEGIN PRIVATE KEY----- = pkcs8
        #-----BEGIN ENCRYPTED PRIVATE KEY----- pkcs8 encrypted
        #-----BEGIN RSA PRIVATE KEY----- = pkcs1

        # ??? Need to add a test for PFX?  If PFX doesn't store certs in DER format?
        #  JKS files?

        #print (f"\tIt appears you've given me a file that is in {format} format.")

        if fileformat == "key":
            with open(f.filename) as f:
                contents = f.readlines()
            for line in contents:
                result= line.find("-----BEGIN PRIVATE KEY-----")
                if result != -1:
                    key_format = "pkcs8"
                    break
                result = line.find("-----BEGIN ENCRYPTED PRIVATE KEY-----")
                if result != -1:
                    key_format = "pkcs8-encrypted"
                    break
                result= line.find("-----BEGIN RSA PRIVATE KEY-----")
                if result != -1:
                    key_format = "pkcs1"
                    break

            # End of for loop through key file
            #print (f"\tThe key file appears to be in {key_format} format.")
        # End of key file checks

        return render_template("uploadsuccess.html", name = certfile, fileformat = fileformat, key_format = key_format)


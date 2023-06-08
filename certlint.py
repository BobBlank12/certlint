import os
import sys
import subprocess

def determine_file_format(filename, fileformat, key_type):
    #filenames=["es01.p12","es01.der","es01.pkcs1.key","es01.pem","es01.p7b", "es01.pkcs8.key", "es01.pkcs8-encrypted.key"]
    print (f"Determining the file type of: {filename}")

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

    print (f"\tIt appears you've given me a file that is in {fileformat} format.")

    if fileformat == "key":
        with open(filename) as f:
            contents = f.readlines()
        key_type = "unknown"
        for line in contents:
            result= line.find("-----BEGIN PRIVATE KEY-----")
            if result != -1:
                key_type = "pkcs8"
                break
            result = line.find("-----BEGIN ENCRYPTED PRIVATE KEY-----")
            if result != -1:
                key_type = "pkcs8-encrypted"
                break
            result= line.find("-----BEGIN RSA PRIVATE KEY-----")
            if result != -1:
                key_type = "pkcs1"
                break
            result= line.find("-----BEGIN ENCRYPTED PRIVATE KEY-----")
            if result != -1:
                key_type = "pkcs8-encrypted"
                break
        # End of for loop through key file
        print (f"\tThe key file appears to be in {key_type} format.")
    # End of key file checks
    #print (f"")

    return fileformat, key_type

# End of determine_file_format

def get_pem_cert_details(filename):

    certdetails = []

    # Get the Subject:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-subject"], capture_output=True)
    subject = result.stdout.decode('utf-8').split('subject=', 1)[1].strip()
    print (f"Subject:{subject}")
    certdetails.append(
        {
            "Subject:" : subject.strip()
        }
    )

    # Get the subjectAltName:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-inform", "pem", "-ext", "subjectAltName"], capture_output=True)
    subjectaltnames = result.stdout.decode('utf-8')
    for subjectaltname in iter(subjectaltnames.splitlines()[1:]):
        print (f"Subject Alternate Names: {subjectaltname.strip()}")
        certdetails.append(
            {
                "Subject Alternate Names:" : subjectaltname.strip()
            }
        )

    # Get the Serial:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-serial"], capture_output=True)
    serial = result.stdout.decode('utf-8').split('serial=', 1)[1].strip()
    print (f"Serial:{serial}")
    certdetails.append(
        {
            "Serial:" : serial.strip()
        }
    )

    # Get the Fingerprint:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-fingerprint", "-sha256"], capture_output=True)
    fingerprint = result.stdout.decode('utf-8').split('sha256 Fingerprint=', 1)[1].strip()
    print (f"sha256 Fingerprint:{fingerprint}")
    certdetails.append(
        {
            "Fingerprint:" : fingerprint.strip()
        }
    )

    # Get the Startdate:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-startdate"], capture_output=True)
    startdate = result.stdout.decode('utf-8').split('notBefore=', 1)[1].strip()
    print (f"Not Before:{startdate}")
    certdetails.append(
        {
            "Not Before:" : startdate.strip()
        }
    )

    # Get the Enddate:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-enddate"], capture_output=True)
    enddate = result.stdout.decode('utf-8').split('notAfter=', 1)[1].strip()
    print (f"Not After:{enddate}")
    certdetails.append(
        {
            "Not After:" : enddate.strip()
        }
    )

    # Get the Basic Constraints:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-inform", "pem", "-ext", "basicConstraints"], capture_output=True)
    basicconstraints = result.stdout.decode('utf-8')
    for constraint in iter(basicconstraints.splitlines()[1:]):
        print (f"Basic Contraints: {constraint.strip()}")
        certdetails.append(
            {
                "Basic Constraints:" : constraint.strip()
            }
        )

    # Get the keyUsage:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-inform", "pem", "-ext", "keyUsage"], capture_output=True)
    keyusages = result.stdout.decode('utf-8')
    for keyusage in iter(keyusages.splitlines()[1:]):
        print (f"Key Usage: {keyusage.strip()}")
        certdetails.append(
            {
                "Key Usage:" : keyusage.strip()
            }
        )

    # Get the extendedKeyUsage:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-inform", "pem", "-ext", "extendedKeyUsage"], capture_output=True)
    extkeyusages = result.stdout.decode('utf-8')
    for extkeyusage in iter(extkeyusages.splitlines()[1:]):
        print (f"Extended Key Usage: {extkeyusage.strip()}")
        certdetails.append(
            {
                "Extended Key Usage:" : extkeyusage.strip()
            }
        )

    # Get Issuer:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-issuer"], capture_output=True)
    issuer = result.stdout.decode('utf-8').split('issuer=', 1)[1].strip()
    print (f"Issuer:{issuer}")
    certdetails.append(
        {
            "Issuer:" : issuer.strip()
        }
    )

    return certdetails

# End of get_pem_cert_details

def convert_der_to_pem(filename):
    result = subprocess.call(["openssl", "x509", "-inform", "der", "-in", filename, "-out", filename + "-converted-to.pem"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    return(result)
# End of convert_der_to_pem

def convert_p12_to_pem(filename):
    #
    # This is in 2 passes... to JUST get the node cert and not the ca certs
    #
    # I should get the CA certs for the user out of the bundle as well... TODO.
    #
    result1 = subprocess.call(["openssl", "pkcs12", "-in", filename, "-nodes", "-nokeys", "-out", filename + "-temp.pem", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result1 == 0:
        #Save JUST the node cert from the temp PEM file... if there happened to be a ca chain in the P12... for consistency
        result2 = subprocess.call(["openssl", "x509", "-in", filename + "-temp.pem", "-out", filename + "-converted-to.pem", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
        os.remove(filename+"-temp.pem")
    return (result1+result2) 
# End of convert_p12_to_pem

def convert_pem_to_pem(filename):
    #
    # This is just in case there are multiple certs (a chain) in the pem file.
    #
    result = subprocess.call(["openssl", "x509", "-in", filename, "-out", filename + "-converted-to.pem"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    return (result) 
# End of convert_pem_to_pem


def convert_p7b_to_pem(filename):
    #
    # This is in 2 passes... to JUST get the node cert and not the ca certs
    #
    # I should get the CA certs for the user out of the bundle as well... TODO.
    #
    #openssl pkcs7 -print_certs -in certificate.p7b -out certificate.cer
    result1 = subprocess.call(["openssl", "pkcs7", "-print_certs", "-in", filename, "-out", filename + "-temp.pem"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result1 == 0:
        result2 = subprocess.call(["openssl", "x509", "-in", filename + "-temp.pem", "-out", filename + "-converted-to.pem", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
        os.remove(filename+"-temp.pem")
    return (result1+result2) 
# End of convert_p7b_to_pem
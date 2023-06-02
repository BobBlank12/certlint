import os
import subprocess


######################

######################

os.system("clear")

filenames=["es01.p12","es01.der","es01.pkcs1.key","es01.pem","es01.p7b", "es01.pkcs8.key", "es01.pkcs8-encrypted.key"]
for filename in filenames:

    print (f"Determining the file type of: {filename}")

    # Order matters here since P12 files also show valid keys and DER formats
    # so P12 HAS to be last in this check.

    #Test for PEM format
    #print (f"Testing PEM format...")
    result = subprocess.call(["openssl", "x509", "-inform", "pem", "-in", filename, "-text", "-noout"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        format = "pem"

    #Test for P7B format
    #print (f"Testing P7B format...")
    result = subprocess.call(["openssl", "pkcs7", "-in", filename, "-print_certs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        format = "p7b"

    #Test for DER format
    #print (f"Testing DER format...")
    result = subprocess.call(["openssl", "x509", "-inform", "DER", "-in", filename, "-text", "-noout"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        format = "der"

    #Test to see if it is a key, not a cert (that has no password for the key)
    #print (f"Testing if it is a key...")
    result= subprocess.call(["openssl", "rsa", "-in", filename, "-check", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        format = "key"


    #Test for P12 (that has no password for the cert)
    #print (f"Testing P12 format...")
    result = subprocess.call(["openssl", "pkcs12", "-info", "-in", filename, "-nokeys", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        format = "p12"

    # Notes on keys...
    #-----BEGIN PRIVATE KEY----- = pkcs8
    #-----BEGIN ENCRYPTED PRIVATE KEY----- pkcs8 encrypted
    #-----BEGIN RSA PRIVATE KEY----- = pkcs1

    # ??? Need to add a test for PFX?  If PFX doesn't store certs in DER format?

    #  JKS files?

    print (f"\tIt appears you've given me a file that is in {format} format.")

    if format == "key":
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
    print (f"")
# End of for loop through file list


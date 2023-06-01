import os
import subprocess


######################

######################

os.system("clear")

filenames=["es01.p12","es01.der","es01.key","es01.pem","es01.p7b"]
for filename in filenames:

    print (f"Dertermining the file type of: {filename}")

    #Test for P12 (that has no password for the cert)
    #print (f"Testing P12 format...")
    p12_format = subprocess.call(["openssl", "pkcs12", "-info", "-in", filename, "-nokeys", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    print (f"p12_format={p12_format}")

    #Test for PEM format
    #print (f"Testing PEM format...")
    pem_format = subprocess.call(["openssl", "x509", "-inform", "pem", "-in", filename, "-text", "-noout"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    print (f"pem_format={pem_format}")

    #Test for P7B format
    #print (f"Testing P7B format...")
    p7b_format = subprocess.call(["openssl", "pkcs7", "-in", filename, "-print_certs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    print (f"p7b_format={p7b_format}")

    #Test for DER format
    #print (f"Testing DER format...")
    der_format = subprocess.call(["openssl", "x509", "-inform", "DER", "-in", filename, "-text", "-noout"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    print (f"der_format={der_format}")

    #Test to see if it is a key, not a cert
    #print (f"Testing if it is a key...")
    key_format = subprocess.call(["openssl", "rsa", "-in", filename, "-check"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    print (f"key_format={key_format}")
 
    # NEED TO ADD A TEST HERE TO SEE WHAT FORMAT THE KEY IS IN...

    # ??? Need to add a test for PFX?  If PFX doesn't store certs in DER format?

    #  JKS files?

    


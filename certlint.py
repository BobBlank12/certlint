import os
import subprocess


######################

######################

#os.system("clear")

#filename="es01.p12"
#filename="es01.der"
#filename="es01.key"
#filename="es01.pem"
filename="es01.p7b"

print (f"Dertermining the file type of: {filename}\n")

#Test for P12 (that has no password for the cert)
print (f"Testing P12 format...")
p12_format = subprocess.call(["openssl", "pkcs12", "-info", "-in", filename, "-nokeys", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
print (f"p12_format={p12_format}\n")

#Test for PEM format
print (f"Testing PEM format...")
pem_format = subprocess.call(["openssl", "x509", "-inform", "pem", "-in", filename, "-text", "-noout"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
print (f"pem_format={pem_format}\n")

#Test for P7B format
print (f"Testing P7B format...")
p7b_format = subprocess.call(["openssl", "pkcs7", "-in", filename, "-print_certs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
print (f"p7b_format={p7b_format}\n")

#Test for DER format
print (f"Testing DER format...")
der_format = subprocess.call(["openssl", "x509", "-inform", "DER", "-in", filename, "-text", "-noout"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
print (f"der_format={der_format}\n")
"""
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os

with open(filename, "rb") as f:
    cert= x509.load_pem_x509_certificate(f.read(), default_backend())

print (f"Serial Number: {cert.serial_number}")
print (f"Extensions: {cert.extensions}")

fingerprint_hashed_byte_string = cert.fingerprint(hashes.SHA256())
fingerprint_hex_string = ':'.join([format(byte, '02x') for byte in fingerprint_hashed_byte_string])
print (f"Fingerprint: {fingerprint_hex_string}")
print (f"Issuer: {cert.issuer}")
print (f"Not Valid Before: {cert.not_valid_before}")
print (f"Not Valid After: {cert.not_valid_after}")
"""

"""
OR SIMPLY USING OPENSSL...

openssl x509 -in es01.pem -noout -subject
subject=C = US, ST = Minneosta, L = Bloomington, O = TEST-CERTS, OU = CERTS, CN = es01

openssl x509 -in es01.pem -noout -serial
serial=12D498EEF25477293EE0CB9A287E530FE2466EF2

openssl x509 -noout -fingerprint -sha256 -inform pem -in es01.pem
sha256 Fingerprint=69:B5:89:3E:7C:9F:D8:70:B1:B5:55:97:B3:87:43:CB:3F:55:D1:0E:8E:D6:58:9B:19:7E:CA:F6:B3:F5:17:50

openssl x509 -noout -ext basicConstraints -inform pem -in es01.pem
X509v3 Basic Constraints: 
    CA:FALSE

openssl x509 -noout -ext keyUsage -inform pem -in es01.pem
X509v3 Key Usage: 
    Digital Signature, Non Repudiation, Key Encipherment, Data Encipherment

openssl x509 -noout -ext extendedKeyUsage -inform pem -in es01.pem
X509v3 Extended Key Usage: 
    TLS Web Server Authentication, TLS Web Client Authentication

openssl x509 -in es01.pem -noout -ext subjectAltName
X509v3 Subject Alternative Name: 
    DNS:es01, IP Address:127.0.0.1, DNS:localhost

openssl x509 -in es01.pem -noout -startdate
notBefore=Apr 18 15:36:36 2023 GMT

openssl x509 -in es01.pem -noout -enddate
notAfter=Apr 17 15:36:36 2025 GMT

openssl x509 -in es01.pem -noout -issuer
issuer=C = US, ST = Minneosta, L = Bloomington, O = TEST-CA, OU = CERTS, CN = INTERMEDIATE-CA

"""

import os
import subprocess
# Get the Subject:
result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-subject"], capture_output=True)
subject = result.stdout.decode('utf-8').split('subject=', 1)[1].strip()
print (f"Subject:{subject}")

# Get the subjectAltName:
result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-inform", "pem", "-ext", "subjectAltName"], capture_output=True)
subjectaltnames = result.stdout.decode('utf-8')
for subjectaltname in iter(subjectaltnames.splitlines()[1:]):
    print (f"Subject Alternate Names: {subjectaltname.strip()}")

# Get the Serial:
result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-serial"], capture_output=True)
serial = result.stdout.decode('utf-8').split('serial=', 1)[1].strip()
print (f"Serial:{serial}")

# Get the Fingerprint:
result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-fingerprint", "-sha256"], capture_output=True)
fingerprint = result.stdout.decode('utf-8').split('sha256 Fingerprint=', 1)[1].strip()
print (f"sha256 Fingerprint:{fingerprint}")

# Get the Startdate:
result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-startdate"], capture_output=True)
startdate = result.stdout.decode('utf-8').split('notBefore=', 1)[1].strip()
print (f"Not Before:{startdate}")

# Get the Enddate:
result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-enddate"], capture_output=True)
enddate = result.stdout.decode('utf-8').split('notAfter=', 1)[1].strip()
print (f"Not After:{enddate}")

# Get the Basic Constraints:
result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-inform", "pem", "-ext", "basicConstraints"], capture_output=True)
basicconstraints = result.stdout.decode('utf-8')
for constraint in iter(basicconstraints.splitlines()[1:]):
    print (f"Basic Contraints: {constraint.strip()}")

# Get the keyUsage:
result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-inform", "pem", "-ext", "keyUsage"], capture_output=True)
keyusages = result.stdout.decode('utf-8')
for keyusage in iter(keyusages.splitlines()[1:]):
    print (f"Key Usage: {keyusage.strip()}")

# Get the extendedKeyUsage:
result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-inform", "pem", "-ext", "extendedKeyUsage"], capture_output=True)
extkeyusages = result.stdout.decode('utf-8')
for extkeyusage in iter(extkeyusages.splitlines()[1:]):
    print (f"Extended Key Usage: {extkeyusage.strip()}")

# Get Issuer:
result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-issuer"], capture_output=True)
issuer = result.stdout.decode('utf-8').split('issuer=', 1)[1].strip()
print (f"Issuer:{issuer}")
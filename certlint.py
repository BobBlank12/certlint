import os
import sys
import subprocess

def getuploadfolder():
    return "uploads/" 

def create_certificate(cert_file_name,cert_c,cert_st,cert_l,cert_o,cert_ou,cert_cn,cert_ip,cert_dns,intermediate_ca_pem,intermediate_ca_key,root_ca_pem):

    #create_server_private_key
    #openssl genrsa -out $1.key 2048
    result = subprocess.run(["openssl", "genrsa", "-out", cert_file_name+".key", "2048"], capture_output=True, shell=False, timeout=20)
    print (result.stdout.decode("utf-8"))
    print (result.stderr.decode("utf-8"))

    #create_intermediate_csr.conf
    csr_conf = open(cert_file_name+"_csr.conf","w")
    csr_conf.write("[ req ]"+"\n")
    csr_conf.write("default_bits = 2048"+"\n")
    csr_conf.write("prompt = no"+"\n")
    csr_conf.write("default_md = sha256"+"\n")
    csr_conf.write("req_extensions = req_ext"+"\n")
    csr_conf.write("distinguished_name = dn"+"\n")
    csr_conf.write("[ dn ]"+"\n")
    csr_conf.write("C = " + cert_c+"\n")
    csr_conf.write("ST = " + cert_st+"\n")
    csr_conf.write("L = " + cert_l+"\n")
    csr_conf.write("O = " + cert_o+"\n")
    csr_conf.write("OU = " + cert_ou+"\n")
    csr_conf.write("CN = " + cert_cn+"\n")
    csr_conf.write("[ req_ext ]"+"\n")
    csr_conf.write("subjectAltName = @alt_names"+"\n")
    csr_conf.write("[ alt_names ]"+"\n")
    csr_conf.write("DNS.1 = " + cert_cn+"\n")
    csr_conf.write("DNS.2 = " + cert_dns+"\n")
    csr_conf.write("IP.1 = " + cert_ip+"\n")
    csr_conf.close()

    #create_server_csr
    #openssl req -new -key $1.key -out $1.csr -config $1_csr.conf
    result = subprocess.run(["openssl", "req", "-new", "-key", cert_file_name+".key", "-out", cert_file_name+".csr", "-config", cert_file_name+"_csr.conf"], capture_output=True, shell=False, timeout=3)
    print (result.stdout.decode("utf-8"))
    print (result.stderr.decode("utf-8"))

    #create_server_cert.conf
    csr_conf = open(cert_file_name+"_cert.conf","w")
    csr_conf.write("authorityKeyIdentifier=keyid,issuer"+"\n")
    csr_conf.write("basicConstraints=CA:FALSE"+"\n")
    csr_conf.write("keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment"+"\n")
    csr_conf.write("subjectAltName = @alt_names"+"\n")
    csr_conf.write("[alt_names]"+"\n")
    csr_conf.write("DNS.1 = "+cert_cn+"\n")
    csr_conf.write("DNS.2 = "+cert_dns+"\n")
    csr_conf.write("IP.1 = "+cert_ip+"\n")
    csr_conf.close()

    #create_server_cert()
    #openssl x509 -req \
    #    -in $1.csr \
    #    -CA intermediateCA.crt -CAkey intermediateCA.key \
    #    -CAcreateserial -out $1.pem \
    #    -days 730 \
    #    -sha256 -extfile $1_cert.conf

    result = subprocess.run(["openssl", "x509", "-req", "-in", cert_file_name+".csr", "-out", cert_file_name+".pem", "-extfile", cert_file_name+"_cert.conf","-CA", intermediate_ca_pem, "-CAkey", intermediate_ca_key, "-CAcreateserial", "-days", "730", "-sha256"], capture_output=True, shell=False, timeout=3)
    print (result.stdout.decode("utf-8"))
    print (result.stderr.decode("utf-8"))

    return (result.returncode)

# End of create_certificate


def create_cachain(root_file_name,root_c,root_st,root_l,root_o,root_ou,root_cn,intermediate_file_name,intermediate_c,intermediate_st,intermediate_l,intermediate_o,intermediate_ou,intermediate_cn):

#        openssl req -x509 \
#            -sha256 -days 3560 \
#            -nodes \
#            -newkey rsa:4096 \
#            -subj "/CN=ROOT-CA/C=US/ST=Minnesota/L=Bloomington/O=TEST-CA/OU=CERTS" \
#            -keyout rootCA.key -out rootCA.crt 

    subj = "/CN="+root_cn+"/C="+root_c+"/ST="+root_st+"/L="+root_l+"/O="+root_o+"/OU="+root_ou
    result = subprocess.run(["openssl", "req", "-x509", "-sha256", "-days", "3560", "-nodes", "-newkey", "rsa:4096", "-subj", subj, "-keyout", root_file_name+".key", "-out", root_file_name+".pem"], capture_output=True, shell=False, timeout=20)
    #print (result.stdout.decode("utf-8"))
    #print (result.stderr.decode("utf-8"))

    #create_intermediate_private_key
    # openssl genrsa -out intermediateCA.key 4096
    result = subprocess.run(["openssl", "genrsa", "-out", intermediate_file_name+".key", "4096"], capture_output=True, shell=False, timeout=20)
    print (result.stdout.decode("utf-8"))
    print (result.stderr.decode("utf-8"))

    #create_intermediate_csr.conf
    csr_conf = open(intermediate_file_name+"_csr.conf","w")
    csr_conf.write("[ req ]"+"\n")
    csr_conf.write("default_bits = 4096"+"\n")
    csr_conf.write("prompt = no"+"\n")
    csr_conf.write("default_md = sha256"+"\n")
    csr_conf.write("req_extensions = req_ext"+"\n")
    csr_conf.write("distinguished_name = dn"+"\n")
    csr_conf.write("[ dn ]"+"\n")
    csr_conf.write("C = " + intermediate_c+"\n")
    csr_conf.write("ST = " + intermediate_st+"\n")
    csr_conf.write("L = " + intermediate_l+"\n")
    csr_conf.write("O = " + intermediate_o+"\n")
    csr_conf.write("OU = " + intermediate_ou+"\n")
    csr_conf.write("CN = " + intermediate_cn+"\n")
    csr_conf.write("[ req_ext ]"+"\n")
    csr_conf.write("subjectAltName = @alt_names"+"\n")
    csr_conf.write("[ alt_names ]"+"\n")
    csr_conf.write("DNS.1 = " + intermediate_cn+"\n")
    csr_conf.close()

    #create_intermediate_csr
    #openssl req -new -key intermediateCA.key -out intermediateCA.csr -config intermediateCA_csr.conf
    result = subprocess.run(["openssl", "req", "-new", "-key", intermediate_file_name+".key", "-out", intermediate_file_name+".csr", "-config", intermediate_file_name+"_csr.conf"], capture_output=True, shell=False, timeout=3)
    print (result.stdout.decode("utf-8"))
    print (result.stderr.decode("utf-8"))

    #create_intermediate_cert.conf
    csr_conf = open(intermediate_file_name+"_cert.conf","w")
    csr_conf.write("authorityKeyIdentifier=keyid,issuer"+"\n")
    csr_conf.write("basicConstraints=critical,CA:TRUE"+"\n")
    csr_conf.write("keyUsage = critical, digitalSignature, cRLSign, keyCertSign"+"\n")
    csr_conf.write("subjectAltName = @alt_names"+"\n")
    csr_conf.write("[alt_names]"+"\n")
    csr_conf.write("DNS.1 = "+intermediate_cn+"\n")
    csr_conf.close()

    #create_intermediate_cert
    # openssl x509 -req \
    #  -in intermediateCA.csr \
    #  -CA rootCA.crt -CAkey rootCA.key \
    #  -CAcreateserial -out intermediateCA.crt \
    #  -days 3649 \
    #  -sha256 -extfile intermediateCA_cert.conf   
    result = subprocess.run(["openssl", "x509", "-req", "-in", intermediate_file_name+".csr", "-out", intermediate_file_name+".pem", "-extfile", intermediate_file_name+"_cert.conf","-CA", root_file_name+".pem", "-CAkey", root_file_name+".key", "-CAcreateserial", "-days", "3649", "-sha256"], capture_output=True, shell=False, timeout=3)
    print (result.stdout.decode("utf-8"))
    print (result.stderr.decode("utf-8"))

    return (result.returncode)

# End of create_cachain

def determine_file_format(filename, fileformat, key_type, password):
    #filenames=["es01.p12","es01.der","es01.pkcs1.key","es01.pem","es01.p7b", "es01.pkcs8.key", "es01.pkcs8-encrypted.key"]
    print (f"Determining the file type of: {filename}")

    # Order matters here since P12 files also show valid keys and DER formats
    # so P12 HAS to be last in this check.

    #Test for PEM format
    print (f"Testing PEM format...")
    result = subprocess.call(["openssl", "x509", "-inform", "pem", "-in", filename, "-text", "-noout"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        fileformat = "pem"

    #Test for P7B format
    print (f"Testing P7B format...")
    result = subprocess.call(["openssl", "pkcs7", "-in", filename, "-print_certs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        fileformat = "p7b"

    #Test for DER format
    print (f"Testing DER format...")
    result = subprocess.call(["openssl", "x509", "-inform", "DER", "-in", filename, "-text", "-noout", "-passin", "pass:"+password], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        fileformat = "der"

    #Test to see if it is a key, not a cert (that has no password for the key)
    print (f"Testing if it is a key...")
    result= subprocess.call(["openssl", "rsa", "-in", filename, "-check", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result == 0:
        fileformat = "key"

    #Test for P12
    print (f"Testing P12 format...")
    result = subprocess.run(["openssl", "pkcs12", "-info", "-in", filename, "-nokeys", "-passin", "pass:"+password], shell=False, timeout=3, capture_output=True)
    if result.returncode == 0:
        fileformat = "p12"
    elif result.stderr.decode("utf-8").find("invalid password") != -1:
        fileformat = "P12 with a bad password"

    # ??? Need to add a test for PFX?  If PFX doesn't store certs in DER format?
    #  JKS files?

    print (f"\tIt appears you've given me a file that is in format: {fileformat}")

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

    print (f"filename={filename}")

    # Get the Subject:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-subject"], capture_output=True)
    subject = result.stdout.decode('utf-8').split('subject=', 1)[1].strip()
    #print (f"Subject:{subject}")
    certdetails.append(
        {
            "Subject:" : subject.strip()
        }
    )

    # Get the subjectAltName:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-inform", "pem", "-ext", "subjectAltName"], capture_output=True)
    subjectaltnames = result.stdout.decode('utf-8')
    for subjectaltname in iter(subjectaltnames.splitlines()[1:]):
        #print (f"Subject Alternate Names: {subjectaltname.strip()}")
        certdetails.append(
            {
                "Subject Alternate Names:" : subjectaltname.strip()
            }
        )

    # Get the Serial:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-serial"], capture_output=True)
    serial = result.stdout.decode('utf-8').split('serial=', 1)[1].strip()
    #print (f"Serial:{serial}")
    certdetails.append(
        {
            "Serial:" : serial.strip()
        }
    )

    # Get the Fingerprint:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-fingerprint", "-sha256"], capture_output=True)
    #print(f"Fingerprint Output = {result.stdout.decode('utf-8')}")
    fingerprint = result.stdout.decode('utf-8').upper().split('SHA256 FINGERPRINT=', 1)[1].strip()
    #print (f"sha256 Fingerprint:{fingerprint}")
    certdetails.append(
        {
            "Fingerprint:" : fingerprint.strip()
        }
    )

    # Get the Startdate:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-startdate"], capture_output=True)
    startdate = result.stdout.decode('utf-8').split('notBefore=', 1)[1].strip()
    #print (f"Not Before:{startdate}")
    certdetails.append(
        {
            "Not Before:" : startdate.strip()
        }
    )

    # Get the Enddate:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-enddate"], capture_output=True)
    enddate = result.stdout.decode('utf-8').split('notAfter=', 1)[1].strip()
    #print (f"Not After:{enddate}")
    certdetails.append(
        {
            "Not After:" : enddate.strip()
        }
    )

    # Get the Basic Constraints:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-inform", "pem", "-ext", "basicConstraints"], capture_output=True)
    basicconstraints = result.stdout.decode('utf-8')
    for constraint in iter(basicconstraints.splitlines()[1:]):
        #print (f"Basic Contraints: {constraint.strip()}")
        certdetails.append(
            {
                "Basic Constraints:" : constraint.strip()
            }
        )

    # Get the keyUsage:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-inform", "pem", "-ext", "keyUsage"], capture_output=True)
    keyusages = result.stdout.decode('utf-8')
    for keyusage in iter(keyusages.splitlines()[1:]):
        #print (f"Key Usage: {keyusage.strip()}")
        certdetails.append(
            {
                "Key Usage:" : keyusage.strip()
            }
        )

    # Get the extendedKeyUsage:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-inform", "pem", "-ext", "extendedKeyUsage"], capture_output=True)
    extkeyusages = result.stdout.decode('utf-8')
    for extkeyusage in iter(extkeyusages.splitlines()[1:]):
        #print (f"Extended Key Usage: {extkeyusage.strip()}")
        certdetails.append(
            {
                "Extended Key Usage:" : extkeyusage.strip()
            }
        )

    # Get Issuer:
    result = subprocess.run(["openssl", "x509", "-in", filename, "-noout", "-issuer"], capture_output=True)
    issuer = result.stdout.decode('utf-8').split('issuer=', 1)[1].strip()
    #print (f"Issuer:{issuer}")
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

def convert_pem_to_der(filename):
    # Use the clean PEM file I have already converted
    result = subprocess.call(["openssl", "x509", "-outform", "der", "-in", filename + "-converted-to.pem", "-out", filename + "-converted-to.der"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    return(result)
# End of convert_pem_to_der

def convert_p12_to_pem(filename, password):
    #print (f"filename={filename}")
    #
    # This is in 2 passes... to JUST get the node cert and not the ca certs
    #
    # I should get the CA certs for the user out of the bundle as well... TODO.
    #
    result1 = subprocess.call(["openssl", "pkcs12", "-in", filename, "-nodes", "-nokeys", "-out", filename + "-temp.pem", "-passin", "pass:"+password], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
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
    #openssl pkcs7 -print_certs -in certificate.p7b -out certificate.cer
    result1 = subprocess.call(["openssl", "pkcs7", "-print_certs", "-in", filename, "-out", filename + "-temp.pem"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if result1 == 0:
        result2 = subprocess.call(["openssl", "x509", "-in", filename + "-temp.pem", "-out", filename + "-converted-to.pem", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
        os.remove(filename+"-temp.pem")
    return (result1+result2) 
# End of convert_p7b_to_pem

def extract_ca_from_p12(filename):
    result = subprocess.call(["openssl", "pkcs12", "-nodes", "-cacerts", "-nokeys", "-in", filename, "-out", filename + "-extraxted-ca-certs.pem", "-passin", "pass:"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    if os.path.getsize(filename + "-extraxted-ca-certs.pem") == 0:
        os.remove(filename + "-extraxted-ca-certs.pem")
        raise Exception("No CA certs found in " + filename + " to extract.")
    return (result) 

# End of extract_ca_from_p12

def extract_ca_from_p7b(filename,session):
    #openssl pkcs7 -in node-and-cas.p7b -print_certs -out temp.pem -outform pem
    result = subprocess.call(["openssl", "pkcs7", "-print_certs", "-in", filename, "-out", filename + "-all-extracted-certs.pem"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    found_ca = get_cas_from_pem_file(filename,session)
    os.remove(filename + "-all-extracted-certs.pem")
    return (found_ca) 

# End of extract_ca_from_p7b

def extract_ca_from_pem(filename,session):

# Two step process... first to a P7B then extract the chain.
# openssl crl2pkcs7 -nocrl -certfile node-and-cas.pem | openssl pkcs7 -print_certs -text
    result = subprocess.call(["openssl", "crl2pkcs7", "-nocrl", "-certfile", filename, "-out", filename + "-temp.p7b"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    result = subprocess.call(["openssl", "pkcs7", "-print_certs", "-in", filename + "-temp.p7b", "-out", filename + "-all-extracted-certs.pem"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False, timeout=3)
    found_ca = get_cas_from_pem_file(filename,session)
    os.remove(filename + "-all-extracted-certs.pem")
    os.remove(filename + "-temp.p7b")
    return (found_ca) 

# End of extract_ca_from_pem


def get_cas_from_pem_file(filename,session):

    input_file = filename + "-all-extracted-certs.pem"
    output_file_prefix = "website/" + getuploadfolder() + session['mysessionid'] + "/" + "temp-"

    # Read the PEM file
    with open(input_file, "r") as file:
        data = file.readlines()

    pem_data = iter(data)
    i = 1

    for line in pem_data:
        if line.startswith("-----BEGIN CERTIFICATE-----"):
            output_file = f"{output_file_prefix}{i}.pem"
            with open(output_file, "w") as file:
                file.write(line)
                line = next(pem_data)
                while not line.startswith("-----END CERTIFICATE-----"):
                    file.write(line)
                    line = next(pem_data)
                else:
                    file.write("-----END CERTIFICATE-----\n")
                    file.close()
                    #print(f"Certificate {i} saved to {output_file}")
                    i=i+1
    
    found_ca = False

    for x in range(1, i):
        z = 1
        # Get the Basic Constraints:
        tempfile = output_file_prefix + str(x) + ".pem"
        result = subprocess.run(["openssl", "x509", "-in", tempfile , "-noout", "-inform", "pem", "-ext", "basicConstraints"], capture_output=True)
        basicconstraints = result.stdout.decode('utf-8')
        for constraint in iter(basicconstraints.splitlines()[1:]):
            if constraint.strip().find("CA:FALSE") != -1:
                # this cert is NOT a CA... get rid of it.
                #print ("temp-"+str(x)+".pem is NOT a CA file")
                os.remove(output_file_prefix + str(x) + ".pem")
            elif constraint.strip().find("CA:TRUE") != -1:
                # I may split the root and intermediate ca cert(s) out in the future...
                """

                # Here we should determine if it is the ROOT. ISS and SUBJ are equal
                # We should rename it and add a link to the dictionary for the Web Page for it
                #print ("temp-"+str(x)+".pem is a CA file")

                # Get the Subject:
                result = subprocess.run(["openssl", "x509", "-in", tempfile, "-noout", "-subject"], capture_output=True)
                subject = result.stdout.decode('utf-8').split('subject=', 1)[1].strip()
                #print (f"Subject:{subject}")

                # Get Issuer:
                result = subprocess.run(["openssl", "x509", "-in", tempfile, "-noout", "-issuer"], capture_output=True)
                issuer = result.stdout.decode('utf-8').split('issuer=', 1)[1].strip()
                #print (f"Issuer:{issuer}")

                if issuer == subject:
                    #This is the ROOT CA
                    os.rename("temp-"+str(x)+".pem", "ca-root-extracted-from-p7b.pem")
                    cadetails.append(
                        {
                            "ROOT CA:" : "ca-root-extracted-from-p7b.pem"
                        }
                    )
                else:
                    os.rename("temp-"+str(x)+".pem", "ca-intermediate-" + str(z) + "extracted-from-p7b.pem")
                    cadetails.append(
                        {
                            "Intermediate CA-" + str(z) + ".pem:" : "ca-intermediate-" + str(z) + "extracted-from-p7b.pem"
                        }
                    )
                    z=z+1
                """
                found_ca = True
                with open(filename + "-extraxted-ca-certs.pem", "a") as fo:
                    #print("trying to process file: " + output_file_prefix + "-" + str(x) + ".pem")
                    with open(output_file_prefix + str(x) + ".pem",'r') as fi: fo.write(fi.read())
                fo.close()
                os.remove(output_file_prefix + str(x) + ".pem")
            else:
                print ("I found a cert that I cannot determine if it is a CA or NOT based on the basic constraints")
            
            # End if the temp file is a CA or not.
        # End of looping through the basic constraints
    # End of looping through each temp.pem file to test it

    return(found_ca)
    # End get_cas_from_pem_file
from OpenSSL import crypto,SSL
from socket import gethostname

certFile='./cert/selfsigned.crt'
keyFile='./cert/selfsigned.key'

def genSelfsignedCert():
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "CN"
    cert.get_subject().ST = "BeiJing"
    cert.get_subject().L = "BeiJing"
    cert.get_subject().O = "C919"
    cert.get_subject().OU = "C919"
    cert.get_subject().CN = 'pan.c919.com'
    cert.set_serial_number(23333)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k,'sha512')
    # output cert
    with open(certFile, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    # output key
    with open(keyFile, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))
    print('selfsigned success')

if __name__=='__main__':
    genSelfsignedCert()
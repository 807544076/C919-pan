from os import path, mkdir, urandom
import rsa
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad
import hashlib
from linksql import C919SQL


keyPath = './userKey/'


def create_key(uid):
    user_path = keyPath + str(uid) + '/user/'
    server_path = keyPath + str(uid) + '/server/'
    if not path.exists(keyPath + str(uid)):
        mkdir(keyPath + str(uid))
        mkdir(user_path)
        mkdir(server_path)

    (u_pubkey, u_privkey) = rsa.newkeys(1024)  # 客户端公私钥对
    (s_pubkey, s_privkey) = rsa.newkeys(1024)  # 服务端公私钥对

    u_pubk = u_pubkey.save_pkcs1()
    f = open(user_path + 'public_key.key', 'wb')
    f.write(u_pubk)
    f.close()

    u_prik = u_privkey.save_pkcs1()
    f = open(user_path + 'private_key.key', 'wb')
    f.write(u_prik)
    f.close()

    s_pubk = s_pubkey.save_pkcs1()
    f = open(server_path + 'public_key.key', 'wb')
    f.write(s_pubk)
    f.close()

    s_prik = s_privkey.save_pkcs1()
    f = open(server_path + 'private_key.key', 'wb')
    f.write(s_prik)
    f.close()


def get_user_pubkey(uid):
    user_path = keyPath + str(uid) + '/user/'
    f = open(user_path + 'public_key.key', 'rb')
    content = f.read()
    f.close()
    return content.decode('utf-8')


def get_server_pubkey(uid):
    server_path = keyPath + str(uid) + '/server/'
    f = open(server_path + 'public_key.key', 'rb')
    content = f.read()
    f.close()
    return content.decode('utf-8')


def server_decrypt(uid, fileContent):
    f = open('./userKey/' + uid + '/server/private_key.key', 'rb')
    prik = f.read()
    f.close()
    privatekey = rsa.PrivateKey.load_pkcs1(prik)
    try:
        fileContent = rsa.decrypt(fileContent, privatekey)
    except Exception as e:
        print("Error:" + str(e))
        return False
    return fileContent


def server_encrypt(uid, fileContent):
    f = open('./userKey/' + uid + '/server/public_key.key', 'rb')
    pubk = f.read()
    f.close()
    publickey = rsa.PublicKey.load_pkcs1(pubk)
    try:
        fileContent = rsa.encrypt(fileContent, publickey)
    except Exception as e:
        print("Error:" + str(e))
        return False
    return fileContent


def user_decrypt(uid, fileContent):
    f = open('./userKey/' + uid + '/user/private_key.key', 'rb')
    prik = f.read()
    f.close()
    privatekey = rsa.PrivateKey.load_pkcs1(prik)
    try:
        fileContent = rsa.decrypt(fileContent, privatekey)
    except Exception as e:
        print("Error:" + str(e))
        return False
    return fileContent


def user_encrypt(uid, fileContent):
    f = open('./userKey/' + uid + '/user/public_key.key', 'rb')
    pubk = f.read()
    f.close()
    publickey = rsa.PublicKey.load_pkcs1(pubk)
    try:
        fileContent = rsa.encrypt(fileContent, publickey)
    except Exception as e:
        print("Error:" + str(e))
        return False
    return fileContent


def aes_keygen(uid, stamp):
    # gen key encrypt
    psd = urandom(32)
    salt = urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", psd, salt, 4096, 32)
    key_e = user_encrypt(uid, key)
    # gen iv encrypt
    psd = urandom(32)
    salt = urandom(32)
    iv = hashlib.pbkdf2_hmac("sha256", psd, salt, 4096, 16)
    iv_e = user_encrypt(uid, iv)
    # save key, iv
    aes_path = keyPath + str(uid) + '/file_aes/' + stamp + '/'
    mkdir(aes_path)
    with open(aes_path + 'key.key', 'wb') as f:
        f.write(key_e)
    with open(aes_path + 'iv.key', 'wb') as f:
        f.write(iv_e)
    return key, iv


def aes_encrypt(key, iv, message):
    cipher = AES.new(key, AES.MODE_OFB, iv)
    cipher_text = cipher.encrypt(message)
    return cipher_text


def aes_decrypt(key, iv, message):
    try:
        decipher = AES.new(key, AES.MODE_OFB, iv)
        re = decipher.decrypt(message)
        return unpad(re, 16)
    except Exception as e:
        print("Error:" + str(e))
        return False


# print(aes_keygen()[0])
# key, iv = aes_keygen()
# print(key, iv)
# print(key.hex(), iv.hex())
# cipher = AES.new(key, AES.MODE_OFB, iv)
# message = b'aaabbbccc'
# c = cipher.encrypt(message)
# print(c)
# decipher = AES.new(key, AES.MODE_OFB, iv)
# m = decipher.decrypt(c)
# print(m)





from os import path, mkdir
import rsa
from cryptography.hazmat.bindings import openssl


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

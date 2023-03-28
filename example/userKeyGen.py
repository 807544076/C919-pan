from os import path, mkdir
import rsa
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad
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


def server_decrypt(email, fileContent):
    db = C919SQL()
    db.search_link()
    userUUID = str(db.selectUserUID(email)[0])
    db.end_link()
    f = open('./userKey/' + userUUID + '/server/private_key.key', 'rb')
    prik = f.read()
    f.close()
    privatekey = rsa.PrivateKey.load_pkcs1(prik)
    try:
        fileContent = rsa.decrypt(fileContent, privatekey)
    except:
        return False
    return fileContent


def aes_decrypt(key, iv, message):
    try:
        decipher = AES.new(key, AES.MODE_OFB, iv)
        re = decipher.decrypt(message)
        return unpad(re, 16)
    except Exception as e:
        print(str(e))
        return False


# key = get_random_bytes(32)
# iv = get_random_bytes(16)
# print()
# cipher = AES.new(key, AES.MODE_OFB, iv)
# message = b'aassddffgghhjjkkllmmnnbbvvccxxzzqqwweerrttyyuuiioopp'
# c = cipher.encrypt(message)
# print(c)
# decipher = AES.new(key, AES.MODE_OFB, iv)
# m = decipher.decrypt(c)
# print(m)





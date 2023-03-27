from os import path, mkdir
from hashlib import sha256

import rsa

from linksql import C919SQL
from nacl.public import SealedBox

tempDir = './temp/'
fileStorage = './fileStorage/'


def dirCheck(email):  # 为每个用户生成相应的文件夹
    if not path.exists(tempDir):
        mkdir(tempDir)
    if not path.exists(fileStorage):
        mkdir(fileStorage)
    db = C919SQL()
    db.search_link()
    userUUID = str(db.selectUserUID(email)[0])
    db.end_link()
    if not path.exists(fileStorage + userUUID):
        mkdir(fileStorage + userUUID)
    return fileStorage + userUUID


def fileExist(newFileHash):  # hash相同即可快速上传
    db = C919SQL()
    db.search_link()
    allHashRecord = db.selectAllFileHash()
    flag = False
    for item in allHashRecord:
        print(item[0])
        if item[0] == newFileHash:
            flag = True
            break
    if flag:
        db.end_link()
        return True
    else:
        db.end_link()
        return False


def upload(email, fileContent, nameString):
    db = C919SQL()
    db.admin_link()
    userDir = dirCheck(email)  # 存储位置
    fileSize = len(fileContent)  # 文件大小
    assert fileSize <= 1024 * 1024 * 10, '文件过大,超过10MB限制'
    userUUID = str(db.selectUserUID(email)[0])
    f = open('./userKey/' + userUUID + '/server/private_key.key', 'rb')
    prik = f.read()
    f.close()
    privatekey = rsa.PrivateKey.load_pkcs1(prik)
    try:
        fileContent = rsa.decrypt(fileContent, privatekey)
        print(fileContent)
    except:
        return 'decrypt failed'
    fileHash = sha256(fileContent).hexdigest()  # 文件内容hash
    if fileExist(fileHash):  # 快速上传（拷贝记录）
        print('fast upload')
        db.upload_file(nameString, userUUID, fileHash, str(fileSize))
        db.end_link()
    else:
        # userPasswordHash = db.selectUserPasswordHash(email)
        print(nameString, userUUID, fileHash, fileSize)
        db.upload_file(nameString, userUUID, fileHash, str(fileSize))
        db.end_link()
        # fileContentEncrypted=SealedBox(userPasswordHash).encrypt(fileContent)
        with open(userDir + '/' + nameString + fileHash, 'wb') as f:
            f.write(fileContent)
    return 'success'

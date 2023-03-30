from os import path, mkdir
from hashlib import sha256
import random
from userKeyGen import aes_encrypt, aes_keygen
from linksql import C919SQL

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


def genstamp():
    stamp = ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
         'e', 'd', 'c', 'b', 'a', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 20))
    return stamp


def gen_check_stamp():
    db = C919SQL()
    db.search_link()
    stamp = genstamp()
    stamps = db.select_all_stamp()
    db.end_link()
    flag = True
    while flag and stamps:
        for st in stamps:
            if st[0] == stamp:
                stamp = genstamp()
                break
            else:
                flag = False
    return stamp


def upload(email, fileContent, nameString):
    db = C919SQL()
    db.admin_link()
    userDir = dirCheck(email)  # 存储位置
    fileSize = len(fileContent)  # 文件大小
    assert fileSize <= 1024 * 1024 * 10, '文件过大,超过10MB限制'
    userUUID = str(db.selectUserUID(email)[0])
    fileHash = sha256(fileContent).hexdigest()  # 文件内容hash
    if fileExist(fileHash):  # 快速上传（拷贝记录）
        print('fast upload')
        # db.upload_file(nameString, userUUID, fileHash, str(fileSize))
    else:
        stamp = gen_check_stamp()  # 为每个文件生成独特的stamp
        print(nameString, userUUID, fileHash, fileSize, stamp)
        db.upload_file(nameString, userUUID, fileHash, str(fileSize), stamp)
        key, iv = aes_keygen(userUUID, stamp)  # 生成文件对应的aes密钥
        en_file_content = aes_encrypt(key, iv, fileContent)  # 对文件内容进行加密
        with open(userDir + '/' + nameString + fileHash, 'wb') as f:    # 保存加密的文件
            f.write(en_file_content)
    db.end_link()
    return 'success'

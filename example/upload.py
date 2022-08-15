from os import path,mkdir
from hashlib import md5
from linksql import C919SQL
import nacl

fileStorage='./fileStorage/'
fileTypeWhiteList=['jpg','png','gif','jpeg','bmp','doc','docx','xls','xlsx','ppt','pptx']

def dirCheck(email):
    if not path.exists(fileStorage):
        mkdir(fileStorage)
    db=C919SQL()
    db.search_link()
    userUUID=db.selectUserUUID(email)
    db.end_link()
    if not path.exists(fileStorage+userUUID):
        mkdir(fileStorage+userUUID)
    return fileStorage+userUUID

def fileExist(newFileHash):
    db=C919SQL()
    db.search_link()
    allHashRecord=db.selectAllFileHash()
    flag=False
    for item in allHashRecord:
        if item==newFileHash:
            flag=True
            break
    if flag:
        db.end_link()
        return True
    else:
        db.end_link()
        return False

def upload(email,file):
    userDir=dirCheck(email)
    fileName=path.splitext(file)[0]
    fileExtension=path.splitext(file)[1][1:]
    assert fileExtension in fileTypeWhiteList,'不允许的文件类型'
    assert len(fileName)<=45,'文件名过长,超过45个字符'
    fileContent=open(file,'rb').read()
    fileSize=len(fileContent)
    assert fileSize<=1024*1024*10,'文件过大,超过10MB限制'
    fileHash=md5(fileContent).hexdigest()
    if fileExist(fileName,fileHash):
        db=C919SQL()
        db.admin_link()
        userUUID=db.selectUserUUID(email)
        db.upload_file(fileName,userUUID,fileHash,fileSize)
        db.end_link()
    else:
        db=C919SQL()
        db.admin_link()
        userUUID=db.selectUserUUID(email)
        userPasswordHash=db.selectUserPasswordHash(email)
        db.upload_file(fileName,userUUID,fileHash,fileSize)
        db.end_link()
        fileContentEncrypted=nacl.public.SealedBox(userPasswordHash).encrypt(fileContent)
        with open(userDir+'/'+fileName,'wb') as f:
            f.write(fileContentEncrypted)
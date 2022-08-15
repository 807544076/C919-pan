from os import path,mkdir
from hashlib import md5
from linksql import C919SQL
from nacl.public import SealedBox

tempDir='./temp/'
fileStorage='./fileStorage/'
fileTypeWhiteList=['jpg','png','gif','jpeg','bmp','doc','docx','xls','xlsx','ppt','pptx']

def dirCheck(email):
    if not path.exists(tempDir):
        mkdir(tempDir)
    if not path.exists(fileStorage):
        mkdir(fileStorage)
    db=C919SQL()
    db.search_link()
    userUUID=str(db.selectUserUID(email)[0])
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

def upload(email,file,nameString):
    userDir=dirCheck(email)
    fileName=path.splitext(nameString)[0]
    fileExtension=path.splitext(nameString)[1][1:]
    assert fileExtension not in fileTypeWhiteList,'不允许的文件类型'
    assert len(fileName)<=45,'文件名过长,超过45个字符'
    fileContent=file.read()
    fileSize=len(fileContent)
    assert fileSize<=1024*1024*10,'文件过大,超过10MB限制'
    fileHash=md5(fileContent).hexdigest()
    if fileExist(fileHash):
        db=C919SQL()
        db.admin_link()
        userUUID=str(db.selectUserUID(email)[0])
        db.upload_file(nameString, userUUID, fileHash, str(fileSize))
        db.end_link()
    else:
        db=C919SQL()
        db.admin_link()
        userUUID=str(db.selectUserUID(email)[0])
        userPasswordHash=db.selectUserPasswordHash(email)
        print(nameString, userUUID, fileHash, fileSize)
        db.upload_file(fileName, userUUID, fileHash, str(fileSize))
        db.end_link()
        # fileContentEncrypted=SealedBox(userPasswordHash).encrypt(fileContent)
        with open(userDir+'/'+fileName+fileHash,'wb') as f:
            f.write(fileContent)
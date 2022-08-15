import pymysql


class C919SQL:
    def __init__(self):
        self.__cursor = None
        self.__db = None
        self.islink = False

    def admin_link(self):
        if self.islink:
            print('already linked')
        else:
            self.__db = pymysql.connect(host='localhost',
                         user = 'c919',
                         password = 'c919',
                         database = 'c919db')   # 账号密码仅做参考
            self.__cursor = self.__db.cursor()
            print('success')
            self.islink = True

    def execute(self, sql):
        if not self.islink:
            print('error! not linked yet')
        else:
            self.__cursor.execute(sql)
            data = self.__cursor.fetchall()
            print('execute successfully')
            return data

    def end_link(self):
        if not self.islink:
            print('error! not linked yet')
        else:
            self.__db.close()
            self.__cursor = None
            self.__db = None
            self.islink = False;
            print('close')

    def search_link(self):
        if self.islink:
            print('already linked')
        else:
            self.__db = pymysql.connect(host='localhost',
                         user = 'c919select',
                         password = 'c919select',
                         database = 'c919db')   # 账号密码仅做参考
            self.__cursor = self.__db.cursor()
            print('success')
            self.islink = True

    def userCreate(self, username, email, password):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = 'insert into user_info(name,email,password) values("%s","%s","%s")' % (username,email,password)
            self.__cursor.execute(sql)
            self.__db.commit()
            print('create successfully')

    def root_link(self, root, password):
        if self.islink:
            print('already linked')
        else:
            self.__db = pymysql.connect(host='localhost',
                                        user=root,
                                        password=password)  # 账号密码仅做参考
            self.__cursor = self.__db.cursor()
            print('success')
            self.islink = True

    def select_email(self, email):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select email from user_info where email = '" + email + "'"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
            if result:
                return True
            else:
                return False

    def select_password(self, password):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select email from user_info where password = '" + password + "'"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
            if result:
                return True
            else:
                return False

    def select_username(self, email):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select name from user_info where email = '" + email + "'"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
            return result

    def upload_file(self, filename, owner_uid, filehash):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "insert into file_info(filename, owner_uid, filehash) values(%s %s %s)" % (filename, owner_uid, filehash)
            self.__cursor.execute(sql)
            self.__db.commit()
            print('create successfully')

    def delete_file(self, file_id):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "delete from file_info where id = '" + file_id + "';"
            self.__cursor.execute(sql)
            print('delete successfully')

    def select_file_id(self, filename, owner_uid):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select id from file_info where filename = '" + filename + "' and owner_uid = " + owner_uid + ";"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
            return result

    def set_shared(self, file_id, status):
        if not self.islink:
            print('error! not linked yet')
        else:
            if status:
                sql = "update file_info set isshared = true where id = " + file_id + ";"
            else:
                sql = "update file_info set isshared = false where id = " + file_id + ";"
            self.__cursor.execute(sql)
            print('change successfully')

    def set_check(self, uid, status):
        if not self.islink:
            print('error! not linked yet')
        else:
            if status:
                sql = "update user_info set ischeck = true where uid = " + uid + ";"
            else:
                sql = "update user_info set ischeck = false where uid = " + uid + ";"
            self.__cursor.execute(sql)
            print('change successfully')

    def set_frozen(self, uid, status):
        if not self.islink:
            print('error! not linked yet')
        else:
            if status:
                sql = "update user_info set isfrozen = true where uid = " + uid + ";"
            else:
                sql = "update user_info set isfrozen = false where uid = " + uid + ";"
            self.__cursor.execute(sql)
            print('change successfully')

    def selectUserUUID(self, email):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select uuid from user_info where email = " + email + ";"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
            return result
    
    def selectFileHash(self,filename):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select filehash from file_info where filename = " + filename + ";"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
            return result
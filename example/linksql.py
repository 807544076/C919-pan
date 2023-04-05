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
                                        user='c919',
                                        password='c919',
                                        database='c919db')  # 账号密码仅做参考
            self.__cursor = self.__db.cursor()
            print('admin connected successfully')
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
            print('link closed')

    def search_link(self):
        if self.islink:
            print('already linked')
        else:
            self.__db = pymysql.connect(host='localhost',
                                        user='c919select',
                                        password='c919select',
                                        database='c919db')  # 账号密码仅做参考
            self.__cursor = self.__db.cursor()
            print('search connected successfully')
            self.islink = True

    def userCreate(self, username, email, password):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = 'insert into user_info(name,email,password) values("%s","%s","%s")' % (username, email, password)
            self.__cursor.execute(sql)
            self.__db.commit()
            print('user created successfully')

    def root_link(self, root, password):
        if self.islink:
            print('already linked')
        else:
            self.__db = pymysql.connect(host='localhost',
                                        user=root,
                                        password=password)  # 账号密码仅做参考
            self.__cursor = self.__db.cursor()
            print('root connected successfully')
            self.islink = True

    def check_email(self, email):
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

    def check_password(self, email, password):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select * from user_info where password = '" + password + "' and email = '" + email + "'"
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

    def upload_file(self, filename, owner_uid, filehash, filesize, stamp):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "insert into file_info(filename, owner_uid, filehash, filesize, stamp) values('" + filename + "', " + owner_uid + ", '" + filehash + "', " + filesize + ", '" + stamp + "');"
            self.__cursor.execute(sql)
            self.__db.commit()
            print('upload file created successfully')

    def delete_file(self, stamp):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "delete from file_info where stamp = '" + stamp + "';"
            self.__cursor.execute(sql)
            self.__db.commit()
            print('file deleted successfully')

    def select_file_id(self, filename, owner_uid):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select id from file_info where filename = '" + filename + "' and owner_uid = " + owner_uid + ";"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
            return result

    def set_shared(self, stamp, status):
        if not self.islink:
            print('error! not linked yet')
        else:
            if status:
                sql = "update file_info set isshared = true where stamp = '" + stamp + "';"
            else:
                sql = "update file_info set isshared = false where stamp = '" + stamp + "';"
            self.__cursor.execute(sql)
            self.__db.commit()
            print('sharing changed successfully')

    def set_check(self, uid, status):
        if not self.islink:
            print('error! not linked yet')
        else:
            if status:
                sql = "update user_info set ischeck = true where uid = " + uid + ";"
            else:
                sql = "update user_info set ischeck = false where uid = " + uid + ";"
            self.__cursor.execute(sql)
            self.__db.commit()
            print('checking changed successfully')

    def set_frozen(self, uid, status):
        if not self.islink:
            print('error! not linked yet')
        else:
            if status:
                sql = "update user_info set isfrozen = true where uid = " + uid + ";"
            else:
                sql = "update user_info set isfrozen = false where uid = " + uid + ";"
            self.__cursor.execute(sql)
            self.__db.commit()
            print('frozen changed successfully')

    def selectUserUID(self, email):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select uid from user_info where email = '" + email + "';"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
            return result

    def selectFileHash(self, filename):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select filehash from file_info where filename = '" + filename + "';"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
            return result

    def selectAllFileHash(self):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select filehash from file_info;"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
            return result

    def selectUserPasswordHash(self, email):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select password from user_info where email = '" + email + "';"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
            return result

    def reset_passwd(self, email, password):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "update user_info set password = '" + password + "' where email ='" + email + "';"
            self.__cursor.execute(sql)
            self.__db.commit()
            print('password changed successfully')
            return True

    def select_all_stamp(self):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select stamp from file_info;"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
            return result

    def select_all_file(self, uid):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select filename, upload_date, filesize, stamp, isshared from file_info where owner_uid = " + str(uid) + ";"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
            return result

    def select_file_stamp(self, stamp):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select * from file_info where stamp = '" + stamp + "';"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
            return result

    def select_username_by_uid(self, uid):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select name from user_info where uid = " + str(uid) + ";"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
            return result

    def set_authorization_code(self, stamp, code):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "update file_info set authorization_code = '" + code + "' where stamp ='" + stamp + "';"
            self.__cursor.execute(sql)
            self.__db.commit()
            return True

    def select_file_owner(self, stamp):
        if not self.islink:
            print('error! not linked yet')
        else:
            sql = "select owner_id from file_info where stamp = '" + stamp + "';"
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
            return result

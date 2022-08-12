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

    def userCreate(self, username,email,password):
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


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
            data = self.__cursor.fetchone()
            print('execute successfully')
            return data

    def end_link(self):
        if not self.islink():
            print('error! not linked yet')
        else:
            self.__db.close()
            self.__cursor = None
            self.__db = None
            print('close')

    def search_link(self):
        pass

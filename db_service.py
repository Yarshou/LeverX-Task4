from mysql.connector import connection, Error
from file_loader import JSONLoad
import mysql.connector


class DBService(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(DBService, cls).__new__(cls)
        return cls.instance

    def __init__(self, settings):
        self.__cnx = connection.MySQLConnection()
        self.settings = settings

    def connect(self):
        self.__cnx = connection.MySQLConnection(
            host=self.settings['host'],
            user=self.settings['username'],
            password=self.settings['password'],
            database=self.settings['database'],
        )

    def connect_or_create(self):
        try:
            return self.connect()
        except mysql.connector.errors.ProgrammingError:
            self.__init_db__()
            self.connect()

    def init_table(self, query, data=None):
        cursor = self.__cnx.cursor()
        try:
            cursor.execute(f'USE `{self.settings["database"]}`;')
            cursor.execute(query, data)
        except Error as err:
            return None
        finally:
            cursor.close()
            self.connect()
        return None

    def __init_db__(self):
        self.__cnx = mysql.connector.connect(
            host=self.settings['host'],
            user=self.settings['username'],
            password=self.settings['password']
        )

        cursor = self.__cnx.cursor()
        cursor.execute(f"CREATE DATABASE `{self.settings['database']}`;")

    def update_query(self, query, data=None):
        cursor = self.__cnx.cursor()
        try:
            cursor.execute(query, data)
        except Error as err:
            if err.errno == 1062:
                return None
            elif err.errno == 1061:
                print(f'{err.errno}, index already exists')
                return None
            else:
                print("UNEXPECTED ERROR")
                return None
        finally:
            cursor.close()
        return None

    def execute_query(self, query, data=None):
        cursor = self.__cnx.cursor(dictionary=True)
        try:
            cursor.execute(query, data)
            result = cursor.fetchall()
        except Error:
            return None
        finally:
            cursor.close()
        return result

    def fullfill(self, filepath, table_name):

        loader = JSONLoad()
        data = loader.load(filepath)
        keys = data[0].keys()
        query = f"INSERT INTO {table_name}("
        for entry in data:
            for key in keys:
                query += f"{key},"
            query = query[:-1] + ")VALUES("
            for key in keys:
                query += f"'{entry[key]}',"
            query = query[:-1] + ");"
            self.update_query(query)
            self.__cnx.commit()
            query = f"INSERT INTO {table_name}("

    def close_connection(self):
        self.__cnx.close()

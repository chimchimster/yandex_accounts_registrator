from logs.conf import Logger
from mysql.connector import Connect


log = Logger()
log.configurate()


class DataBase:
    """ Connects to MySQL MariaDB """

    def __init__(self, db_name: str, host: str, user: str, password: str) -> None:
        self.db_name = db_name
        self.host = host
        self.user = user
        self.password = password
        try:
            self.connection = Connect(host=self.host, user=self.user, password=self.password)
        except Exception as e:
            log.logger.warning(e)

    def insert_into_yandex_tokens_table(self, table_name: str, collection: list) -> None:
        cursor = self.connection.cursor()

        try:
            cursor.execute(f'USE {self.db_name}')
            cursor.execute(f'INSERT INTO {table_name} (work, space_used, first_name, last_name, username, password, phone, token) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', collection)
            self.connection.commit()
        except Exception as e:
            log.logger.warning(e)

    def get_proxies(self, table_name: str, script: str = 'insta_story') -> tuple:
        cursor = self.connection.cursor()

        try:
            cursor.execute(f'USE {self.db_name}')
            cursor.execute(f'SELECT proxy, port, login, password FROM {table_name} WHERE script = "{script}" ORDER BY RAND() LIMIT 1')
        except Exception as e:
            log.logger.warning(e)

        return cursor.fetchone()

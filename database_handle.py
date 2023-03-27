import settings
from mysql.connector import Connect


class DataBase:
    """ Connects to MySQL MariaDB """

    def __init__(self, db_name: str, host: str, user: str, password: str) -> None:
        self.db_name = db_name
        self.host = host
        self.user = user
        self.password = password
        self.connection = Connect(host=self.host, user=self.user, password=self.password)

    def insert_into_yandex_tokens_table(self, table_name: str, collection: list) -> None:
        cursor = self.connection.cursor()

        cursor.execute(f'USE {self.db_name}')
        cursor.execute(f'INSERT INTO {table_name} (work, space_used, first_name, last_name, username, password, phone, token) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', collection)
        self.connection.commit()

    def get_proxies(self, table_name: str, script: str = 'insta_story') -> tuple:
        cursor = self.connection.cursor()

        cursor.execute(f'USE {self.db_name}')
        cursor.execute(f'SELECT proxy, port, login, password FROM {table_name} WHERE script = "{script}" ORDER BY RAND() LIMIT 1')

        return cursor.fetchone()


# db = DataBase('social_services', settings.social_services_db['host'], settings.social_services_db['user'], settings.social_services_db['password'])
#
# db.insert_into_yandex_tokens_table('yandex_tokens', [1, 4900, 'Melissa', 'Copeland', 'melissa.copeland.9180.DZuc', '#3tFvBoC%2', '+77783586934', 'y0_AgAAAABpj_AXAADLWwAAAADfgME8RuZEWUvlQ4WJVdlOcgSU-kDwuOA'])
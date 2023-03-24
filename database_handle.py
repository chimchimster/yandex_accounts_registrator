from mysql.connector import Connect


class DataBase:
    def __init__(self, db_name: str, host: str, user: str, password: str) -> None:
        self.db_name = db_name
        self.host = host
        self.user = user
        self.password = password
        self.connection = Connect(self.host, self.user, self.password)

    def insert_into_yandex_tokens_table(self, table_name: str, collection: list) -> None:
        cursor = self.connection.cursor()

        cursor.execute(f'USE {self.db_name}')
        cursor.execute(f'INSERT INTO {table_name} (first_name, last_name, username, password, phone, token) VALUES (%s,%s,%s,%s,%s,%s)', collection)


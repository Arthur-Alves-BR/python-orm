import psycopg


class Database:

    def __init__(self) -> None:
        self._connection = None

    def connect(self, database: str, user: str, password: str, host: str, port: int = 5432) -> None:
        if not self._connection:
            self._connection = psycopg.connect(
                password=password,
                autocommit=True,
                dbname=database,
                user=user,
                host=host,
                port=port,
            )

    def execute(self, command: str) -> psycopg.cursor.Cursor:
        return self._connection.execute(command)

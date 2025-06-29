import os

import psycopg2
from dotenv import load_dotenv
load_dotenv(override=True)


def create_database_and_tables(dbname, user, password, host="localhost", port="5432"):
    """Функция для создания базы данных"""

    connection = psycopg2.connect(user=user, password=password, host=host, port=port)

    connection.autocommit = True  # Включаем автокоммит для создания базы данных
    cursor = connection.cursor()

    # Создание базы данных
    try:
        cursor.execute(f"CREATE DATABASE {dbname};")
        print(f"База данных '{dbname}' создана.")
    except psycopg2.Error as e:
        print(f"Ошибка создания базы данных: {e}")
    finally:
        cursor.close()
        connection.close()  # Закрываем соединение для создания базы данных

    # Подключение к только что созданной базе данных для создания таблиц
    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    cursor = connection.cursor()

    # Создание таблицы для организаций
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT NULL
)
    """
    )

    # Создание таблицы для вакансий
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Vacancy (
            id SERIAL PRIMARY KEY UNIQUE,
            name VARCHAR(100) NOT NULL,
            url TEXT NULL UNIQUE,
            salary INTEGER NULL,
            company_id INTEGER REFERENCES Company(id) ON DELETE CASCADE
        )
    """
    )

    connection.commit()  # Сохранение изменений в структуре базы данных

    cursor.close()
    connection.close()
    print("Все таблицы успешно созданы.")


if __name__ == "__main__":
    DB_NAME = os.getenv('DB_NAME')
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')

    # Создание базы данных и таблиц
    create_database_and_tables(DB_NAME, USER, PASSWORD)

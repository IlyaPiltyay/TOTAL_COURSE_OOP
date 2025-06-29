import os
from typing import List, Tuple, Any

import psycopg2
from dotenv import load_dotenv

from src.headHunterAPI import HeadHunterAPI
from src.vacancy import Vacancy
load_dotenv(override=True)


class DBManager:
    def __init__(self, dbname: str, user: str, password: str, host: str = "localhost", port: str = "5432"):
        self.connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self) -> Any:
        query = """
            SELECT c.name AS company_name, COUNT(v.id) AS vacancies_count
            FROM Company c
            LEFT JOIN Vacancy v ON c.id = v.company_id
            GROUP BY c.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self) -> Any:
        query = """
            SELECT v.name, v.salary, c.name
            FROM Vacancy v
            JOIN Company c ON v.company_id = c.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self) -> Any:
        query = """
            SELECT AVG(salary) AS avg_salary
            FROM Vacancy
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> Any:
        """Вакансии с ЗП выше среднего"""
        avg_salary = self.get_avg_salary()
        query = """
            SELECT v.name, v.salary, c.name
            FROM Vacancy v
            JOIN Company c ON v.company_id = c.id
            WHERE v.salary > %s
        """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_by_keywords(self, keywords: str) -> Any:
        """Поиск вакансий по ключевым словам"""
        query_parts = ["name ILIKE %s"] * len(keywords)
        query = "SELECT * FROM Vacancy WHERE " + " OR ".join(query_parts)

        params = [f"%{keyword}%" for keyword in keywords]

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def insert_company(self, company_name: str) -> Any:
        """Добавление данных в таблицу Компаний"""
        query = """
        INSERT INTO Company (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id
        """
        self.cursor.execute(query, (company_name,))
        company_id = self.cursor.fetchone()

        if company_id:
            return company_id[0]
        else:
            self.cursor.execute("SELECT id FROM Company WHERE name = %s", (company_name,))
            existing_company = self.cursor.fetchone()
            return existing_company[0] if existing_company else None

    def insert_vacancy(self, vacancy: Vacancy) -> Any:
        """Добавление данных в таблицу Вакансий"""
        company_id = self.insert_company(vacancy.company)

        name = vacancy.name
        salary = vacancy.salary
        url = vacancy.url
        query = """
                INSERT INTO Vacancy (name, salary, url, company_id)  
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING
                """

        self.cursor.execute(query, (name, salary, url, company_id))
        self.connection.commit()

    def close(self) -> None:
        """Закрытие конекотора и ккурсора"""
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    DB_NAME = os.getenv('DB_NAME')
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')
    db_manager = DBManager(dbname=DB_NAME, user=USER, password=PASSWORD)

    try:
        print("Companies and vacancies count:")
        companies_count = db_manager.get_companies_and_vacancies_count()
        for company_name, count in companies_count:
            print(f"Компания: {company_name}, Вакансий: {count}")

        print("\nAll vacancies:")
        vacancies = db_manager.get_all_vacancies()
        for name, salary, company_name in vacancies:
            print(f"Вакансия: {name}, Зарплата: {salary}, Компания: {company_name}")

        avg_salary = db_manager.get_avg_salary()
        print(f"\nAverage salary: {avg_salary}")

        print("\nVacancies with higher salary than average:")
        higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
        for name, salary, company_name in higher_salary_vacancies:
            print(f"Вакансия: {name}, Зарплата: {salary}, Компания: {company_name}")

        keyword_input = input("Введите слово для поиска")
        print(f"\nVacancies with keyword '{keyword_input}':")
        keyword_vacancies = db_manager.get_vacancies_by_keywords(keyword_input)
        hh_api = HeadHunterAPI()
        vacancies = hh_api.get_vacancies("Phyton")
        for i in vacancies:
            x = Vacancy(i["id"], i["name"], i["salary"], i["url"], i["snippet"]["requirement"], i["employer"]["name"])
            db_manager.insert_vacancy(x)

        for vacancy in keyword_vacancies:
            print(vacancy)
    finally:
        db_manager.close()

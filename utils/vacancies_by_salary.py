import json
from typing import Any


def get_top_vacancies_by_salary(file_handler: Any) -> None:

    count_vacancy = int(input("Введите количество вакансий для получения по зарплате: "))

    with open(r"C:\Уроки\TCOURSE_OOP\data\vacancy.json", "r", encoding="utf-8") as file:
        vacancies_data = json.load(file)

        vacancies_with_salary = []

        for vacancy in vacancies_data:
            salary = vacancy.get("salary")
            salary_from = salary.get("from", salary) if isinstance(salary, dict) else salary

            if isinstance(salary_from, (int, float)) and salary_from >= 0:
                vacancy["salary_from"] = salary_from
                vacancies_with_salary.append(vacancy)

        top_vacancies = sorted(vacancies_with_salary, key=lambda x: x["salary_from"], reverse=True)[:count_vacancy]

        for vacancy in top_vacancies:
            print(f'{vacancy["id"]} {vacancy["name"]} Зарплата: {vacancy["salary"]} {vacancy["url"]}')

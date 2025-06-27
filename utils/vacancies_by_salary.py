import json
from typing import Any

from src.vacancy import Vacancy


def get_top_vacancies_by_salary(file_handler: Any) -> None:
    count_vacancy = int(input("Введите количество вакансий для получения по зарплате: "))

    with open(r"data/vacancy.json", "r", encoding="utf-8") as file:
        # загружаем словари из файла
        vacancies_data = json.load(file)

    vacancies = []
    for d in vacancies_data:
        vacancy = Vacancy(**d)
        vacancies.append(vacancy)

    top_vacancies = sorted(vacancies, reverse=True)[:count_vacancy]

    for vacancy in top_vacancies:
        print(vacancy)

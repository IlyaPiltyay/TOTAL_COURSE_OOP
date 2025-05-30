from abc import ABC, abstractmethod

import requests


class Base_API(ABC):
    """Базовый абстрактный класс для работы с API"""

    @abstractmethod
    def __init__(self):
        """Инициализация объекта"""
        pass

    @abstractmethod
    def _connect(self, keyword):
        """Внутренний метод подключения и получения данных"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword):
        """Получение списка вакансий"""
        pass


class HeadHunterAPI(Base_API):
    """Класс реализует получение вакансий с hh.ru через API"""

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": 100}
        self.vacancies = []

    def _connect(self, keyword):
        """Метод для подключения к API"""
        self.params["text"] = keyword
        self.params["page"] = 0
        self.vacancies = []
        while self.params["page"] < 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            if response.status_code != 200:
                raise ValueError(f"Ошибка запроса: {response.status_code}")
            data = response.json()
            items = data.get("items", [])
            if not items:
                break
            self.vacancies.extend(items)
            self.params["page"] += 1

    def get_vacancies(self, keyword):
        """Метод для получения вакансий"""
        self._connect(keyword)
        return [
            {
                "name": i["name"],
                "company": i["employer"]["name"],
                "url": i["alternate_url"],
                "salary": i.get("salary"),
                "id": i.get("id"),
            }
            for i in self.vacancies
        ]


if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    try:
        hh_vacancies = hh_api.get_vacancies("Python")
        for vacancy in hh_vacancies:
            salary = vacancy["salary"]
            if salary and salary["from"] is not None and salary["to"] is not None:
                average_salary = salary["from"] + (salary["to"] - salary["from"]) / 2
            elif salary and salary["from"] is not None:
                average_salary = salary["from"]
            elif salary and salary["to"] is not None:
                average_salary = salary["to"]
            else:
                average_salary = "Не указана"

            print(
                f"Название вакансии: {vacancy['name']}, Работодатель: {vacancy['company']}, "
                f"Ссылка: {vacancy['url']}, Средняя зарплата: {average_salary}, id: {vacancy['id']}"
            )
    except Exception as e:
        print(f"Произошла ошибка: {e}")

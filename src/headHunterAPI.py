from abc import ABC, abstractmethod

import requests


class Base_API(ABC):
    """Базовый абстрактный класс для работы с API"""

    @abstractmethod
    def __init__(self) -> None:
        """Инициализация объекта"""
        pass

    @abstractmethod
    def _connect(self, keyword: str) -> None:
        """Внутренний метод подключения и получения данных"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> list:
        """Получение списка вакансий"""
        pass


class HeadHunterAPI(Base_API):
    """Класс реализует получение вакансий с hh.ru через API"""

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": 100}
        self.vacancies = []

    def _connect(self, keyword: str) -> None:
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

    def get_vacancies(self, keyword: str) -> list:
        """Метод для получения вакансий"""
        self._connect(keyword)
        return self.vacancies


if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies("Продавец")
    for i in hh_vacancies:
        print(i["employer"]["name"])

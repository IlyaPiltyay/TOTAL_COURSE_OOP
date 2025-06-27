from typing import Dict, Union

from src.headHunterAPI import HeadHunterAPI


class Vacancy:
    __slots__ = ("id", "_name", "_salary", "_url", "snippet", "_company")

    def __init__(self, id: int, name: str, salary: Union[int, float], url: str, snippet: str, company: str) -> None:
        self.id = id
        self._name = self.__validate_name(name)
        self._salary = self.__validate_salary(salary)
        self._url = self.__validate_url(url)
        self.snippet = snippet
        self._company = company

    @property
    def name(self) -> str:
        return self._name

    @property
    def salary(self) -> Union[int, float]:
        return self._salary

    @property
    def url(self) -> str:
        return self._url

    @property
    def company(self) -> str:
        return self._company

    def __validate_name(self, name: str) -> str:
        """Метод для валидации названия вакансии"""
        if not isinstance(name, str) or not name:
            return "Название вакансии не указано"
        return name

    def __validate_salary(self, salary: Union[int, float, Dict[str, Union[int, float]]]) -> Union[int, float]:
        """Метод для валидации суммы заработной платы"""

        if salary is None:
            return 0
        if isinstance(salary, dict):
            salary_from = salary.get("from")
            salary_to = salary.get("to")
            if salary_from is not None and salary_from > 0:
                return salary_from
            elif salary_to is not None and salary_to > 0:
                return salary_to
        if isinstance(salary, (int, float)) and salary >= 0:
            return salary

        return 0

    def __validate_url(self, url: str) -> str:
        """Метод для валидации ссылки на вакансию"""
        if not isinstance(url, str) or not url.startswith("http"):
            return "Ссылка не указана"
        return url

    def to_dict(self) -> dict:
        """Метод для приобразования в словарь"""
        return {
            "id": self.id,
            "name": self.name,
            "salary": self.salary,
            "url": self.url,
            "snippet": self.snippet,
            "company": self.company,
        }

    def __lt__(self, other: "Vacancy") -> bool:
        """Сравнеие <"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary

    def __le__(self, other: "Vacancy") -> bool:
        """Сравнеие <="""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary <= other.salary

    def __eq__(self, other: object) -> bool:
        """Сравнеие =="""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary

    def __ne__(self, other: object) -> bool:
        """Сравнеие !="""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary != other.salary

    def __gt__(self, other: "Vacancy") -> bool:
        """Сравнеие >"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary > other.salary

    def __ge__(self, other: "Vacancy") -> bool:
        """Сравнеие >="""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary >= other.salary

    def __repr__(self) -> str:
        """Вывод для отладки"""
        return f"Vacancy(name='{self.name}', salary={self.salary}, url='{self.url}' , snippet= {self.snippet})"

    def __str__(self) -> str:
        """Вывод для строки"""
        return f"ID: {self.id}\nНаименование: {self.name}\nЗарплата: {self.salary}\nСсылка: {self.url}\nТребования: \n{self.snippet}\nКомпания: {self.company}"


if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("Phyton")
    for i in vacancies:
        x = Vacancy(i["id"], i["name"], i["salary"], i["url"], i["snippet"]["requirement"], i["employer"]["name"])
        print(x, sep="\n")

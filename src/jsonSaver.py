import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from src.headHunterAPI import HeadHunterAPI
from src.vacancy import Vacancy


class FileHandler(ABC):
    def __init__(self, filename: str) -> None:
        self.__filename = filename  # Приватный атрибут для хранения имени файла

    @property
    def filename(self) -> str:
        """Свойство для доступа к имени файла."""
        return self.__filename

    @abstractmethod
    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: Union[int, str]) -> None:
        pass


class JSONFileHandler(FileHandler):
    def __init__(self, filename: str = r"C:\Уроки\TCOURSE_OOP\data\vacancy.json") -> None:
        super().__init__(filename)  # Вызов конструктора родительского класса

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Метод для добавления вакансии в файл."""
        vacancies = self.get_vacancies()
        if vacancy not in vacancies:
            vacancies.append(vacancy)
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=4)

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Метод для получения вакансий по указанным критериям."""
        if not os.path.exists(self.filename):
            return []

        with open(self.filename, "r", encoding="utf-8") as f:
            try:
                vacancies = json.load(f)
            except json.JSONDecodeError:
                return []

        if criteria:
            filtered_vacancies = [
                vacancy for vacancy in vacancies if all(vacancy.get(key) == value for key, value in criteria.items())
            ]
            return filtered_vacancies
        return vacancies

    def delete_vacancy(self, vacancy_id: Union[int, str]) -> None:
        """Метод для удаления вакансии."""
        vacancies = self.get_vacancies()
        vacancies = [vacancy for vacancy in vacancies if str(vacancy.get("id")) != str(vacancy_id)]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=5)


if __name__ == "__main__":
    file_handler = JSONFileHandler()
    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("Python")
    for i in vacancies:
        all_vacancies = Vacancy(i["id"], i["name"], i["salary"], i["url"], i["snippet"]["requirement"])
        all_vacancies_dict = all_vacancies.to_dict()
        file_handler.add_vacancy(all_vacancies_dict)
        # file_handler.delete_vacancy("120769384")
        # x = file_handler.get_vacancies({"id": "121280339"})
        # print(x)

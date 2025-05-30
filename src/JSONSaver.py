import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union


class FileHandler(ABC):
    def __init__(self, filename: str) -> None:
        self._filename = filename

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
    def __init__(self, filename: str = "Data/vacancies.json") -> None:
        super().__init__(filename)

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Метод для добавления вакансии в файл."""
        vacancies = self.get_vacancies()
        if vacancy not in vacancies:
            vacancies.append(vacancy)
            with open(self._filename, "w") as f:
                json.dump(vacancies, f, indent=4)

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Метод для получения вакансий по указанным критериям."""
        if not os.path.exists(self._filename):
            return []
        with open(self._filename, "r") as f:
            vacancies = json.load(f)
        if criteria:
            filtered_vacancies = []
            for vacancy in vacancies:
                if all(vacancy.get(key) == value for key, value in criteria.items()):
                    filtered_vacancies.append(vacancy)
            return filtered_vacancies
        return vacancies

    def delete_vacancy(self, vacancy_id: Union[int, str]) -> None:
        """Метод для удаления вакансии."""
        vacancies = self.get_vacancies()
        vacancies = [vacancy for vacancy in vacancies if str(vacancy.get("id")) != str(vacancy_id)]
        with open(self._filename, "w") as f:
            json.dump(vacancies, f, indent=4)

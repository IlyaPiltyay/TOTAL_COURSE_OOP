import unittest
from unittest.mock import MagicMock, patch

from src.vacancy import Vacancy
from utils.vacancies_by_keyword import get_vacancies_by_keyword


class TestGetVacanciesByKeyword(unittest.TestCase):

    @patch("builtins.input", side_effect=["Python", "2"])
    def test_get_vacancies_by_keyword(self, mock_input):
        mock_hh_api = MagicMock()
        mock_hh_api.get_vacancies.return_value = [
            {
                "id": 1,
                "name": "Python Developer",
                "salary": 100000,
                "url": "http://example.com/1",
                "snippet": {"requirement": "Experience in Python."},
                "employer": {"name": "Ozon"},
            },
            {
                "id": 2,
                "name": "Senior Python Developer",
                "salary": 150000,
                "url": "http://example.com/2",
                "snippet": {"requirement": "Expert in Python."},
                "employer": {"name": "Ozon"},
            },
            {
                "id": 3,
                "name": "Java Developer",
                "salary": 120000,
                "url": "http://example.com/3",
                "snippet": {"requirement": "Experience in Java."},
                "employer": {"name": "Ozon"},
            },
        ]

        mock_file_handler = MagicMock()
        get_vacancies_by_keyword(mock_hh_api, mock_file_handler)
        self.assertEqual(mock_file_handler.add_vacancy.call_count, 2)
        expected_vacancy_1 = Vacancy(
            id=1, name="Python Developer", salary=100000, url="http://example.com/1", snippet="Experience in Python.",
            company="Ozon"
        ).to_dict()

        expected_vacancy_2 = Vacancy(
            id=2,
            name="Senior Python Developer",
            salary=150000,
            url="http://example.com/2",
            snippet="Expert in Python.",
            company="Ozon",
        ).to_dict()
        mock_file_handler.add_vacancy.assert_any_call(expected_vacancy_1)
        mock_file_handler.add_vacancy.assert_any_call(expected_vacancy_2)


if __name__ == "__main__":
    unittest.main()

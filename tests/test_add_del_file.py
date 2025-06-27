import unittest
from unittest.mock import MagicMock, patch

from src.vacancy import Vacancy
from utils.add_to_file import add_vacancy_to_file, delete_vacancy_from_file


class TestVacancyFunctions(unittest.TestCase):

    @patch("builtins.input", side_effect=["1", "Test Vacancy", "100000", "http://example.com", "Experience required"])
    def test_add_vacancy_to_file(self, mock_input):
        mock_file_handler = MagicMock()
        add_vacancy_to_file(mock_file_handler)
        expected_vacancy = Vacancy(
            id=1, name="Test Vacancy", salary=100000, url="http://example.com", snippet="Experience required"
        )
        mock_file_handler.add_vacancy.assert_called_once_with(expected_vacancy.to_dict())

    @patch("builtins.input", side_effect=["1"])
    def test_delete_vacancy_from_file(self, mock_input):
        mock_file_handler = MagicMock()
        delete_vacancy_from_file(mock_file_handler)
        mock_file_handler.delete_vacancy.assert_called_once_with("1")


if __name__ == "__main__":
    unittest.main()

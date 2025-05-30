import unittest
from unittest.mock import Mock, patch

from src.HeadHunterAPI import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):

    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get):
        # Настраиваем ответ мока
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Python Developer",
                    "employer": {"name": "Tech Company"},
                    "alternate_url": "http://example.com/vacancy/1",
                    "salary": {"from": 60000, "to": 80000},
                    "id": 1,
                },
                {
                    "name": "Senior Python Developer",
                    "employer": {"name": "Another Tech Company"},
                    "alternate_url": "http://example.com/vacancy/2",
                    "salary": {"from": 100000, "to": None},
                    "id": 2,
                },
            ]
        }
        mock_get.return_value = mock_response

        # Проверяем, что возвращается правильный результат
        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        self.assertEqual(vacancies[0]["name"], "Python Developer")
        self.assertEqual(vacancies[0]["company"], "Tech Company")
        self.assertEqual(vacancies[0]["url"], "http://example.com/vacancy/1")
        self.assertEqual(vacancies[0]["salary"], {"from": 60000, "to": 80000})
        self.assertEqual(vacancies[0]["id"], 1)

    @patch("requests.get")
    def test_get_vacancies_no_items(self, mock_get):
        # Настраиваем ответ мока
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        # Проверяем поведение при отсутствии вакансий
        api = HeadHunterAPI()
        vacancies = api.get_vacancies("NonExistingKeyword")
        self.assertEqual(vacancies, [])

    @patch("requests.get")
    def test_get_vacancies_error(self, mock_get):
        # Настраиваем ответ мока с ошибкой
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Проверяем, что выбрасывается ошибка при ошибочном запросе
        api = HeadHunterAPI()
        with self.assertRaises(ValueError) as context:
            api.get_vacancies("Python")
        self.assertEqual(str(context.exception), "Ошибка запроса: 404")


if __name__ == "__main__":
    unittest.main()

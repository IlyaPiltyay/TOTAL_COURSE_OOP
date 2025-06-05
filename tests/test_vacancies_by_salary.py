import unittest
from unittest.mock import MagicMock, patch, mock_open
import json

from utils.vacancies_by_salary import get_top_vacancies_by_salary


class TestGetTopVacanciesBySalary(unittest.TestCase):

    @patch('builtins.input', side_effect=['2'])
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"id": 1, "name": "Junior Developer", "salary": 50000, "url": "http://example.com/1",
         "snippet": {"requirement": "Learning experience."}},
        {"id": 2, "name": "Middle Developer", "salary": 80000, "url": "http://example.com/2",
         "snippet": {"requirement": "Some experience needed."}},
        {"id": 3, "name": "Senior Developer", "salary": {"from": 120000}, "url": "http://example.com/3",
         "snippet": {"requirement": "Expertise is required."}},
        {"id": 4, "name": "Lead Developer", "salary": {"from": 150000}, "url": "http://example.com/4",
         "snippet": {"requirement": "Leadership skills."}},
    ]))
    @patch('builtins.print')  # Моким функцию print
    def test_get_top_vacancies_by_salary(self, mock_print, mock_open, mock_input):
        mock_file_handler = MagicMock()
        get_top_vacancies_by_salary(mock_file_handler)
        self.assertEqual(mock_print.call_count, 2)
        printed_arguments = [call[0][0] for call in mock_print.call_args_list]
        expected_outputs = [
            '4 Lead Developer Зарплата: {\'from\': 150000} http://example.com/4',
            '3 Senior Developer Зарплата: {\'from\': 120000} http://example.com/3'
        ]

        for expected in expected_outputs:
            self.assertIn(expected, printed_arguments)


if __name__ == '__main__':
    unittest.main()

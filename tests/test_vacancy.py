import unittest

from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):

    def test_initialization_valid(self):
        vacancy = Vacancy(1, "Software Engineer", 1000, "http://example.com", "Experience in Python")
        self.assertEqual(vacancy.id, 1)
        self.assertEqual(vacancy.name, "Software Engineer")
        self.assertEqual(vacancy.salary, 1000)
        self.assertEqual(vacancy.url, "http://example.com")
        self.assertEqual(vacancy.snippet, "Experience in Python")

    def test_initialization_invalid_name(self):
        vacancy = Vacancy(2, "", 1000, "http://example.com", "Experience in Python")
        self.assertEqual(vacancy.name, "Название вакансии не указано")

    def test_initialization_invalid_salary(self):
        vacancy = Vacancy(3, "Data Analyst", -500, "http://example.com", "Experience in SQL")
        self.assertEqual(vacancy.salary, 0)

        vacancy = Vacancy(4, "Data Scientist", {}, "http://example.com", "Experience in ML")
        self.assertEqual(vacancy.salary, 0)

        vacancy = Vacancy(
            5, "Product Manager", {"from": 1500, "to": 2000}, "http://example.com", "Experience in Agile"
        )
        self.assertEqual(vacancy.salary, 1500)

    def test_initialization_invalid_url(self):
        vacancy = Vacancy(6, "Web Developer", 1200, "invalid_url", "Experience in HTML/CSS")
        self.assertEqual(vacancy.url, "Ссылка не указана")

    def test_to_dict(self):
        vacancy = Vacancy(1, "Software Engineer", 1000, "http://example.com", "Experience in Python")
        expected_dict = {
            "id": 1,
            "name": "Software Engineer",
            "salary": 1000,
            "url": "http://example.com",
            "snippet": "Experience in Python",
        }
        self.assertEqual(vacancy.to_dict(), expected_dict)

    def test_comparison_operators(self):
        vacancy1 = Vacancy(1, "Software Engineer", 1000, "http://example.com", "Experience in Python")
        vacancy2 = Vacancy(2, "Data Scientist", 1200, "http://example.com", "Experience in ML")

        self.assertTrue(vacancy1 < vacancy2)
        self.assertTrue(vacancy1 <= vacancy2)
        self.assertFalse(vacancy1 > vacancy2)
        self.assertFalse(vacancy1 >= vacancy2)
        self.assertFalse(vacancy1 == vacancy2)
        self.assertTrue(vacancy1 != vacancy2)

    def test_repr_and_str(self):
        vacancy = Vacancy(1, "Software Engineer", 1000, "http://example.com", "Experience in Python")
        self.assertEqual(
            repr(vacancy),
            "Vacancy(name='Software Engineer', salary=1000, url='http://example.com' , snippet= Experience in Python)",
        )
        self.assertEqual(
            str(vacancy),
            "1 - Software Engineer, salary=1000, Ссылка : 'http://example.com',требования : Experience in Python",
        )


if __name__ == "__main__":
    unittest.main()

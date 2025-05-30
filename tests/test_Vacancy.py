import unittest

from src.Vacancy import Vacancy


class TestVacancy(unittest.TestCase):

    def test_creation_valid(self)-> None:
        vacancy = Vacancy(1, "Software Engineer", "Tech Company", 60000, "http://example.com")
        self.assertEqual(vacancy.id, 1)
        self.assertEqual(vacancy.name, "Software Engineer")
        self.assertEqual(vacancy.company, "Tech Company")
        self.assertEqual(vacancy.salary, 60000)
        self.assertEqual(vacancy.url, "http://example.com")

    def test_creation_invalid_name(self)-> None:
        vacancy = Vacancy(2, "", "Tech Company", 50000, "http://example.com")
        self.assertEqual(vacancy.name, "Название вакансии не указано")

    def test_creation_invalid_company(self)-> None:
        vacancy = Vacancy(3, "Software Engineer", "", 50000, "http://example.com")
        self.assertEqual(vacancy.company, "Название компании-работодателя не указано")

    def test_creation_invalid_salary(self)-> None:
        vacancy = Vacancy(4, "Software Engineer", "Tech Company", -100, "http://example.com")
        self.assertEqual(vacancy.salary, 0)

    def test_creation_invalid_url(self)-> None:
        vacancy = Vacancy(5, "Software Engineer", "Tech Company", 50000, "invalid_url")
        self.assertEqual(vacancy.url, "Ссылка не указана")

    def test_comparison_operators(self)-> None:
        vacancy1 = Vacancy(6, "Junior Developer", "Tech Company", 40000, "http://example.com")
        vacancy2 = Vacancy(7, "Senior Developer", "Tech Company", 80000, "http://example.com")

        self.assertTrue(vacancy1 < vacancy2)
        self.assertTrue(vacancy1 <= vacancy2)
        self.assertFalse(vacancy1 == vacancy2)
        self.assertTrue(vacancy1 != vacancy2)
        self.assertFalse(vacancy1 > vacancy2)
        self.assertFalse(vacancy1 >= vacancy2)

    def test_repr(self)-> None:
        vacancy = Vacancy(8, "DevOps Engineer", "Tech Company", 70000, "http://example.com")
        self.assertEqual(
            repr(vacancy),
            "Vacancy(name='DevOps Engineer', company='Tech Company', salary=70000, url='http://example.com')",
        )

    def test_to_dict(self)-> None:
        vacancy = Vacancy(9, "Data Scientist", "Data Company", 85000, "http://example.com")
        expected_dict = {
            "id": 9,
            "name": "Data Scientist",
            "company": "Data Company",
            "salary": 85000,
            "url": "http://example.com",
        }
        self.assertEqual(vacancy.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()

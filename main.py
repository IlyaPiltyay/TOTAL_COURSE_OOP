from src.date_Base import DBManager
from src.DB import create_database_and_tables
from src.headHunterAPI import HeadHunterAPI
from src.jsonSaver import JSONFileHandler
from src.vacancy import Vacancy
from utils.add_to_file import add_vacancy_to_file, delete_vacancy_from_file
from utils.vacancies_by_keyword import get_vacancies_by_keyword
from utils.vacancies_by_salary import get_top_vacancies_by_salary


def user_interaction() -> None:
    """Функция взаимодействия с пользоватем"""
    try:
        # hh_api = HeadHunterAPI()
        db_manager = DBManager(dbname="job_database", user="postgres", password="6577")

        while True:
            print("\nВыберите действие:")
            print("1. Получить количество вакансий по компаниям")
            print("2. Получить все вакансии")
            print("3. Получить вакансии с зарплатой выше средней")
            print("4. Поиск вакансий по ключевым словам")
            print("5. Выход")

            choice = input("Введите номер действия: ")

            if choice == "1":
                print("Количество вакансий по компаниям:")
                companies_count = db_manager.get_companies_and_vacancies_count()
                for company_name, count in companies_count:
                    print(f"Компания: {company_name}, Вакансий: {count}")

            elif choice == "2":
                print("\nВсе вакансии:")
                vacancies = db_manager.get_all_vacancies()
                for name, salary, company_name in vacancies:
                    print(f"Вакансия: {name}, Зарплата: {salary}, Компания: {company_name}")

            elif choice == "3":
                avg_salary = db_manager.get_avg_salary()
                print(f"\nСредняя зарплата: {avg_salary}")
                print("\nВакансии с зарплатой выше средней:")
                higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
                for name, salary, company_name in higher_salary_vacancies:
                    print(f"Вакансия: {name}, Зарплата: {salary}, Компания: {company_name}")

            elif choice == "4":
                keyword_input = input("Введите слова для поиска, разделенные пробелами: ")
                keywords = keyword_input.split()  # Получаем список ключевых слов
                print(f"\nВакансии с ключевыми словами {keywords}:")

                # Получение вакансий из базы данных по ключевым словам
                keyword_vacancies = db_manager.get_vacancies_by_keywords(keywords)

                if keyword_vacancies:
                    for vacancy in keyword_vacancies:
                        name = vacancy[1]  # Получаем название вакансии
                        salary = vacancy[2]  # Получаем зарплату
                        url = vacancy[3]  # Получаем URL вакансии
                        print(f"Вакансия: {name}, Зарплата: {salary}, URL: {url}")
                    else:
                        print("Нет вакансий, соответствующих введенным ключевым словам.")

            elif choice == "5":
                print("Выход из программы.")
                break

            else:
                print("Некорректный ввод. Пожалуйста, выберите действие от 1 до 5.")

    finally:
        db_manager.close()

        # print("\nВыберите действие:")
        # print("1. Поиск вакансий по ключевому слову")
        # print("2. Получить топ N вакансий по зарплате")
        # print("3. Добавить вакансию в файл")
        # print("4. Удалить вакансию из файла")
        # print("5. Выход")
        #
        # choice = input("Введите номер действия: ")
        #
        # if choice == "1":
        #     get_vacancies_by_keyword(hh_api, file_handler)
        # elif choice == "2":
        #     get_top_vacancies_by_salary(file_handler)
        # elif choice == "3":
        #     add_vacancy_to_file(file_handler)
        # elif choice == "4":
        #     delete_vacancy_from_file(file_handler)
        # elif choice == "5":
        #     print("Выход из программы.")
        #     break
        # else:
        #     print("Некорректный ввод. Пожалуйста, выберите действие от 1 до 5.")


if __name__ == "__main__":
    user_interaction()
    DB_NAME = "job_database"
    USER = "postgres"
    PASSWORD = "6577"
    # Создание базы данных и таблиц
    create_database_and_tables(DB_NAME, USER, PASSWORD)
    db_manager = DBManager("your_db_name", "your_user", "your_password")

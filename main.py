from src.headHunterAPI import HeadHunterAPI
from src.jsonSaver import JSONFileHandler
from utils.add_to_file import add_vacancy_to_file, delete_vacancy_from_file
from utils.vacancies_by_keyword import get_vacancies_by_keyword
from utils.vacancies_by_salary import get_top_vacancies_by_salary


def user_interaction() -> None:
    hh_api = HeadHunterAPI()
    file_handler = JSONFileHandler()

    while True:
        print("\nВыберите действие:")
        print("1. Поиск вакансий по ключевому слову")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Добавить вакансию в файл")
        print("4. Удалить вакансию из файла")
        print("5. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            get_vacancies_by_keyword(hh_api, file_handler)
        elif choice == "2":
            get_top_vacancies_by_salary(file_handler)
        elif choice == "3":
            add_vacancy_to_file(file_handler)
        elif choice == "4":
            delete_vacancy_from_file(file_handler)
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите действие от 1 до 5.")


if __name__ == "__main__":
    user_interaction()

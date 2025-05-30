from src.HeadHunterAPI import HeadHunterAPI
from src.JSONSaver import JSONFileHandler
from src.Vacancy import Vacancy


def user_interaction():
    hh_api = HeadHunterAPI()
    file_handler = JSONFileHandler()

    while True:
        print("\nВыберите действие:")
        print("1. Поиск вакансий по ключевому слову")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Получить вакансии с ключевым словом из файла")
        print("4. Записать вакансию в файл")
        print("5. Удалить вакансию из файла")
        print("6. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            keyword = input("Введите поисковый запрос: ")
            cantidad = int(input("Введите количество вакансий для получения: "))
            vacancies = hh_api.get_vacancies(keyword)[0:cantidad]
            if vacancies:
                for vacancy in vacancies:
                    print(
                        f"Название: {vacancy['name']}, Компания: {vacancy['company']}, "
                        f"Зарплата: {vacancy['salary']}, Ссылка: {vacancy['url']}, id{vacancy["id"]}"
                    )
            else:
                print("Вакансии не найдены.")

        elif choice == "2":
            n = int(input("Введите количество вакансий для получения по зарплате: "))
            vacancies = file_handler.get_vacancies()
            sorted_vacancies = sorted(vacancies, key=lambda x: x.get("salary", 0), reverse=True)[:n]
            if sorted_vacancies:
                for vacancy in sorted_vacancies:
                    print(
                        f"Название: {vacancy['name']}, Компания: {vacancy['company']},"
                        f" Зарплата: {vacancy['salary']}, Ссылка: {vacancy['url']}"
                    )
            else:
                print("Вакансии не найдены.")

        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска в файле: ")
            vacancies = file_handler.get_vacancies(name=keyword)
            if vacancies:
                for vacancy in vacancies:
                    print(
                        f"Название: {vacancy['name']}, Компания: {vacancy['company']},"
                        f" Зарплата: {vacancy['salary']}, Ссылка: {vacancy['url']}"
                    )
            else:
                print("Вакансии не найдены.")

        elif choice == "4":
            name = input("Введите название вакансии: ")
            company = input("Введите название компании: ")
            salary = float(input("Введите зарплату (если не указана, введите 0): "))
            url = input("Введите ссылку на вакансию: ")
            id = int(input("Введите ID вакансии"))

            vacancy = Vacancy(id=id, name=name, company=company, salary=salary, url=url)
            file_handler.add_vacancy(vacancy.to_dict())
            print("Вакансия добавлена в файл.")

        elif choice == "5":
            vacancy_id = input("Введите ID вакансии для удаления: ")
            file_handler.delete_vacancy(vacancy_id)
            print(f"Вакансия с ID {vacancy_id} удалена из файла.")

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите действие от 1 до 6.")


if __name__ == "__main__":
    user_interaction()

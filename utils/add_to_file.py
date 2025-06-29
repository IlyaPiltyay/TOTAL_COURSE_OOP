from src.vacancy import Vacancy


def add_vacancy_to_file(file_handler) -> None:
    id = int(input("Введите ID вакансии: "))
    name = input("Введите название вакансии: ")
    salary = float(input("Введите зарплату (если не указана, введите 0): "))
    url = input("Введите ссылку на вакансию: ")
    snippet = input("Введите требования: ")

    vacancy = Vacancy(id=id, name=name, salary=salary, url=url, snippet=snippet, company="Ozon")
    file_handler.add_vacancy(vacancy.to_dict())
    print("Вакансия добавлена в файл.")


def delete_vacancy_from_file(file_handler) -> None:
    vacancy_id = input("Введите ID вакансии для удаления: ")
    file_handler.delete_vacancy(vacancy_id)
    print(f"Вакансия с ID {vacancy_id} удалена из файла.")

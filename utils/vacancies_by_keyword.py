from src.vacancy import Vacancy


def get_vacancies_by_keyword(hh_api, file_handler) -> None:
    keyword = input("Введите поисковый запрос: ")
    count_vacancy = int(input("Введите количество вакансий для получения: "))
    vacancies = hh_api.get_vacancies(keyword)[:count_vacancy]

    for vacancy in vacancies:
        vacancy_instance = Vacancy(
            id=vacancy["id"],
            name=vacancy["name"],
            salary=vacancy["salary"],
            url=vacancy["url"],
            snippet=vacancy["snippet"]["requirement"],
        )
        file_handler.add_vacancy(vacancy_instance.to_dict())

    print(f"{len(vacancies)} вакансий записано в файл")

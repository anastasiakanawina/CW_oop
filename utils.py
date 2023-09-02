from coursework_api.get_api import HeadHunterAPI
from coursework_api.get_api import SuperJobAPI
from coursework_api.vacancy import Vacancy


def init_query(query=None):
    """ Возвращает словарь с вакансиями """
    # Инициализируем API для HeadHunter и SuperJob
    hh_api = HeadHunterAPI()
    sj_api = SuperJobAPI()
    hh_vacancies = hh_api.get_vacancies(query)
    sj_vacancies = sj_api.get_vacancies(query)

    Vacancy.vacancies_from_hh(hh_vacancies)
    Vacancy.vacancies_from_sj(sj_vacancies)
    load_vacancies = Vacancy.all_vacancies

    vacancies_data = []
    for vacancy in load_vacancies:
        vacancies_data.append(vacancy.__dict__)

    return vacancies_data

def user_interaction():

    # Список доступных команд для пользователя
    print("Доступные команды:")
    print("1. Поиск вакансий")
    print("2. Получить топ N вакансий по зарплате")
    print("3. Получить вакансии в отсортированном виде")
    print("4. Получить вакансии с ключевыми словами")
    print("5. Выход")

    while True:
        try:
            choice = int(input("Выберите команду: "))
            if choice == 1:
                search_query = input("Введите поисковый запрос(или оставьте пусто, чтобы выгрузить все): ")
                vacancies_data = init_query(search_query)

                if not vacancies_data:
                    print("Нет вакансий, соответствующих запросу.")
                else:
                    print("Результаты поиска:")

                    for vacancy in vacancies_data:
                        print(f"ID - {vacancy['vac_id']}\n"
                              f"Title - {vacancy['title']}\n"
                              f"URL - {vacancy['link']}\n"
                              f"Salary from {vacancy['salary']}\n"
                              f"Description - {vacancy['description']}\n"
                              "")

            elif choice == 2:
                top_n = int(input("Введите количество вакансий для вывода в топ N: "))
                search_query = input("Введите поисковый запрос(или оставьте пусто, чтобы выгрузить по всем вакансиям): ")
                vacancies_data = init_query(search_query)
                sorted_vacancies = sorted(vacancies_data, key=lambda x: x['salary'], reverse=True)[:top_n]

                if not sorted_vacancies:
                    print("Нет вакансий с зарплатой.")
                else:
                    print(f"Топ {top_n} вакансий по зарплате:")
                    for i, vacancy in enumerate(sorted_vacancies, start=1):
                        print(f"{i}. {vacancy['title']} ({vacancy['salary']})")

            elif choice == 3:
                search_query = input("Введите поисковый запрос(или оставьте пусто, чтобы выгрузить по всем вакансиям): ")
                vacancies_data = init_query(search_query)
                sorted_vacancies = sorted(vacancies_data, key=lambda x: x['title'])

                if not sorted_vacancies:
                    print("Нет вакансий для сортировки.")
                else:
                    print("Вакансии в отсортированном виде:")
                    for i, vacancy in enumerate(sorted_vacancies, start=1):
                        print(f"{i}. {vacancy['title']}")

            elif choice == 4:
                print("Выход из программы.")
                break
            else:
                print("Некорректный выбор команды. Попробуйте еще раз.")
        except ValueError:
            print("Введите число для выбора команды.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")



from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time

# Инициализация браузера
browser = webdriver.Firefox()

# Переход на главную страницу Википедии
browser.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
assert "Википедия" in browser.title

# Функция для поиска статьи по запросу
def search_wikipedia(query):
    search_box = browser.find_element(By.NAME, "search")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Ждем загрузки страницы

# Функция для листания параграфов статьи
def browse_paragraphs():
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for i, paragraph in enumerate(paragraphs):
        if paragraph.text.strip():  # Пропускаем пустые параграфы
            print(f"\nПараграф {i + 1}:")
            print(paragraph.text)
            input("Нажмите Enter для продолжения...")

# Функция для перехода на связанные страницы
def browse_links():
    # Ищем только ссылки, которые ведут на статьи (игнорируем служебные ссылки)
    links = browser.find_elements(By.CSS_SELECTOR, "div.mw-parser-output p a[href^='/wiki/']")
    print("\nДоступные связанные страницы:")
    valid_links = []
    for i, link in enumerate(links[:10]):  # Ограничиваем список 10 ссылками
        if link.text.strip():  # Пропускаем пустые ссылки
            print(f"{i + 1}. {link.text}")
            valid_links.append(link)
    if not valid_links:
        print("Нет доступных связанных страниц.")
        return
    choice = int(input("Выберите номер страницы: ")) - 1
    if 0 <= choice < len(valid_links):
        # Прокручиваем страницу, чтобы элемент стал видимым
        browser.execute_script("arguments[0].scrollIntoView();", valid_links[choice])
        time.sleep(1)  # Ждем, пока элемент станет видимым
        valid_links[choice].click()
        time.sleep(2)  # Ждем загрузки страницы
    else:
        print("Неверный выбор.")

# Основной цикл программы
def main():
    # Запрос у пользователя первоначального запроса
    initial_query = input("Введите ваш первоначальный запрос: ")
    search_wikipedia(initial_query)

    while True:
        # Предложение пользователю вариантов действий
        print("\nВыберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")
        choice = input("Ваш выбор: ")

        if choice == "1":
            browse_paragraphs()
        elif choice == "2":
            browse_links()
        elif choice == "3":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

# Запуск программы
if __name__ == "__main__":
    try:
        main()
    finally:
        # Закрытие браузера при завершении программы
        browser.quit()
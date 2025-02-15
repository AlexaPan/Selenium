from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def print_paragraphs(driver):
    try:
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        for index, paragraph in enumerate(paragraphs):
            print(f"Параграф {index + 1}:\n{paragraph.text}\n")
    except NoSuchElementException:
        print("Параграфы не найдены.")

def navigate_to_link(driver):
    try:
        links = driver.find_elements(By.XPATH, "//div[@class='mw-parser-output']//a[starts-with(@href, '/wiki/') and not(contains(@href, ':'))]")
        links_text = [link.text for link in links]

        for index, link_text in enumerate(links_text):
            print(f"{index + 1}. {link_text}")

        choice = int(input("Введите номер ссылки для перехода или 0 для возврата: "))
        if choice > 0 and choice <= len(links):
            links[choice - 1].click()
            WebDriverWait(driver, 10).until(EC.title_contains("Википедия"))
            return True
    except (NoSuchElementException, TimeoutException):
        print("Ошибка при переходе по ссылке.")
    except ValueError:
        print("Пожалуйста, введите корректный номер.")
    return False

def main():
    browser = webdriver.Firefox()

    try:
        browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")
        WebDriverWait(browser, 10).until(EC.title_contains("Википедия"))

        while True:
            initial_query = input("Введите ваш первоначальный запрос: ")
            try:
                search_box = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "searchInput")))
                search_box.clear()
                search_box.send_keys(initial_query)
                search_box.send_keys(Keys.RETURN)
                WebDriverWait(browser, 10).until(EC.title_contains(initial_query))
            except (NoSuchElementException, TimeoutException):
                print("Ошибка поиска. Попробуйте снова.")
                continue

            while True:
                print("\nВыберите действие:")
                print("1. Листать параграфы текущей статьи")
                print("2. Перейти на одну из связанных страниц")
                print("3. Выйти из программы")

                action = input("Введите номер действия: ")

                if action == '1':
                    print_paragraphs(browser)
                elif action == '2':
                    if not navigate_to_link(browser):
                        print("Неверный выбор или возврат. Попробуйте снова.")
                elif action == '3':
                    print("Выход из программы.")
                    return
                else:
                    print("Неверный выбор. Попробуйте снова.")
    finally:
        browser.quit()

if __name__ == "__main__":
    main()
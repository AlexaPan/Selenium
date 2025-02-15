from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


browser = webdriver.Firefox()

browser.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
assert "Википедия" in browser.title
initial_query = input("Введите ваш первоначальный запрос: ")

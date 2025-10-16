from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import copy
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
from datetime import datetime

def write_to_log(function_name):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('execution_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"{function_name}-{current_time}\n")
    print(f"Выполнено: {function_name} в {current_time}")

with open('execution_log.txt', 'w', encoding='utf-8') as f:
    f.write(f"Начало работы: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/")
time.sleep(1)
write_to_log("initialize_driver")

clickable_element = driver.find_element(By.XPATH, value='/html/body/nav/ul/li[4]/a')
clickable_element.click()
time.sleep(1)
write_to_log("click_login_button")

ActionChains(driver)\
    .key_down(Keys.ESCAPE)\
    .send_keys("a")\
    .key_up(Keys.ESCAPE)\
    .send_keys("b")\
    .perform()
time.sleep(2)
write_to_log("perform_keyboard_actions")

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
write_to_log("scroll_page")

i = 1
array = []
while i <= 70:
    subarr = []
    vac = driver.find_element(By.XPATH, value=f'/html/body/div[1]/div/main/section/ul/li[{i}]/div/div[2]/h3')
    subarr.append(vac.text)
    comp = driver.find_element(By.XPATH, value=f'/html/body/div[1]/div/main/section/ul/li[{i}]/div/div[2]/h4')
    subarr.append(comp.text)
    loc = driver.find_element(By.XPATH, value=f'/html/body/div[1]/div/main/section/ul/li[{i}]/div/div[2]/div/span')
    subarr.append(loc.text)
    try:
        oi = driver.find_element(By.XPATH, value=f'/html/body/div[1]/div/main/section/ul/li[{i}]/div/div[2]/div/div')
        subarr.append(oi.text)
    except:
        subarr.append("Нет прочей информации")
    timer = driver.find_element(By.XPATH, value=f'/html/body/div[1]/div/main/section/ul/li[{i}]/div/div[2]/div/time')
    subarr.append(timer.text)
    array.append(subarr)
    i += 1
write_to_log("extract_job_data")

column = ['Должность', 'Компания', 'Расположение', 'Прочая информация', 'Время создания заявки']
data = np.array(array)
df = pd.DataFrame(data, columns=column)
print(df)
write_to_log("create_dataframe")

df.to_csv('data.csv')
write_to_log("save_to_csv")

with open('execution_log.txt', 'a', encoding='utf-8') as f:
    f.write(f"Все операции завершены: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

driver.quit()
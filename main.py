from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

import time


# PATH = "C:\\Users\\Skelet0N_0FF\\Desktop\\parsing\\driver\\geckodriver.exe"
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

try:
    driver.get("https://mandarinbean.com/new-hsk-1-word-list/")
    headers = [header.get_attribute("innerHTML") for header in driver.find_elements(By.TAG_NAME, "strong")]
    final_data = pd.DataFrame(columns=headers)
    def get_table(webpage):     # Берёт страницу и собирает с неё все элементы таблицы (в тегах <td>) в датафрейм
        driver.get(webpage)
        element = WebDriverWait(driver, 10).until(          # Ожидание прогрузки элементов в тегах <td>
            EC.presence_of_element_located((By.TAG_NAME, "td"))
        )
        temp_data = [value.get_attribute("innerHTML") for value in driver.find_elements(By.TAG_NAME, "td")]
        data = []
        for i in range(len(temp_data)):         # Не уверен, что написал эту штуку правильно ПРОВЕРЬ
            data.append([td for td in temp_data[0:i+1]])
            temp_data = temp_data[i+1:]
        return pd.DataFrame(data=data, columns=headers)

    for i in range(1, 4):
        final_data = pd.concat(objs=[final_data, get_table(f"https://mandarinbean.com/new-hsk-{i}-word-list/")]) 

    final_data.drop(labels="No", axis=1)
    final_data.to_csv(path_or_buf=".\\pinyin.csv")
#except Exception as e:
#    print(f"{e}\n\nThe process will terminate in 10 seconds...")
#    time.sleep(10)
finally:
    driver.close()
    driver.quit()
#    exit()

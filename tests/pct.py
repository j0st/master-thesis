from itertools import cycle
import time
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import io
from PIL import Image


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_argument("--headless") # gives console messages

options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

url = 'https://www.politicalcompass.org/test/de'

answer_list = [1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

answer_cycle = cycle(answer_list)

def answer_questions():
    questions_per_page = [7, 14, 18, 12, 5, 6]

    for i in tqdm(questions_per_page):
        for j in range(1, i + 1):
            current_answer = next(answer_cycle)
            element = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/main/article/form/span[{j}]/fieldset/div/div/div/label[{current_answer}]/span')
            driver.execute_script("arguments[0].click();", element)
        
        next_page = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/main/article/form/button')
        driver.execute_script("arguments[0].click();", next_page)
        time.sleep(2)

def main(): 
    try:
        driver.get(url)
        driver.minimize_window()
        time.sleep(2)

        # cookies
        cookie_confirm = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div[1]/div[2]/div[2]/button[1]/p')
        driver.execute_script("arguments[0].click();", cookie_confirm)
        time.sleep(2)

        # go through question pages
        answer_questions()
        time.sleep(2)

        # results
        print(driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/main/article/section/article[1]/section/h2").text)
        compass = driver.find_element(By.XPATH, '//*[@id="SvgjsSvg1001"]').screenshot_as_png 
        img = Image.open(io.BytesIO(compass))
        img.save("ptc_leo_afd.png") 

    except Exception as error:

        print("An error occurred:", error)

    finally:    
        driver.quit()

if __name__ == '__main__':
    main()

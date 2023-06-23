from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

driver = webdriver.Edge()

driver.get('https://www.ign.com/playlist/rchnemesis/lists/top-100-indie-games')
print(driver.title)
body = driver.find_element(By.TAG_NAME,'body')
# simulate scrolling
for _ in range(20):  # adjust this range depending on your needs
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    
gamelist =[]
for i in range(1,101):
    img = driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[2]/div[3]/div/figure[{i}]/a/div[1]/div/img')
    game_name = img.get_attribute('alt')
    gamelist.append(game_name)
    
with open('gamelist.txt','w') as f:
    for i in gamelist:
        f.write(i+'\n')

driver.quit()
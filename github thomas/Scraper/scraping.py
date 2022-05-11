# %%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# %%
driver = webdriver.Firefox(r"C:\tools\selenium")
driver.get("https://www.meteoswiss.admin.ch/home/measurement-values.html?param=messwerte-lufttemperatur-10min&table=true")
# assert "Watson" in driver.title
rows = driver.find_elements_by_xpath("//table/tbody/tr")
r = len(rows)
print(r)

try:
    for i in range(1,r):
        th = driver.find_elements_by_xpath(f"//table/tbody/tr[{i}]/th")
        print(th[0].text)
        for j in range(1,9):
            td = driver.find_elements_by_xpath(f"//html/body/div[1]/div/div[1]/div/div/div[3]/div[1]/div/div[3]/div[2]/div/div/table/tbody/tr[{i}]/td[{j}]")
            print(td[0].text)
except BaseException as err:
    print(f"Unexpected {err=}, {type(err)=}")

# to close the browser
driver.close()

# %%

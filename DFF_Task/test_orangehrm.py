import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook, load_workbook
from orangehrm_page import web_page
from excel_data import ex_read
import datetime
from datetime import date
from datetime import datetime

@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.close()
    driver.quit()

@pytest.fixture()
def read_test_data(file_path=r"C:\Users\AM9131\Desktop\login_details.xlsx"):
    global input_file
    input_file=ex_read(file_path)
    return input_file.readdata()

@pytest.mark.parametrize('n', range(1,6))
def test_case1(driver,read_test_data,n,testername="Mallika"):
    obj1=web_page(driver)
    obj1.open_page("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    obj1.login_page(read_test_data[n]["Username"],read_test_data[n]["Password"])
    global input_file
    current_time = datetime.now()
    input_file.updatecellvalue(n+1,4,date.today())
    input_file.updatecellvalue(n+1, 5, current_time.strftime("%H:%M:%S"))
    input_file.updatecellvalue(n + 1, 6,testername)
    if "Dashboard" in driver.page_source:
        input_file.updatecellvalue(n+1,7,"valid login")
    else:
        input_file.updatecellvalue(n+1, 7, "invalid login")

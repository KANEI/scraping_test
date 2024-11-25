from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def get_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get(url)
    return driver

def set_start_date(driver,start_date):
    #初めの日程を設定
    if len(start_date) != 0:
        date_list = list(map(int, start_date.split("/")))
        for num,date_idx in enumerate(date_list):
            name = f'stage_start_date_{num+1}i'
            e1 = driver.find_element(By.ID, name)
            s = Select(e1)
            try:
                s.select_by_value(str(date_idx))
            except:
                pass


def set_end_date(driver,end_date):
    #終わりの日程を設定
    if len(end_date) != 0:
        date_list = list(map(int, end_date.split("/")))
        for num,date_idx in enumerate(date_list):
            e1 = driver.find_element(By.ID, f'stage_end_date_{num+1}i')
            s = Select(e1)
            try:
                s.select_by_value(str(date_idx))
            except:
                pass

def set_freeword(driver,freeword):
    #フリーワード
    if len(freeword)!=0:
        text_box = driver.find_element(By.NAME,"freeword")
        text_box.send_keys(freeword)

def set_erea(driver,erea):
    #エリア(東京:13, 神奈川:14)
    if len(erea) != 0:
        e1 = driver.find_element(By.ID,'pref_id')
        s = Select(e1)
        try:
            s.select_by_value(str(erea))
        except:
            pass

def push_search_button(driver):
    #検索
    submit_button = driver.find_element(By.XPATH,'//div[@class="col-sm-offset-3 col-sm-9"]/input')
    submit_button.click()

def do_search(driver,start_date="",end_date="",freeword="",erea=""):
    #日程を絞る
    set_start_date(driver,start_date)
    set_end_date(driver,end_date)
    #フリーワード入力
    set_freeword(driver,freeword)
    #エリアを限定
    set_erea(driver,erea)
    #検索ボタンを押す。
    push_search_button(driver)

def not_zero(driver):
    tag = driver.find_element(By.CLASS_NAME,"hit")
    return not("0-0件" in tag.text)


def is_last_page(driver):
    last_li = driver.find_element(By.XPATH, "//ul[@class='pagination']/li[last()]")
    class_name = last_li.get_attribute("class")
    if "disable" in class_name:
        return True
    else:
        return False


def move_to_next_page(driver):
    #次ページに移動
    last_li = driver.find_element(By.XPATH, "//ul[@class='pagination']/li[last()]")
    try:
        last_a = last_li.find_element(By.TAG_NAME, "a")
        link = last_a.get_attribute("href")
        # そのリンクをクリック
        driver.get(link) 
    except:
        print("次のページに移動できません。")
        pass

def get_new_url(driver):
    current_url = driver.current_url
    return current_url

def set_new_driver(driver):
    current_url = driver.current_url
    driver.get(current_url)
    return driver

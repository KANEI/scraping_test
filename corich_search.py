import requests
from bs4 import BeautifulSoup
from pages import *
from datetime import datetime

def get_soup(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    return soup

def get_stage(soup):
    tags = soup.find_all('p',class_="stage")
    text_list = [x.string for x in tags]
    return text_list

def get_group(soup):
    tags = soup.find_all('p',class_="group")
    text_list = [x.string for x in tags]
    return text_list

def get_theater(soup):
    tags = soup.find_all('p',class_="theater")
    theater_list = []

    for i in range(len(tags)):
        text_list = [x for x in tags[i].stripped_strings]
        theater_list.append(text_list)
    
    return theater_list

def get_period(soup):
    tags = soup.find_all('p',class_="period")
    period_list = []

    for i in range(len(tags)):
        text_list = [x for x in tags[i].stripped_strings]
        period_list.append(text_list[0])
    
    return period_list

def get_link(soup):
    tags = soup.find_all('a',class_="list-group-item box")
    link_list =[]

    for i in range(len(tags)):
        link = tags[i].get('href')
        link_list.append("https://stage.corich.jp"+str(link))
    return link_list

def is_date(date):

    if len(date) == 0:
        return True

    date_list = list(date.split("/"))
    date_list = list(map(int, date_list))
    con1 = bool(len(date_list) == 3)
    con2 = bool(1975 <= date_list[0] <= datetime.now().year + 1)
    con3 = bool(1 <= date_list[1] <= 12)
    con4 = bool(1 <= date_list[2] <= 31)
    return all([con1,con2,con3,con4])

def match_erea(theater,erea):
    if erea == "":
        return True
    elif erea == "関東":
        erea_list = ["東京","千葉","埼玉","神奈川","群馬","栃木","茨城","山梨"]
    else:
        erea_list = list(erea.split(","))

    for er in erea_list:
        if er in theater:
            return True
    return False


if __name__ == "__main__":

    #ドライバー、スープの準備
    print("処理を開始します。")
    default_url = 'https://stage.corich.jp/stage/search?utf8=%E2%9C%93&search=1&sort=start_desc&freeword_type=all&list_format=img&scale_type=0'
    driver = get_driver(default_url)
    soup = get_soup(default_url)

    #入力
    print("次の項目を指定しない場合はエンターを押してください。")

    while True:
        start_date = input("開始日を入力してください。(例：2024/01/01)")
        if is_date(start_date):
            break

    while True:
        end_date = input("終了日を入力してください。(例：2024/01/01)")
        if is_date(end_date):
            break
    
    freeword = input("フリーワードを入力してください。(公演、団体、出演者名など)")
    erea = input("限定するエリアを1つ入力してください。(例:東京)")
    print("検索条件が入力されました。処理中です...")
    
    #検索を行う。
    do_search(driver,start_date,end_date,freeword)
    print("以上の条件で検索します。")

    cnt = 0
    while True:
        url = get_new_url(driver)
        soup = get_soup(url)

        print("情報を読み込んでいます。少々お待ちください。")
        if not_zero(driver):
            stage = get_stage(soup)
            group = get_group(soup)
            theater = get_theater(soup)
            period = get_period(soup)
            link = get_link(soup)
        else:
            print("条件に一致するものが存在しません。")
            break

        print("-----------------")
        for i in range(len(stage)):
            if match_erea(theater[i][1],erea):
                print("stage: ", stage[i])
                print("group: ", group[i])
                print("theater: ", theater[i][0]+theater[i][1])
                print("period: ", period[i])
                print("link: " , link[i])
                print("-----------------")

        if cnt > 3:
            conti = input("続きを見る yes/no : ")
            if conti == "no":
                print("システムを終了します。")
                break

        if is_last_page(driver):
            print("システムを終了します。")
            break
        else:
            print("次のページに移動します。")
            move_to_next_page(driver)
            print("次のページに移動しました。")
            driver = set_new_driver(driver)
            cnt += 1

    input("エンターキーで終了")

    

    
    


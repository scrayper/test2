#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import datetime


# In[2]:


# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')  # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    if os.name == 'nt':
        return Chrome(executable_path=os.getcwd() + "/" + driver_path,options=options)
    elif os.name == 'posix':
        return Chrome(executable_path='/usr/local/Caskroom/chromedriver/88.0.4324.96/chromedriver', options=options)
        
    


# In[3]:


# main処理
def main():
    search_keyword = input('検索ワードを入力して下さい >>>')
        
    # driverを起動
    if os.name == 'nt':  # Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix':  # Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)

    #ポップアップ
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass

    # 検索窓に入力
    search_bar = driver.find_element_by_class_name("topSearch__text")
    search_bar.send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("iconFont--search").click()

    # 1ページから最終ページまでの情報をリスト格納
    exp_name_list = []
    exp_copy_list = []
    exp_status_list = []
    count = 0
    success = 0
    fail = 0
    while True:
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        copy_list = driver.find_elements_by_class_name('cassetteRecruit__copy')
        status_list = driver.find_elements_by_class_name('labelEmploymentStatus')
        for name, copy, status in zip(name_list, copy_list, status_list):
            try:
                exp_name_list.append(name.text)
                exp_copy_list.append(copy.text)
                exp_status_list.append(status.text)
                success += 1
            except Exception as e:
                fail += 1
            finally:
                count += 1
        #次のページをクリッック
        next_page = driver.find_elements_by_class_name("iconFont--arrowLeft")
        if len(next_page) >= 1:
            next_page_link = next_page[0].get_attribute('href')
            driver.get(next_page_link)
        else:
            break
                        
    #取得したデータを出力
    for exp_name, exp_copy, exp_status in zip(exp_name_list, exp_copy_list, exp_status_list):
        print(exp_name, exp_copy, exp_status)
    print('処理が終了しました')
    
    #CSVにデータを出力
    csv_date = datetime.datetime.today().strftime('%Y%m%d')
    file_name = 'mynabi' + '_' + search_keyword + csv_date
    #columns = ['会社名', 'キャッチコピー', '勤務形態']
    df = pd.DataFrame({'会社名': exp_name_list, 'キャッチコピー': exp_copy_list, '勤務形態': exp_status_list})
    df.to_csv(file_name)

    #テキストファイル出力
    def log():
        s = datetime.datetime.now().strftime('%Y%m%d%H%M')
        path_w = os.getcwd() + "/log.text"
        #path_w = '/Users/ogawatakayuki/Desktop/MyPandas/課題2/log.text'
        with open(path_w + _ + s, mode='w') as f:
                f.write('{}件のデータ取得に成功しました\n'.format(success))
                f.write('{}件のエラーが発生しました\n'.format(fail))
                f.write('{}件の処理が完了しました\n'.format(success))
                f.write('csv出力が完了しました')
    log()


# In[4]:


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()


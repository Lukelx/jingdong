# _*_ coding: utf-8 _*_

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pyquery import PyQuery as pq
import csv


def create_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins-discovery")

    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
    driver.start_client()
    # driver.delete_all_cookies()
    return driver

def scroll_down():
    html_page = driver.find_element_by_tag_name('html')
    for i in range(4):
        html_page.send_keys(Keys.END)
        time.sleep(1)

def get_products(driver):
    html = driver.page_source
    doc = pq(html, parser='html')
    items = doc('#plist .gl-warp .gl-item').items()
    products = []
    for item in items:
        p_price = item.find('.p-price .J_price:nth-child(1)').text().strip('¥').strip()
        p_name = item.find('.p-name a em').text()
        p_link = item.find('.p-name a').attr('href')
        p_commit = item.find('.p-commit .comment').text()
        p_shop = item.find('.p-shop span a').attr('title')
        shop_link = item.find('.p-shop span a').attr('href')
        products.append([p_price, p_name, 'https:' + str(p_link), p_commit, p_shop, 'https:' + str(shop_link)])
    return products




driver = create_driver()
offset = [x * 2 + 1 for x in range(0, 3)]
for num in offset:
    page_url = f'https://list.jd.com/list.html?cat=670,671,672&page={num}&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main'
    print('page' + str((num - 1) / 2 + 1))
    print(page_url)
    driver.get(page_url)
    time.sleep(1)
    scroll_down()
    time.sleep(1)
    products = get_products(driver)
    print(len(products))
    with open('jingdong.csv', 'a', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(products)

driver.quit()


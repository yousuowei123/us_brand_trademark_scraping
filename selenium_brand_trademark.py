# -*- coding:utf-8 -*-
# -*- author:cto_b -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from random import choice
import json
from settings import WEB_HEADERS_POOL, PROXY
from selenium.common.exceptions import NoSuchElementException


"""
The script is goal to scraping the amazon product brand info
"""

chrome_path = r"E:\Developer Tools\driver\chromedriver.exe"


def set_chrome_option():
    """
    set chrome options
    :return: chrome_options
    """
    chrome_options = webdriver.ChromeOptions()

    # set headless model
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    user_agent = 'user-agent={}'.format(choice(WEB_HEADERS_POOL))
    chrome_options.add_argument(user_agent)
    # permission loading image
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    print('chrome_options -->', chrome_options)

    return chrome_options


def execute(keyword, chrome_options=None):
    start_url = "https://www.uspto.gov/trademarks-application-process/search-trademark-database"
    print('downloading -->', start_url)

    driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    # driver.set_page_load_timeout(30)
    driver.get(start_url)

    wait = WebDriverWait(driver, 15)
    # first page
    print('process first page!')
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/article/div/p[3]/a')))
    element.click()

    # second page
    print('process second page!')
    basic_word = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/center/table[1]/tbody/tr[2]/td/font/font/a')))
    basic_word.click()

    # third page
    print('process third page!')
    wait.until(EC.title_contains('Trademark Electronic Search System (TESS)'))
    query = driver.find_element_by_xpath('//*[@id="querytext"]/input')
    query.clear()
    query.send_keys(keyword)
    submit = driver.find_element_by_xpath('/html/body/form/font/table[4]/tbody/tr[4]/td/input[3]')
    submit.click()

    # Todo get brand info, @key point
    try:
        is_target_table = driver.find_element_by_xpath('/html/body/table[7]/tbody/tr[2]/td[2]/a')
        print('is_target_table -->', is_target_table)
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[1]/input[3]')))
        first_word = driver.find_element_by_xpath('/html/body/table[7]/tbody/tr[2]/td[2]/a')
        first_word.click()

        wait.until(EC.title_contains('Trademark Electronic Search System (TESS)'))
        html = driver.page_source
        tree = etree.HTML(html)
        tr_list = tree.xpath('/html/body/table[5]/tbody/tr')
        process_result(tr_list)

    except NoSuchElementException:
        # process only one result and zero result
        print('NoSuchElementException!!!')
        is_error_title = driver.title
        print('is_error_title -->', is_error_title)
        if is_error_title == "TESS -- Error" or "":
            print('congratulation! the brand is not in database')
        else:
            html = driver.page_source
            tree = etree.HTML(html)
            tr_list = tree.xpath('/html/body/table[4]/tbody/tr')
            process_result(tr_list)

    # quit the chrome driver
    driver.quit()


def process_result(tr_list):
    content = {}
    for tr in tr_list:
        # string = tr.xpath('string(.)') --> return string
        string_list = tr.xpath('string(.)').split('\n')
        clean_string_list = [i for i in string_list if i and i != ' ']
        print('clean_string_list -->', clean_string_list)
        key = clean_string_list[0].strip()
        if len(clean_string_list) == 2:
            value = clean_string_list[-1].strip()
        elif len(clean_string_list) > 2:
            value = ''.join([j for j in clean_string_list[1:]]).strip()
        else:
            value = ""
        content[key] = value
        print('content -->', content)
        print('-' * 50)
    owner_item = content.get('Owner', '')
    if 'CHINA' in owner_item:
        content['is_china_brand'] = 1
    else:
        content['is_china_brand'] = 0

    save_result(content)


def save_result(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        lines = json.dumps(content, ensure_ascii=False) + '\n'
        f.write(lines)
        print('\033[36;1msave result success-->\033[0m', lines)
        f.close()


def demo(chrome_options=None):
    driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)

    driver.get('http://httpbin.org/get?show_env=1')
    driver.set_page_load_timeout(10)
    # driver.get('https://www.httpbin.org/ip')
    html = driver.page_source
    print(html)
    driver.quit()


def main():
    # keywords = ['iphone', 'hotapei', 'nitama']
    keywords = ['iphone']
    for keyword in keywords:
        try:
            print('\033[32;1mscraping keyword --> {}\033[0m'.format(keyword))
            chrome_options = set_chrome_option()
            execute(keyword, chrome_options=chrome_options)
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    main()

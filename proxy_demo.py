# -*- coding:utf-8 -*-
# -*- author:cto_b -*-
from selenium import webdriver
import os
import time

"""
test selenium how to set proxy
"""

"""
# 【tips】
# 1. proxy ip stable ip, not rotation ip
# 2. proxy ip speed is slow
# 3. computer memory --> demand large memory
# 4. browser.quit() --> clear browser cache
"""


# selenium proxy chrome version


path = r"E:\Developer Tools\driver\chromedriver.exe"

start1_time = time.time()
chrome_options = webdriver.ChromeOptions()

# set headless model
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')
chrome_options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1')
prefs = {
    'profile.default_content_setting_values': {
        'images': 2
    }
}
chrome_options.add_experimental_option('prefs', prefs)

proxy = 'http://104.245.96.105:19012'
chrome_options.add_argument('--proxy-server=%s' % proxy)
driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

driver.get('http://httpbin.org/get?show_env=1')
# driver.get('https://www.httpbin.org/ip')
html = driver.page_source
print(html)

# driver.get_screenshot_as_file('demo.png')
driver.quit()
end_time = time.time() - start1_time
print('chrome headless use time is -->{}'.format(end_time))
# only headless chrome could use proxy about time 7.8
# set permissions image
print('-'*50)


# selenium proxy firefox version
# ==============================
"""
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver import FirefoxOptions

start2_time = time.time()

firefox_options = FirefoxOptions()
firefox_options.set_headless()
firefox_options.add_argument('--disable-gpu')
firefox_options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"')


firefox_path = r"E:\Developer Tools\driver\geckodriver.exe"
profile = FirefoxProfile()
# 激活手动代理配置（对应着在 profile（配置文件）中设置首选项）
profile.set_preference("network.proxy.type", 1)
# ip及其端口号配置为 http 协议代理
profile.set_preference("network.proxy.http", "104.245.96.105")
profile.set_preference("network.proxy.http_port", 19012)
profile.set_preference('permissions.default.image', 2)

# 所有协议共用一种 ip 及端口，如果单独配置，不必设置该项，因为其默认为 False
# profile.set_preference("network.proxy.share_proxy_settings", True)

# 默认本地地址（localhost）不使用代理，如果有些域名在访问时不想使用代理可以使用类似下面的参数设置
# profile.set_preference("network.proxy.no_proxies_on", "localhost")

# 以代理方式启动 firefox
firefox = webdriver.Firefox(profile, options=firefox_options, executable_path=firefox_path)
firefox.get('http://httpbin.org/get')
firefox.set_page_load_timeout(20)
html = firefox.page_source
print(html)

firefox.quit()
end2_time = time.time() - start2_time

print('firefox use time is -->{}'.format(end2_time))
# have windows about time 7.98s
# firefox headless about time 6.8s
"""
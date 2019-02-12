# -*- coding: utf-8 -*-
import sys, time, glob, configparser
import util
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from xvfbwrapper import Xvfb
import time
import json

# HTML保存
def save_html(driver, path, ini):
    print("function:{0} start".format(sys._getframe().f_code.co_name))
    try:
        # HTML保存
        html_path = path + ini.get("html", "folder")
        util.mkdir(html_path)
        util.write(driver.page_source, ini.get("html", "file"), html_path)
        # util.download(url, html_path)
    except:
        print("Unexpected error:", sys.exc_info()[0])
    print("function:{0} end".format(sys._getframe().f_code.co_name))

# 画像収集
def save_image(driver, device, path, ini, add_dir = ""):
    print("function:{0} start".format(sys._getframe().f_code.co_name))
    # イメージリスト作成 
    try:
        if device == "PC":
            imgs_path = path + ini.get("image", "folder")
        elif device == "Mobile":
            imgs_path = path + ini.get("image", "folder")
        else:
            print (ini.get("message", "DEVICE_REQUIRE"))
            sys.exit()

        if len(add_dir) != 0:
            imgs_path = imgs_path + add_dir + "/"

        util.mkdir(imgs_path)
        text = "";
        element_list = driver.find_elements_by_tag_name("img")
        for i in  element_list:
            title = ""
            try:
                img_src = i.get_attribute("src")
                title = util.download(img_src, imgs_path);
                width = i.get_attribute("width")
                height = i.get_attribute("height")

                # TODO get_attributeできない場合エラーとなるので後々なおす 高横はstyleから取得できないか
                if len(title) != 0:
                    text = text + "title:{0} src:{1} width:{2} height:{3}".format(title, img_src, width, height) + "\n";
            except:
                # print("Unexpected error:", sys.exc_info()[0])
                print("")
        util.write(text, ini.get("image", "listname"), imgs_path)
    except:
        print("Unexpected error:", sys.exc_info()[0])

    print("function:{0} end".format(sys._getframe().f_code.co_name))

# キャプチャ
def save_capture(driver, url, savename, path, ini, add_dir = ""):
    print("function:{0} start".format(sys._getframe().f_code.co_name))
    try:
        cappath = path + ini.get("capture", "folder")

        if len(add_dir) != "":
            cappath = cappath + add_dir + "/"

        util.mkdir(cappath)
        # driver.save_screenshot(cappath + savename + "_default.png")
        util.fullpage_screenshot(driver, cappath + savename + "_full.png")
        # window_fullsize_screenshot(driver, url, cappath + savename + "_default_full.png")
    except WebDriverException as w: 
        print ("WebDriverException {0},{1}".format(sys.exc_info()[0],w.strerror))
    except:
        print("Unexpected error:", sys.exc_info()[0])

    print("function:{0} end".format(sys._getframe().f_code.co_name))

# アラート制御
def switch_to_alert(driver, ini):
    print("function:{0} start".format(sys._getframe().f_code.co_name))
    try:
        alert = driver.switch_to_alert()
        alert.accept()
    except:
        print (ini.get("message", "ALERT_ACCEPT"))
    print("function:{0} end".format(sys._getframe().f_code.co_name))

# ページ情報の取得
def get_page_info(driver, path):
    print("function:{0} start".format(sys._getframe().f_code.co_name))
    try:
        info = {}
        info['title'] = driver.title
        info['url'] = driver.current_url

        element_list = driver.find_elements_by_css_selector("meta[name='description']")
        for i in  element_list:
            if len(i.get_attribute("content")) != 0:
                info['description'] = i.get_attribute("content")
                break

        element_list = driver.find_elements_by_css_selector("meta[name='keywords']")
        for i in  element_list:
            if len(i.get_attribute("content")) != 0:
                info['keywords'] = i.get_attribute("content")
                break
    except:
        print("Unexpected error:", sys.exc_info()[0])

    util.write(info, ini.get("html", "info"), path)

    print("function:{0} end".format(sys._getframe().f_code.co_name))
    return info

# ブラウザ生成
def window_init(url, device):
    print("function:{0} start".format(sys._getframe().f_code.co_name))
    ini = configparser.SafeConfigParser();
    ini.read('config.ini')

    if device == "PC":
        userAgent = ini.get("capture", "useragent.pc")
        displaySize = ini.get("capture", "windowsize.pc")
    elif device == "Mobile":
        userAgent = ini.get("capture", "useragent.mobile")
        displaySize = ini.get("capture", "windowsize.mobile")
    else:
        print ("Device require \"PC\" or \"Mobile\"")
        sys.exit()

    driverPath = ini.get("capture", "chromedriver")

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--lang=ja")
    chrome_options.add_argument("--user-agent=" + userAgent)
    chrome_options.add_argument("--window-size=" + displaySize)

    if device == "Mobile":
        window_size_list = displaySize.split(",")
        mobile_emulation = {"deviceMetrics": { "width": int(window_size_list[0]), "height": int(window_size_list[1]), "pixelRatio": 3.0 }}
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome(driverPath, chrome_options=chrome_options)
    driver.get(url)
    print("function:{0} end".format(sys._getframe().f_code.co_name))
    return driver

# アンカー一覧情報を取得
def get_anchor_url(path, ini):
    print("function:{0} start".format(sys._getframe().f_code.co_name))
    try:
        urls = []
        path = path + ini.get("pageurl", "listname")
        with open(path, 'r') as f:
            for line in f:
                urls.append(line)
        return urls
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return {};

if __name__ == "__main__":
    start = time.time()
    param = sys.argv

    ini = configparser.SafeConfigParser();
    ini.read('config.ini')

    if len(param) != 3:
        print (ini.get("message", "PARAM_ERROR"))
        sys.exit()

    path = param[1]
    device = param[2]
    savename = 'screen'

    if device == "PC":
        print("device:PC")
    elif device == "Mobile":
        print("devide:Mobile")
    else:
        print (ini.get("message", "DEVICE_REQUIRE"))
        sys.exit()

    vdi = Xvfb()
    vdi.start()

    try:
        path = path + ini.get("pageurl", "folder")
        # アンカーURL一覧を取得
        urls = get_anchor_url(path, ini)
        if len(urls) <= 0:
            sys.exit()
        counter = 0
        for url in urls:

            try:
                url = url.replace('href:', '')

                counter_dir = path + str(counter) + "/"
                util.mkdir(counter_dir)
                print(url)
                newdriver = window_init(url, device)
                time.sleep(10)
                info = get_page_info(newdriver, counter_dir)
                switch_to_alert(newdriver, ini)

                save_capture(newdriver, url, savename, counter_dir, ini)
                
                save_image(newdriver, device, counter_dir, ini)
                
                save_html(newdriver, counter_dir, ini)
            except:
                print("Unexpected error:", sys.exc_info()[0])

            if 'newdriver' in locals():
                newdriver.quit()
            counter = counter + 1

    except WebDriverException as e:
        print ("WebDriverException {0},{1}".format(sys.exc_info()[0], e.strerror))
    except:
        print("Unexpected error:", sys.exc_info()[0])

    if 'driver' in locals():
        driver.quit()
    if 'vdi' in locals():
        vdi.stop()

    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

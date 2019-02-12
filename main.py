# -*- coding: utf-8 -*-
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from xvfbwrapper import Xvfb
import sys, time, glob, configparser
import util
import time
import subprocess

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

# アンカー取得
def save_url(driver, url, device, savename, path, ini):
    print("function:{0} start".format(sys._getframe().f_code.co_name))
    try:
        # アンカーURL取得
        if device == "PC":
            pageurl_path = path + ini.get("pageurl", "folder")
        elif device == "Mobile":
            pageurl_path = path + ini.get("pageurl", "folder")
        else:
            print (ini.get("message", "DEVICE_REQUIRE"))
            sys.exit()

        util.mkdir(pageurl_path)
        text = ""
        element_list = driver.find_elements_by_tag_name("a")
        li_uniq = list(set(element_list)) # 重複除去
        counter = 0
        for i in  li_uniq:
            try:
                href = i.get_attribute("href")
                if len(href) == 0:
                    continue

                text = text + "href:{0}".format(href) + "\n";
                # newdriver = window_init(href, device)
                # time.sleep(10)
                # info = get_page_info(newdriver)
                # print(info)
                # switch_to_alert(newdriver, ini)
                # save_href_capture(newdriver, href, savename, path, ini , str(counter))
                # save_href_image(newdriver, device, path, ini, str(counter))

                pageurl_counter_path = pageurl_path + str(counter) + "/"
                util.mkdir(pageurl_counter_path)
                util.write(href, ini.get("pageurl", "listname"), pageurl_counter_path)

                counter = counter + 1
                # newdriver.close()
            except:
                counter = counter + 1
                # newdriver.close()

        util.write(text, ini.get("pageurl", "listname"), pageurl_path)
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
                # width = i.get_attribute("width")
                # height = i.get_attribute("height")

                # TODO get_attributeできない場合エラーとなるので後々なおす 高横はstyleから取得できないか
                if len(title) != 0:
                    text = text + "title:{0} src:{1}".format(title, img_src) + "\n";
            except:
                print("Unexpected error:", sys.exc_info()[0])
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

# 要素スクリーンショット
def window_selector_screenshot(driver, selector, savename):
    print("function:{0} start".format(sys._getframe().f_code.co_name))

    element_list = driver.find_elements_by_css_selector(selector)
    for i in  element_list:
        if len(i.get_attribute("content")) != 0:
            break

    driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
    driver.save_screenshot(savename)

    print("function:{0} end".format(sys._getframe().f_code.co_name))

# ウィンドウサイズフルスクリーンショット
def window_fullsize_screenshot(driver, url, savename):
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

    # ページのサイズ取得
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")

    print("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))

    # ページサイズにウィンドウサイズを変更
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--lang=ja")
    chrome_options.add_argument("--user-agent=" + userAgent)
    chrome_options.add_argument("--window-size={0},{1}".format(total_width,total_height))

    # 新しく生成
    driver = webdriver.Chrome(driverPath, chrome_options=chrome_options)

    driver.get(url)
    time.sleep(10)
    driver.save_screenshot(savename)
    driver.close()

    print("function:{0} end".format(sys._getframe().f_code.co_name))

if __name__ == "__main__":
    start = time.time()
    param = sys.argv

    ini = configparser.SafeConfigParser();
    ini.read('config.ini')

    if len(param) != 5:
        print (ini.get("message", "PARAM_ERROR"))
        sys.exit()

    url = param[1]
    path = param[2]
    savename = param[3]
    device = param[4]

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

        driver = window_init(url, device)
        info = get_page_info(driver, path)
        time.sleep(10)
        switch_to_alert(driver, ini)

        save_capture(driver, url, savename, path, ini)

        save_image(driver, device, path, ini)

        save_url(driver, url, device, savename, path, ini)

        save_html(driver, path, ini)

    except WebDriverException as e:
        print ("WebDriverException {0},{1}".format(sys.exc_info()[0],e.strerror))
    except:
        print("Unexpected error:", sys.exc_info()[0])

    if 'driver' in locals():
        driver.quit()
    if 'vdi' in locals():
        vdi.stop()

    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

    # アンカーURLのデータを収集
    cmd = "python anchor.py {0} PC".format(path)
    print(cmd)
    returncode = subprocess.call(cmd, shell=True)

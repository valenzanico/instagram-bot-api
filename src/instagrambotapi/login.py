import time
import keyboard
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from numpy.random import default_rng
from .time_util import sleep as r_sleep
random = default_rng()
#"D:\myapp\cassinelli\dir-spam-bot\client1\dist\FirefoxPortable\App\Firefox64\firefox.exe"
#"D:\myapp\cassinelli\dir-spam-bot\client1\dist\webdriver\geckodriver.exe"
def random_sleep(min: float, max: float):
        wait_time = random.uniform(float(min), float(max))
        r_sleep(wait_time)
        #print("wait " + str(wait_time))

def insert_text_action(text, text_entry, driver):
    try:
        (ActionChains(driver)
        .move_to_element(text_entry)
        .click(text_entry)
        .send_keys(text)
        .perform()
        )
        return True
    except Exception as error:
        print("error in insert text with action chains")
        print(str(error))
        return False

def login_v1(username, password, headless=True, path={"browser": None, "driver": None}, proxy=None):
    print("start login")
    profile = webdriver.FirefoxProfile()
    # authorize notificatrion
    profile.set_preference('permissions.default.desktop-notification', 1)
    myoptions = Options()
    myoptions.headless = headless  # activate headless mode
    if proxy:
        myproxy_http = proxy["proxy"] + ":" + str(proxy["port_http"])
        myproxy_socks = proxy["proxy"] + ":" + str(proxy["port_socks"])
        firefox_capabilities =  webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities["marionette"] = True

        firefox_capabilities["proxy"] = {
            'proxyType': "MANUAL",
            'httpProxy': myproxy_http,
            'sslProxy': myproxy_http,
            'socksProxy': myproxy_socks,
            'socksVersion': 5
        }
    else:
        firefox_capabilities = None

     # open browser
    if path["browser"]!= None and path["driver"] !=None:
        driver = webdriver.Firefox(executable_path=path["driver"],
        options=myoptions, firefox_profile=profile, firefox_binary=path["browser"],
        capabilities=firefox_capabilities
        ) 
    else:
        driver = webdriver.Firefox(
        options=myoptions, firefox_profile=profile, capabilities=firefox_capabilities) 
    
    if proxy:
        #login to proxy
        driver.get("https://tools.keycdn.com/geo")
        time.sleep(5)
        proxyauth = driver.switch_to.alert
        keyboard.write(proxy["username"])
        time.sleep(1)
        keyboard.press_and_release("tab")
        time.sleep(1)
        keyboard.write(proxy["password"])
        time.sleep(1)
        proxyauth.accept()
        time.sleep(5)
        # time.sleep(5)
        # proxyauth = driver.switch_to.alert
        # time.sleep(1)
        # proxyauth.send_keys(proxy["username"] + Keys.TAB + proxy["password"])

        # time.sleep(3)
        # print(proxyauth.text)
        # time.sleep(4)
        # proxyauth.accept()
        


    driver.get("https://instagram.com")
    time.sleep(1)
    driver.execute_script('''

    document.querySelector("body > div.RnEpo.Yx5HN._4Yzd2 > div > div > button.aOOlW.bIiDR").click()
    ''')# accept cookies  
    random_sleep(3, 7)
    try:
        username_inp = driver.find_element_by_xpath(
        "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")#insert username
        insert_text_action(username, username_inp, driver)
        # for character in username:
        #     username_inp.send_keys(character)
        #     random_sleep(0.05, 0.3)
    except:
        username_inp = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")#insert username
        insert_text_action(username, username_inp, driver)
        # for character in username:
        #     username_inp.send_keys(character)
        #     random_sleep(0.05, 0.3)

    random_sleep(3, 6)
    try:
        password_inp = driver.find_element_by_xpath(
        "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")#insert password
        # for character in password:
        #     password_inp.send_keys(character)
        #     random_sleep(0.05, 0.3)
        insert_text_action(password, password_inp, driver)

    except:
        password_inp = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")#insert password
        # for character in password:
        #     password_inp.send_keys(character)
        #     random_sleep(0.05, 0.3)
        insert_text_action(password, password_inp, driver)
    
    random_sleep(2, 4)
    driver.execute_script(
        '''document.querySelector("#loginForm > div > div:nth-child(3) > button").click()''')#submit credentials
    
    random_sleep(7, 8)
    try:#se trova il rpompt che chiede di salvare le credenziali lo accetta
        driver.execute_script(
'''document.querySelector("#react-root > section > main > div > div > div > section > div > button").click()''')#save credentials
    except Exception as error:
        print("message not found")
    print("login finish")
    random_sleep(7, 8)
    try:
        for cookie in driver.get_cookies():#get session id from cookie
            if cookie["name"] == "sessionid":
                sessionid = cookie["value"]
                break
    except Exception as error:
        print("problem in get session id")
        print(error)
        sessionid = None
    return {"driver": driver, "sessionid": sessionid}

def loginv2(username, password, headless=True, path={"browser": None, "driver": None}, proxy=None):
    print("start login")
    profile = webdriver.FirefoxProfile()
    # authorize notificatrion
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1")
    profile.set_preference('permissions.default.desktop-notification', 1)
    myoptions = Options()
    myoptions.headless = headless  # activate headless mode
    myoptions.add_argument("--width=390")
    myoptions.add_argument("--height=844")
    if proxy:
        myproxy_http = proxy["proxy"] + ":" + str(proxy["port_http"])
        myproxy_socks = proxy["proxy"] + ":" + str(proxy["port_socks"])
        firefox_capabilities =  webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities["marionette"] = True

        firefox_capabilities["proxy"] = {
            'proxyType': "MANUAL",
            'httpProxy': myproxy_http,
            'sslProxy': myproxy_http,
            'socksProxy': myproxy_socks,
            'socksVersion': 5
        }
    else:
        firefox_capabilities = None

     # open browser
    if path["browser"]!= None and path["driver"] !=None:
        driver = webdriver.Firefox(executable_path=path["driver"],
        options=myoptions, firefox_profile=profile, firefox_binary=path["browser"],
        capabilities=firefox_capabilities
        ) 
    else:
        driver = webdriver.Firefox(
        options=myoptions, firefox_profile=profile, capabilities=firefox_capabilities) 
    
    if proxy:
        #login to proxy
        driver.get("https://tools.keycdn.com/geo")
        time.sleep(5)
        proxyauth = driver.switch_to.alert
        keyboard.write(proxy["username"])
        time.sleep(1)
        keyboard.press_and_release("tab")
        time.sleep(1)
        keyboard.write(proxy["password"])
        time.sleep(1)
        proxyauth.accept()
        time.sleep(5)
        # time.sleep(5)
        # proxyauth = driver.switch_to.alert
        # time.sleep(1)
        # proxyauth.send_keys(proxy["username"] + Keys.TAB + proxy["password"])

        # time.sleep(3)
        # print(proxyauth.text)
        # time.sleep(4)
        # proxyauth.accept()
        


    driver.get("https://instagram.com")
    time.sleep(1)
    driver.execute_script('''

    document.querySelector("body > div.RnEpo.Yx5HN._4Yzd2 > div > div > button.aOOlW.bIiDR").click()
    ''')# accept cookies  
    random_sleep(3, 7)
    driver.execute_script('''
    document.querySelector("#react-root > section > main > article > div > div > div > div.AC7dP.Igw0E.IwRSH.pmxbr.eGOV_._4EzTm.gKUEf > button:nth-child(1)").click()
    ''')
    random_sleep(3, 7)
    try:
        username_inp = driver.find_element_by_xpath(
        "/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[3]/div/label/input")#insert username
        insert_text_action(username, username_inp, driver)
        # for character in username:
        #     username_inp.send_keys(character)
        #     random_sleep(0.05, 0.3)
    except Exception as error:
        print(str(error))
        

    random_sleep(3, 6)
    try:
        password_inp = driver.find_element_by_xpath(
        "/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[4]/div/label/input")#insert password
        # for character in password:
        #     password_inp.send_keys(character)
        #     random_sleep(0.05, 0.3)
        insert_text_action(password, password_inp, driver)

    except Exception as error:
        print(str(error))
    
    random_sleep(2, 4)
    driver.execute_script(
        '''document.querySelector("#loginForm > div.Igw0E.IwRSH.eGOV_._4EzTm.kEKum > div:nth-child(6) > button").click()''')#submit credentials
    
    random_sleep(7, 8)
    try:#se trova il rpompt che chiede di salvare le credenziali lo accetta
        driver.execute_script(
'''document.querySelector("#react-root > section > main > div > div > section > div > button").click()''')#save credentials
    except Exception as error:
        print("message not found")
    random_sleep(5, 6)
    try:
        driver.execute_script('''
        document.querySelector("body > div.RnEpo.xpORG._9Mt7n > div > div.YkJYY > div > div:nth-child(5) > button").click()
'''
        )
    except Exception as error:
        print("message not found")
    print("login finish")
    random_sleep(7, 8)
    try:
        for cookie in driver.get_cookies():#get session id from cookie
            if cookie["name"] == "sessionid":
                sessionid = cookie["value"]
                break
    except Exception as error:
        print("problem in get session id")
        print(error)
        sessionid = None
    return {"driver": driver, "sessionid": sessionid}

def login(username, password, headless=True, path={"browser": None, "driver": None}, proxy=None):
    print("start login")
    profile = webdriver.FirefoxProfile()
    # authorize notificatrion
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1")
    profile.set_preference('permissions.default.desktop-notification', 1)
    myoptions = Options()
    myoptions.headless = headless  # activate headless mode
    myoptions.add_argument("--width=390")
    myoptions.add_argument("--height=844")
    seleniumwireopt = None
    if proxy != None:
        seleniumwireopt = {}
        seleniumwireopt["proxy"] = {}
        proxy_opt = seleniumwireopt["proxy"]
        proxy_ip = proxy["proxy"]
        proxy_port = str(proxy["port_http"])
        if proxy["username"] and proxy["password"]:
            proxy_username = proxy["username"]
            proxy_password = proxy["password"]
            print(f"http://{proxy_username}:{proxy_password}@{proxy_ip}:{proxy_port}")
            proxy_opt["http"] = f"http://{proxy_username}:{proxy_password}@{proxy_ip}:{proxy_port}"
            proxy_opt["https"] = f"https://{proxy_username}:{proxy_password}@{proxy_ip}:{proxy_port}"
        else:
            proxy_opt["http"] = f"http://{proxy_ip}:{proxy_port}"
            print(f"http://{proxy_ip}:{proxy_port}")
            proxy_opt["https"] = f"https://{proxy_ip}:{proxy_port}"


     # open browser
    if path["browser"]!= None and path["driver"] !=None:
        driver = webdriver.Firefox(
            executable_path=path["driver"],
            options=myoptions,
            firefox_profile=profile,
            firefox_binary=path["browser"],
            seleniumwire_options=seleniumwireopt) 
    else:
        driver = webdriver.Firefox(
        options=myoptions,
        firefox_profile=profile,
        seleniumwire_options=seleniumwireopt) 
    
    if proxy:
        driver.set_page_load_timeout(20)
        driver.get("https://tools.keycdn.com/geo")
        print("sto controllando se il proxy funziona...")
        time.sleep(2)


    driver.get("https://instagram.com")
    random_sleep(1, 2)
    driver.execute_script('''

    document.querySelector("body > div:nth-child(2) > div > div > div > div:nth-child(4) > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe.x5yr21d.x19onx9a > div > div._ab8w._ab94._ab99._ab9f._ab9m._ab9p._abam._abc0._abcm > div._ab8w._ab94._ab99._ab9f._ab9m._ab9p._abb2._abbk._abcm > button").click()
    ''')# accept cookies  
    random_sleep(1, 4)
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div/div/div[2]/div[3]/button[1]" )
    random_sleep(1, 4)
    try:
        username_inp = driver.find_element_by_xpath(
        "/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[3]/div/label/input")#insert username
        insert_text_action(username, username_inp, driver)
        # for character in username:
        #     username_inp.send_keys(character)
        #     random_sleep(0.05, 0.3)
    except Exception as error:
        print(str(error))
        

    random_sleep(1, 3)
    try:
        password_inp = driver.find_element_by_xpath(
        "/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[4]/div/label/input")#insert password
        # for character in password:
        #     password_inp.send_keys(character)
        #     random_sleep(0.05, 0.3)
        insert_text_action(password, password_inp, driver)

    except Exception as error:
        print(str(error))
    
    random_sleep(1, 2)
    driver.execute_script(
        '''document.querySelector("#loginForm > div.Igw0E.IwRSH.eGOV_._4EzTm.kEKum > div:nth-child(6) > button").click()''')#submit credentials
    
    random_sleep(10, 15)
    try:#se trova il rpompt che chiede di salvare le credenziali lo accetta
        driver.execute_script(
'''document.querySelector("body > div.RnEpo.Yx5HN._4Yzd2 > div > div > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.MGdpg.aGBdT > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm._5VUwz.y2rAt > button").click()''')#save credentials
    except Exception as error:
        print("message not found")
    random_sleep(1, 3)
    try:
        driver.execute_script('''
        document.querySelector("body > div.RnEpo.xpORG._9Mt7n > div > div.YkJYY > div > div:nth-child(5) > button").click()
'''
        )
    except Exception as error:
        print("message not found")
    print("login finish")
    random_sleep(3, 5)
    try:
        for cookie in driver.get_cookies():#get session id from cookie
            if cookie["name"] == "sessionid":
                sessionid = cookie["value"]
                break
    except Exception as error:
        print("problem in get session id")
        print(error)
        sessionid = None
    return {"driver": driver, "sessionid": sessionid}
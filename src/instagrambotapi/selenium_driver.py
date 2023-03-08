from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
import time

#questa classe crea i driver selenium, apre il browser e setta le impostazioni
#le azioni qua sopra descrittte vengono compiute nella funzione init_driver
#la funzione init_drver ritorna il driver selenium


class Driver:
    def __init__(self, headless=True, proxy=None, path={"browser": None, "driver": None}):
        self.headless = headless
        self.proxy = proxy
        self.path = path

    def init_driver(self):
        headless = self.headless
        proxy = self.proxy
        path = self.path

        if self.driver:
            return True
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
            self.execute_action({
                "descrition": "open url ip",
                "command": "get",
                "url":"https://tools.keycdn.com/geo",
                "wait": (2,3),
                "required": False,
            })
            print("sto controllando se il proxy funziona...")
            time.sleep(2)

        self.driver = driver
        return True
    
    def close(self):
        self.driver.quit()
        self.logged = False
        self.scraped_followers = None
        self.driver = None
        return True



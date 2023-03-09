from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

#questa classe contiene le funzioni che si occupano si eseguire il login sul sito di instagram
class Login():

    def __init__(self) -> None:
        super().__init__()

    def login(self, username, password):

        login_commands = [
            {
                # open the login page
                "description": "open login page",
                "command": "get",
                "url": "https://www.instagram.com/accounts/login/",
                "wait": (10,15)
            },
            {
                # Accept instagram login cookies
                "description": "accept cookies",
                "command": "script",
                "script":
                '''
            document.querySelector("body > div:nth-child(2) >  div > div > div:nth-child(4) > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe.x5yr21d.x19onx9a > div > div._ab8w._ab94._ab99._ab9f._ab9m._ab9p._abam._abc0._abcm > div._ab8w._ab94._ab99._ab9f._ab9m._ab9p._abb2._abbk._abcm > button").click()
            ''',
                "wait": (15, 20)
            },
            {
                # inserimento username nel input di testo
                "description": "insert username",
                "command": "write_text",
                "target": (By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div/div/div[2]/form/div[1]/div[3]/div/label/input"),
                "text": username,
                "wait": (1, 3),
            },
            {
                # inserimento password nel input di testo
                "description": "insert password",
                "command": "write_text",
                "target": (By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div/div/div[2]/form/div[1]/div[4]/div/label/input"),
                "text": password,
                "wait": (1, 3)
            },
            {
                "description": "click save information checkbox",
                "command": "click",
                "target": (By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div/div/div[2]/form/div[1]/div[5]/div/label/div[1]"),
                "wait": (1, 3),
                "required": False
            },
            {
                # invio delle credenziali con il pulsante invio
                "description": "ENTER to login",
                "command": "driver_function",
                "function": lambda driver: driver.send_keys(Keys.ENTER),
                "wait": (30, 40)
            },
            {
                # accetta la notifica di salvataggio dei dati di accesso quando la trova
                "description": "accept save login data",
                "command": "click",
                "target": (By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/div/div[2]/section/main/div/div/section/div/button"),
                "wait": (5, 7),
                "required": False
            }
        ]

        for action in login_commands:
            self.execute_action(action)

        self.logged = True

        return True
    def logout(self):
        
        logout_commands = [
            {
            "description": "open instagram site",
            "command": "get",
            "url": "https://www.instagram.com/",
            "wait": (20,23)
        },
        {
            "description": "delete cookies",
            "command": "driver_function",
            "function": lambda driverclass: driverclass.delete_all_cookies(),
            "wait": (1,3)
        },
        {
            "description": "open instagram site",
            "command": "get",
            "url": "https://www.instagram.com/",
            "wait": (15,20)
        },]
        for action in logout_commands:
            self.execute_action(action)
        
        self.logged = False
        return True
        


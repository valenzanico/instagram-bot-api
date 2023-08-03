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
                "wait": (8,13)
            },
            {
                # Accept instagram login cookies
                "description": "accept cookies",
                "command": "click",
                "target":
                (By.XPATH, '''//button[contains(text(), "Consenti tutti i cookie")]'''),
                "wait": (8, 11)
            },
            {
                # inserimento username nel input di testo
                "description": "insert username",
                "command": "write_text",
                "target": (By.XPATH, '''//input[@aria-label = "Numero di telefono, nome utente o e-mail"]'''),
                "text": username,
                "wait": (1, 3),
            },
            {
                # inserimento password nel input di testo
                "description": "insert password",
                "command": "write_text",
                "target": (By.XPATH, '''//input[@aria-label = "Password"]'''),
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
                "function": lambda driver: ActionChains(driver).send_keys(Keys.ENTER).perform(),
                "wait": (20, 25)
            },
            {
                # accetta la notifica di salvataggio dei dati di accesso quando la trova
                "description": "accept save login data",
                "command": "click",
                "target": (By.XPATH, '''//button[contains(text(), "Salva le informazioni")]'''),
                "wait": (5, 7),
                "required": False
            },
            {
                #controlla il login
                "description": "check login",
                "command": "driver_function",
                "function": lambda driver: driver.get_cookie("sessionid"),
                "wait": (3, 4),
            }
        ]

        for action in login_commands:
            self.execute_action(action)

        #check if login was successful
        #if the sessionid cookie is found the login was successful
        #save session cookies in class
        try:
            cookies = self.driver.get_cookies()
            for cookie in cookies:#get session id from cookie
                if cookie["name"] == "sessionid":
                    print("login success")
                    self.logged = True
                    for cookie in cookies:
                        self.session_cookies[cookie["name"]] = cookie["value"]
                    return True

        except Exception as e:
            print(e)
            self.logged = False
            return False
        
        print("login failed")
        print("sessionid not found")
        self.logged = False
        return False
        

        
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
            "description": "open Algorithm-net site",
            "command": "get",
            "url": "https://algorithm-net.com",
            "wait": (5,7)
        },]
        for action in logout_commands:
            self.execute_action(action)
        
        self.logged = False
        return True
        


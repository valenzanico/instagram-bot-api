from string import Template
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
class Senddm:
    def __init__(self):
        super().__init__()

    def send_dm(self, user:str, message:str, check_message=None):
        driver = self.driver
        send_direct_action = [
            {
            #0-Apre la pagina per andare a seguire il ricevente del messaggio
            "description": "open user page",
            "command": "get",
            "url":f"https://www.instagram.com/{user}",
            "wait": (5,6)
        },
          {
            #1-Clicca sul pulsante per seguire il ricevente
            "description": "start follow user",
         "command": "click",
            "target": (By.XPATH, '''//div[contains(text(), "Segui")]'''),
            "wait": (5,7),
            "required": False
         }, 
        # {
        #     #2-Apre la chat dei Direct message con il ricevente
        #     "description": "open DM chat",
        #     "command": "script",
        #     "script": '''document.querySelector("#mount_0_0_BH > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div > div.x78zum5.xdt5ytf.x10cihs4.x1t2pt76.x1n2onr6.x1ja2u2z > div.x9f619.xnz67gz.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.xh8yej3.x1gryazu.x10o80wk.x14k21rp.x1porb0y.x17snn68.x6osk4m > section > main > div > header > section > div._ab8w._ab94._ab99._ab9f._ab9m._ab9p._abcm > div > div._ab8w._ab94._ab99._ab9f._ab9m._ab9o._abb0._ab9s._abcm > div").click()''',
        #     "wait": (5,8)
        # },
        {   #2-Apre la chat dei Direct message con il ricevente
            "description": "Open DM chat",
            "command": "click",
            "target": (By.XPATH, '''//div[contains(text(), "Messaggio")]'''),
            "wait": (8,11)
        },
        # #apre la ricerca del utente a cui inviare i dm
        # {
        #     "description": "open search user",
        #     "command": "click",
        #     "target": (By.XPATH, '''//div[contains(text(), "Invia messaggio")]'''),
        #     "wait": (3,6)
        # },
        # #cerca l'utente a cui inviare i dm
        # {
        #     "description": "search user",
        #     "command": "write_text",
        #     "target": (By.XPATH, '''//input[@placeholder="Cerca..."]'''),
        #     "text": user,
        #     "write_speed": (0.3,0.5),#velocità di scrittura del messaggio
        #     "wait": (3,6)
        # },
        # {
        #     #passa sul utente a cui inviare i dm
        #     "description": "pass on user",
        #     "command": "driver_function",
        #     "function": lambda driver: ActionChains(driver).send_keys(Keys.TAB).perform(),
        #     "wait": (1,3)

        # },
        # {
        #     #conferma il utente a cui inviare i dm
        #     "description": "confirm user",
        #     "command": "driver_function",
        #     "function": lambda driver: ActionChains(driver).send_keys(Keys.ENTER).perform(),
        #     "wait": (1,3)
        # },
        # {
        #     #clicca sul pulsante per aprire la chat dei DM
        #     "description": "click on button that open chat",
        #     "command": "click",
        #     "target": (By.XPATH, '''//div[contains(text(), "Chat")]'''),
        #     "wait": (1,4)
        # },
        
        {
            #3-Scrive il Messaggio nel input dei DM
            "description": "write dm in the chat",
            "command": "write_text",
            "target": (By.XPATH, '''//div[contains(text(), "Scrivi un messaggio...")]'''),
            "text": message,
            "write_speed": (0.1,0.2),#velocità di scrittura del messaggio
            "wait": (2,4)
        },
        {
            #4-clicca sul pulsante di invio e manda il messaggio
            "description": "click on button that dm message",
            "command": "click",
            "target": (By.XPATH, '''//div[contains(text(), "Invia")]'''),
            "wait": (2,6)   
        },
         {
             #5-ritorna alla pagina utente del ricevente per smettere di seguirlo
             "description": "return to user page",
             "command": "get",
             "url":f"https://www.instagram.com/{user}",
             "wait": (5,6),
             "required":False
         },
        # {
        #     #6-clicca sul pulsante di unfollow del ricevente
        #     "description": "click on unfollow button",
        #     "command": "click",
        #  "target": (By.XPATH, '''//div[contains(text(), "Segui già")]'''),
        #      "wait": (4,7),
        #     "required": False
        #  },
        #  {
        #      #7-conferma di voler smettere di seguire il ricevente
        #      "description": "click on confirm unfollow button",
        #      "command": "click",
        #      "target": (By.XPATH, '''//span[contains(text(), "Non seguire più")]'''),
        #      "wait": (4,7),
        #      "required": False
        # }

        ]
        #azione per aprire la chat dei DM
        for action in send_direct_action[:3]:
            self.execute_action(action)
        
        if check_message:#controlla se il messaggio è gia stato mandato nella chat 
            try:
                html_chat = driver.execute_script('''return document.querySelector("#react-root > section > div.IEL5I > div > div > div.Igw0E.IwRSH.hLiUi.vwCYk").innerHTML''')
            except Exception as error:
                print(error)
                html_chat = ""
            if check_message in html_chat:
                return False
        #azione per mandare il messaggio e tornare alla pagina del ricevente
        for action in send_direct_action[3:]:
            self.execute_action(action)

        return True
        

        



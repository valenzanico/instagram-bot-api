from .selenium_driver import Driver
from .login import Login
from .scraper import Scraper
from .senddm import Senddm
from selenium.webdriver.common.action_chains import ActionChains
from numpy.random import default_rng
from .time_util import sleep as r_sleep


class Bot(Driver, Login, Scraper, Senddm):
    def __init__(self,
                headless=True,
                proxy=None,
                path={"browser": None, "driver": None},
                ):
        self.driver = None
        self.logged = False 
        self.scraped_followers = []

        super().__init__(headless, proxy, path)
        if self.init_driver():
            print("Driver initialized")


    def insert_text_action(self, text, text_entry):

        #questa sequenza di azioni selenium inserisce un dato testo in un dato target(text_entry)
        (ActionChains(self.driver)
            .move_to_element(text_entry)
            .click(text_entry)
            .send_keys(text)
            .perform()
            )
        
    
    def random_sleep(self, min: float, max: float):#genera un numero random float tra min e max
        random = default_rng()
        wait_time = random.uniform(float(min), float(max))#random uniforma da numpy
        r_sleep(wait_time)
        #print("wait " + str(wait_time))
 
    
    def execute_action(self, action):

        #questa funzione esegue un azione
        #un azione è un dizionario, l'effetto è descritto nell description 
        #il tipo di azione è identificato dalla ket command
        #ogni azione ha poi degli attributi specifici
        #tutte le azioni possono avere l'attriubuto wait che contiente una tuple con i due tempi da passare a
        #a random_sleep
        #e l'attributo required che di default è segnato su true, se invece viene impostato 
        #su false la funzione non causa un errore in caso di problemi ma ritorna solamente un false
        driver = self.driver
        action_function = None
        command_type = action.get("command")
        print(action.get("description"))
        if command_type == "get":
            action_function = lambda: driver.get(action.get("url"))
        elif command_type == "script":
            action_function = lambda: driver.execute_script(action.get("script"))
        elif command_type == "write_text":
            def action_function():
                text_entry = driver.find_element(*action.get("target"))
                text = action.get("text")
                self.insert_text_action(text, text_entry)
        elif command_type == "driver_function":#questo tipo di azione è usato per eseguire una funzione del driver
            action_function = lambda: action.get("function")(driver)
        elif command_type == "click":
            def action_function():
                target = driver.find_element(*action.get("target"))
                target.click()
        try:
            action_function()
            if action.get("wait"):
                self.random_sleep(*action.get("wait"))
        except Exception as error:
            if action.get("required")==False: 
                print(error)
                return False

            else:
                print(error)
                raise error
            
        return True



            

            
import time
from selenium.common.exceptions import ElementClickInterceptedException



class Bot:
    def __init__(self, message, driver, check=None):
        self.message = message
        self.driver = driver
        self.check = check

    def send_in_dir(self):  # questa funzione manda il messaggio
        driver = self.driver
        time.sleep(3)
        if self.check:#check if message is sent in past
            html_chat = driver.execute_script('''return (document.querySelector("#react-root > section > div > div.Igw0E.IwRSH.eGOV_._4EzTm > div > div > div.DPiy6.Igw0E.IwRSH.eGOV_.vwCYk > div.uueGX > div > div.Igw0E.IwRSH.hLiUi.vwCYk > div").innerHTML)''')
            if self.check in html_chat:
                return "send-past"
        time.sleep(0.3)
        messagelabel = driver.find_element_by_xpath(
            "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
        # selezione label di inseriemto e inserimeto del testo
        messagelabel.send_keys(self.message)
        send_button = driver.find_element_by_xpath(
            "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button")  # selezione pulsante per invio
        send_button.click()  # click sul pulsante
        return "send"

    def send(self, passed_user):
        driver = self.driver
        user = passed_user  # ricevenet
        # apertura profilo ricevente
        driver.get(f"https://www.instagram.com/{user}")

        time.sleep(1)
        driver.execute_script(
                '''document.querySelector("#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm > div > div > div > span > span.vBF20._1OSdk > button").click()''')
        '''selezione pulsante con javascript e iscrizione al utente'''
        time.sleep(2)
        driver.execute_script(
            '''document.querySelector("#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm > div > div._862NM > div > button").click()''')
        try:
            message_status = self.send_in_dir()  # manda il messaggio
        except ElementClickInterceptedException:
            time.sleep(5)
            self.send_in_dir()
        time.sleep(1)
        # ritorna allla pagina del ricevente
        driver.get(f"https://www.instagram.com/{user}")
        time.sleep(1)
        try:
            driver.execute_script(
                '''document.querySelector("#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm > div > div:nth-child(2) > div > span > span.vBF20._1OSdk > button").click()''')
            time.sleep(0.3)
            driver.execute_script(
                '''document.querySelector("body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.-Cab_").click()''')
            '''esecuzuione script javascript che si disiscrive dal utente'''
            time.sleep(3)
        except Exception as errror:
            print(errror)
        return message_status
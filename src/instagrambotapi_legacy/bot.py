"""classe principale del bot"""
from .time_util import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from numpy.random import default_rng
import os
#TO DO cambiare il random al random di numpy

class Bot:
    def __init__(self, message, driver,v=2,  check=None):
        self.random = default_rng()
        self.message = message
        self.driver = driver
        self.check = check
        if v != 1 and v != 2 and v != 3:
            v = 2
        self.bot_version = v
        
    def update(self):
        print("update v01")
    
    def insert_text_action(self, text, text_entry):
        try:
            (ActionChains(self.driver)
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

    def insert_text_cp(self, text, input):
        try:
            os.system("echo " + text.strip() + " | clip")
            input.send_keys(Keys.CONTROL, "v")
            return True
        except Exception as error:
            print("error in insert text with copy paste")
            print(str(error))
            return False
    #TO DO cambiare il random al random di numpy
    def random_sleep(self, min: float, max: float):#questa funzione uando random aspetta un tempo random tra quelli forniti 
        wait_time = self.random.uniform(float(min), float(max))
        sleep(wait_time)
        #print("wait " + str(wait_time))
    

    def send(self, passed_user=None, passed_users=None):#questa funzione apre la chat e manda il messaggio
        #ci sono tre tipi di modi per aprire la chat
        if self.bot_version == 1 and passed_user != None:
            try:
                get_chat = self.send_with_account_follow(passed_user)
                if get_chat == True:
                    print("open chat")
                    pass
                elif get_chat == "timeout":
                    return "timeout"
                else:
                    return "error"
            except Exception as error:
                print("follow error")
                print(str(error))
                return "error"
        elif self.bot_version == 2 and passed_user != None:
            try:
                get_chat = self.get_dir_chat(passed_user)
                if get_chat:
                    print("open chat")
                    pass
                else:
                    return "error"
            except Exception as error:
                print("get_chat error")
                print(str(error))
                return "error"
        elif self.bot_version == 3 and passed_users != None:
            print(passed_users)
            try:
                get_chat = self.create_group(passed_users)
                if get_chat:
                    print("open chat")
                    pass
                else:
                    return "error"
            except Exception as error:
                print("create group error")
                print(str(error))
                return "error"
        else:
            print(self.bot_version)
            print(passed_users)
            print("wrong bot version")
            return "error"

        try:
            send_status = self.send_in_dir()#manda il messaggio nei direct
            if send_status == "send" and self.bot_version !=1:
                return "send"
            elif send_status == "send-past" and self.bot_version !=1:
                return "send-past"
            elif self.bot_version ==1:
                pass
            else:
                print("problem in send_in_dir")
                if send_status:
                    print(str(send_status))
                return "error"
        except Exception as error:
            print("send_in_dir error")
            print(str(error))
            return "error"

        if self.bot_version == 1 and passed_user != None:#se è stato usato il metodo follow e unfollow si discrive dall'utente
            try:
                unfollow = self.send_with_account_unfollow(passed_user)
                if unfollow == True:
                    return "send"
                elif unfollow == "timeout":
                    return "timeout"
                else:
                    return "error-unfollow"
            except Exception as error:
                print("unfollow error")
                print(str(error))
                return "error-unfollow"

    def send_with_account_follow(self, passed_user):
        driver = self.driver
        user = passed_user  # ricevenet
        # apertura profilo ricevente
        try:
            driver.get(f"https://www.instagram.com/{user}")
        except TimeoutException:
            return "timeout"
        except Exception as error:
            print(str(error))
            return False

        self.random_sleep(2, 4)
        try:
            driver.execute_script('''document.querySelector("#react-root > section > main > div > header > section > div.Igw0E.IwRSH.eGOV_._4EzTm > div > div > button").click()''')
        except Exception:
            try:
                btn_follow = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button")
                btn_follow.click()
            except Exception:
                try:
                    btn_follow = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]/div/div/div/span/span[1]/button")
                    btn_follow.click()
                except Exception as error:
                    print(str(error))
                    return False
        '''selezione pulsante con javascript e iscrizione al utente'''
        self.random_sleep(3, 6)
        try:
            driver.execute_script(#apertura direct
            '''document.querySelector("#react-root > section > main > div > header > section > div.Igw0E.IwRSH.eGOV_._4EzTm > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > button").click()''')
        except Exception as error:
            print(str(error))
            return False
        return True
        
    def send_in_dir(self):  # questa funzione manda il messaggio
        driver = self.driver
        self.random_sleep(3, 4)
        try:
            if self.check:#check if message is sent in past
                html_chat = driver.execute_script('''return document.querySelector("#react-root > section > div.IEL5I > div > div > div.Igw0E.IwRSH.hLiUi.vwCYk").innerHTML''')
                if self.check in html_chat:
                    return "send-past"
        
        except Exception as error:
            print("error in check")
            print(error)
            pass
        self.random_sleep(1, 2)
        try:
            messagelabel = driver.find_element_by_xpath(
            "/html/body/div[1]/section/div[2]/div/div/div[2]/div/div/div/textarea")
        except Exception as error:
            print("error in select message input")
            print(str(error))
            return error

        # selezione label di inseriemto e inserimeto del testo
        self.random_sleep(0.5, 2)
        self.insert_text_action(self.message, messagelabel)
        # for character in self.message:
        #     try:
        #         messagelabel.send_keys(character)
        #     except Exception as error:
        #         print("insert message error")
        #         print(str(error))
        #         return error
        #     self.random_sleep(0.05, 0.2)
        self.random_sleep(1, 2)
        try:
            send_button = driver.find_element_by_xpath(
            "/html/body/div[1]/section/div[2]/div/div/div[2]/div/div/div[2]/button")  # selezione pulsante per invio
            send_button.click()  # click sul pulsante
            print("send direct")
        except Exception as error:
            print("send message error")
            print(str(error))
            return error
        return "send"  

    def send_with_account_unfollow(self, passed_user):
        driver =  self.driver
        user = passed_user
        self.random_sleep(3, 5)
        # ritorna allla pagina del ricevente
        driver.get(f"https://www.instagram.com/{user}")
        self.random_sleep(3, 5)
        try:
            driver.execute_script(
                '''document.querySelector("#react-root > section > main > div > header > section > div.Igw0E.IwRSH.eGOV_._4EzTm > div > div.Igw0E.IwRSH.eGOV_._4EzTm.soMvl > div > span > span.vBF20._1OSdk > button").click()''')
            self.random_sleep(2, 4)
            driver.execute_script(
                '''document.querySelector("body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.-Cab_").click()''')
            '''esecuzuione script javascript che si disiscrive dal utente'''
        except Exception as errror:
            print(errror)
            return False
        return True





 







       
      #old version without mobile

    def send_in_dir_old(self):  # questa funzione manda il messaggio
        driver = self.driver
        self.random_sleep(3, 5)
        try:
            if self.check:#check if message is sent in past
                html_chat = driver.execute_script('''return (document.querySelector("#react-root > section > div > div.Igw0E.IwRSH.eGOV_._4EzTm > div > div > div.DPiy6.Igw0E.IwRSH.eGOV_.vwCYk > div.uueGX > div > div.Igw0E.IwRSH.hLiUi.vwCYk > div").innerHTML)''')
                if self.check in html_chat:
                    return "send-past"
        
        except Exception as error:
            print("error in check")
            print(error)
            pass
        self.random_sleep(3, 5)
        try:
            messagelabel = driver.find_element_by_xpath(
            "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
        except Exception as error:
            print("error in select message input")
            print(str(error))
            return error

        # selezione label di inseriemto e inserimeto del testo
        self.random_sleep(0.5, 3)
        self.insert_text_action(self.message, messagelabel)
        # for character in self.message:
        #     try:
        #         messagelabel.send_keys(character)
        #     except Exception as error:
        #         print("insert message error")
        #         print(str(error))
        #         return error
        #     self.random_sleep(0.05, 0.2)
        self.random_sleep(1, 4)
        try:
            send_button = driver.find_element_by_xpath(
            "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button")  # selezione pulsante per invio
            send_button.click()  # click sul pulsante
            print("send direct")
        except Exception as error:
            print("send message error")
            print(str(error))
            return error
        return "send"
    
    def get_dir_chat(self, passed_user):
        self.random_sleep(5, 10)
        driver = self.driver
        try:
            driver.get("https://www.instagram.com/direct/new/")
        except Exception as error:
            print("get direct/new/ error")
            print(str(error))
            return False
        self.random_sleep(5, 10)
        try:
            search_user_input = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div[1]/div/div[2]/input")
        except Exception as error:
            print("select user search input error")
            print(str(error))
            return False
        self.random_sleep(1,3)
        self.insert_text_action(passed_user, search_user_input)
        # for character in passed_user:
        #     try:
        #         search_user_input.send_keys(character)
        #     except Exception as error:
        #         print("type user error")
        #         print(str(error))
        #         return False
        #     self.random_sleep(0.1, 0.4)
        self.random_sleep(1, 4)
        try:
            driver.execute_script('''document.querySelector("body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div.Igw0E.IwRSH.eGOV_.vwCYk._3wFWr > div:nth-child(1)").click()''')#document.querySelector("body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div.Igw0E.IwRSH.eGOV_.vwCYk._3wFWr > div:nth-child(1)")
        except Exception as error:
            print("select user error")
            print(str(error))
            return False
        self.random_sleep(2, 5)
        try:
            driver.execute_script('''document.querySelector("body > div.RnEpo.Yx5HN > div > div > div:nth-child(1) > div > div:nth-child(3) > div > button").click()''')
        except Exception as error:
            print("open direct error")
            print(str(error))
            return False
        self.random_sleep(3, 10)
        return True

    def create_group(self, passed_users):
        self.random_sleep(5, 10)
        driver = self.driver
        try:
            driver.get("https://www.instagram.com/direct/new/")#apertura pagina creazione gruppo
        except Exception as error:
            print("get direct/new/ error")
            print(str(error))
            return False
        self.random_sleep(5, 10)
        try:
            search_user_input = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div[1]/div/div[2]/input")
        except Exception as error:
            print("select user search input error")
            print(str(error))
            return False
        self.random_sleep(1,3)
        for passed_user in passed_users:#inserimento utenti
            for character in passed_user:
                try:
                    search_user_input.send_keys(character)
                except Exception as error:
                    print("type user error")
                    print(str(error))
                    return False
                self.random_sleep(0.1, 0.4)
            self.random_sleep(2, 3)
            try:
                driver.execute_script('''document.querySelector("body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div.Igw0E.IwRSH.eGOV_.vwCYk._3wFWr > div:nth-child(1)").click()''')#document.querySelector("body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div.Igw0E.IwRSH.eGOV_.vwCYk._3wFWr > div:nth-child(1)")
            except Exception as error:
                print("select user error")
                print(str(error))
                return False
            self.random_sleep(2, 5)
        
        try:#creazione gruppo
            driver.execute_script('''document.querySelector(".rIacr").click()''')
        except Exception as error:
            print("open direct error")
            print(str(error))
            return False
        self.random_sleep(3, 10)
        return True   
    def send_old(self, passed_user=None, passed_users=None):#questa funzione apre la chat e manda il messaggio
        #ci sono tre tipi di modi per aprire la chat
        if self.bot_version == 1 and passed_user != None:
            try:
                get_chat = self.send_with_account_follow(passed_user)
                if get_chat:
                    print("open chat")
                    pass
                else:
                    return "error"
            except Exception as error:
                print("follow error")
                print(str(error))
                return "error"
        elif self.bot_version == 2 and passed_user != None:
            try:
                get_chat = self.get_dir_chat(passed_user)
                if get_chat:
                    print("open chat")
                    pass
                else:
                    return "error"
            except Exception as error:
                print("get_chat error")
                print(str(error))
                return "error"
        elif self.bot_version == 3 and passed_users != None:
            print(passed_users)
            try:
                get_chat = self.create_group(passed_users)
                if get_chat:
                    print("open chat")
                    pass
                else:
                    return "error"
            except Exception as error:
                print("create group error")
                print(str(error))
                return "error"
        else:
            print(self.bot_version)
            print(passed_users)
            print("wrong bot version")
            return "error"

        

        try:
            send_status = self.send_in_dir()#manda il messaggio nei direct
            if send_status == "send" and self.bot_version !=1:
                return "send"
            elif send_status == "send-past" and self.bot_version !=1:
                return "send-past"
            elif self.bot_version ==1:
                pass
            else:
                print("problem in send_in_dir")
                if send_status:
                    print(str(send_status))
                return "error"
        except Exception as error:
            print("send_in_dir error")
            print(str(error))
            return "error"

        if self.bot_version == 1 and passed_user != None:#se è stato usato il metodo follow e unfollow si discrive dall'utente
            try:
                unfollow = self.send_with_account_unfollow(passed_user)
                if unfollow:
                    return "send"
                else:
                    return "error"
            except Exception as error:
                print("unfollow error")
                print(str(error))
                return "error"
    def send_with_account_follow_old(self, passed_user):
        driver = self.driver
        user = passed_user  # ricevenet
        # apertura profilo ricevente
        try:
            driver.get(f"https://www.instagram.com/{user}")
        except Exception as error:
            print(str(error))
            return False

        self.random_sleep(2, 4)
        try:
            driver.execute_script(
                '''document.querySelector("#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm > div > div > div > span > span.vBF20._1OSdk > button").click()''')
        except Exception as error:
            print(str(error))
            return False
        '''selezione pulsante con javascript e iscrizione al utente'''
        self.random_sleep(5, 15)
        try:
            driver.execute_script(#apertura direct
            '''document.querySelector("#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm.bPdm3 > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > button").click()''')
        except Exception as error:
            print(str(error))
            return False
        return True
        

    def send_with_account_unfollow_old(self, passed_user):
        driver =  self.driver
        user = passed_user
        self.random_sleep(5, 15)
        # ritorna allla pagina del ricevente
        driver.get(f"https://www.instagram.com/{user}")
        self.random_sleep(5, 10)
        try:
            driver.execute_script(
                '''document.querySelector("#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm > div > div:nth-child(2) > div > span > span.vBF20._1OSdk > button").click()''')
            self.random_sleep(4, 8)
            driver.execute_script(
                '''document.querySelector("body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.-Cab_").click()''')
            '''esecuzuione script javascript che si disiscrive dal utente'''
        except Exception as errror:
            print(errror)
            return False
        return True


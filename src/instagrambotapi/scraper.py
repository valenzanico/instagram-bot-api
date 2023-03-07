from string import Template
import json
from selenium.webdriver.common.by import By

class Scraper:
    def __init__(self) -> None:
        super().__init__()
    def scrape_followers(self, username: str,max_f: int,min_f:int = 0 ) -> list:
        driver = self.driver
        scraped_followers = []
        #instagram api endpoint for scraping
        instagram_api_userinfo = Template("view-source:https://www.instagram.com/$username/?__a=1&__d=a")
        instagram_api_followers_start = Template('''view-source:https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={"id":"$insta_id","include_reel":false,"fetch_mutual":false,"first":50}''')
        instagram_api_followers = Template('''view-source:https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={"id":"$insta_id","include_reel":false,"fetch_mutual":false,"first":50,"after":"$end_cursor"}''')

        #esegue un azione che apre le api che forniscono le info riguardo a un utente
        self.execute_action({
            "description": "open instagram user JSON api",
            "command": "get",
            "url": instagram_api_userinfo.substitute(username=username),
            "wait": (3, 5),
        })
        try:#prova a leggere il JSON
            print("loading user id from JSON...")
            driver.page_source
            page_source = driver.find_element(By.TAG_NAME,"pre").text
            insta_id = (json.loads(page_source))["graphql"]["user"]["id"]
        except Exception as error:
            print("error loading user id from JSON")
            print(error)
            raise error
        print(f"user id: {insta_id}")
        
        #url iniziale per scaricare i followers
        instagram_api_followers_url = instagram_api_followers_start.substitute(insta_id=insta_id)
        print("scraping followers...")
        print(len(scraped_followers)) 
        followers_number = max_f + min_f #numero totale di utenti da raccogliere 
        while len(scraped_followers) < followers_number:
                       
            try:
                self.execute_action({#apertura delle api json
                "description": "open instagram followers list JSON api",
                "command": "get",
                "url": instagram_api_followers_url,
                "wait": (2, 3),
                })
                print("loading followers from JSON...")
                #lettura dei dati
                driver.page_source
                page_source = driver.find_element(By.TAG_NAME,"pre").text
                followers = (json.loads(page_source))["data"]["user"]["edge_followed_by"]["edges"]
                for follower in followers:#aggiunta dei followers alla lista se non è un acccount privato
                    if not follower["node"]["is_private"]:
                        scraped_followers.append(follower["node"]["username"])
                print(f"followers scraped: {len(scraped_followers)}")
                
                #lettura delle info ripoettoa alla pagina json
                page_info = (json.loads(page_source))["data"]["user"]["edge_followed_by"]["page_info"]                
                if not page_info["has_next_page"]:#se non c'è un pagina successiva si ferma
                    break
                else:
                    end_cursor = page_info["end_cursor"]#altrimenti salva 'id della pagina successiva
                    instagram_api_followers_url = instagram_api_followers.substitute(insta_id=insta_id, end_cursor=end_cursor)
            except Exception as error:
                print("error loading followers from JSON")
                print(error)
                #in caso di errore se sono gia stati salvati dei follower li ritorna altrimenti causa un errore
                if len(scraped_followers) == 0:
                    raise error
                else:
                    break
        if len(scraped_followers) > min_f:
            #elliminazione dei followers gia letti in precedenza
            scraped_followers = scraped_followers[min_f:]
        self.scraped_followers = scraped_followers#salvataggio dei followers nello stato della classe
        print("scraping followers completed")
        return True
            
            


        
                
            
            


        
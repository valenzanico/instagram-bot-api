from string import Template
import json
from selenium.webdriver.common.by import By
from numpy.random import default_rng
import requests

class Scraper:
    def __init__(self) -> None:
        super().__init__()
    def scrape_followers(self, number:int, cache_time_slice:int = None, *usernames, include_private=False ) -> list:

        driver = self.driver
        scraped_followers = []

        #instagram api endpoint for scraping
        instagram_api_userinfo = Template("view-source:https://www.instagram.com/$username/?__a=1&__d=a")
        instagram_api_followers_start = Template('''view-source:https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={"id":"$insta_id","include_reel":false,"fetch_mutual":false,"first":50}''')
        instagram_api_followers = Template('''view-source:https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={"id":"$insta_id","include_reel":false,"fetch_mutual":false,"first":50,"after":"$end_cursor"}''')
        
        usernames_info = []


        #caricamento follower gia salvati in precedenza
        #nel caso si scelga di usare la cache
        print("loading cache...")
        cache_users = set()

        if self.cache_dir and cache_time_slice:

            for username in self.read_cache("users", cache_time_slice):
                cache_users.add(username)

            if len(cache_users) > 0:
                print("using cache")

            else:
                print("no cache found")
                cache_users = None
        
        else:
            cache_users = None
            
        print(usernames)

        #ottenimento dell'id delle pagine da cui leggere i followers
        for username in usernames:
            #esegue un azione che apre le api che forniscono le info riguardo a un utente
            
            print(username)
            self.execute_action({
            "description": "open instagram user JSON api",
            "command": "get",
            "url": instagram_api_userinfo.substitute(username=username),
            "wait": (2, 3),
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
            
            usernames_info.append({"username": username, "insta_id": insta_id})
            
            print(f"user id: {insta_id}")

        #numero di pagine fonte fornite
        usernames_number_remaining = len(usernames_info)
        
        print(usernames_info)
        print(usernames_number_remaining)
        
        for username in usernames_info:
            if not len(scraped_followers) > number:
                #numero di follower da raggiungere
                users_to_scrape = int((len(scraped_followers)+((number-len(scraped_followers))//usernames_number_remaining)))
            
            else:
                break
            
            #pagina sucessiva delle API da leggere
            #vuota se è la prima pagina
            next_page = None

            print(users_to_scrape)
            print(len(scraped_followers))
            print(usernames_number_remaining)
            print(next_page)
            print(username["username"])

            while len(scraped_followers) < users_to_scrape:
                if not next_page:
                    instagram_api_followers_url = instagram_api_followers_start.substitute(insta_id=username["insta_id"])
                else:
                    instagram_api_followers_url = instagram_api_followers.substitute(insta_id=username["insta_id"], end_cursor=next_page)

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
                    #lettura lista followers
                    followers = (json.loads(page_source))["data"]["user"]["edge_followed_by"]["edges"]
                    
                    for follower in followers:#aggiunta dei followers alla lista se non è un acccount privato
                        follower_username = follower["node"]["username"]
                        
                        #se il follower è gia stato salvato non lo aggiunge
                        if follower_username in scraped_followers:

                            print("già presente")
                            continue

                        #stessa cosa se è presente nella cache
                        if cache_users:
                            print("cache presente")
                            
                            if follower_username in cache_users:
                                print("già presente nella cache")
                                continue
                        
                        #se è privato e non si vogliono includere gli account privati non lo aggiunge
                        if not include_private:
                            if follower["node"]["is_private"]:
                                print("account privato")
                                continue
                        scraped_followers.append(follower_username)
                    
                    #lettura delle info ripoettoa alla pagina json
                    page_info = (json.loads(page_source))["data"]["user"]["edge_followed_by"]["page_info"]                
                    if not page_info["has_next_page"]:#se non c'è un pagina successiva si ferma
                        print("not enough followers")
                        break
                    else:
                        next_page = page_info["end_cursor"]#altrimenti salva 'id della pagina successiva
                        print(next_page)
                    print(len(scraped_followers))
                
                except Exception as error:
                    print("error loading followers from JSON")
                    print(error)
                    #in caso di errore se sono gia stati salvati dei follower li ritorna altrimenti causa un errore
                    if len(scraped_followers) == 0 and usernames_number_remaining == 1:
                        raise error
                    else:
                        break

            
            #il numero di pagine fotne diminuisce dopo essere stato usato
            usernames_number_remaining -= 1

        

        self.scraped_followers = scraped_followers#salvataggio dei followers nello stato della classe
        print("scraping followers completed")
        return True
    

    def shuffle_followers(self):
        #mescola i followers
        if self.scraped_followers:
            random = default_rng()
            random.shuffle(self.scraped_followers)
            return True
        

    def scrape_post_likes(self, post_url):
        scraping_result = []
        cookies = self.session_cookies
        #se non è avvenuto il login ritorna falso
        if not cookies["sessionid"]:

            print("no cookies found")
            return False
        
        #richiesta delle info del post
        headers = {
        'authority': 'www.instagram.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': self.user_agent,
        }
        params = {
            '__a': '1',
            '__d': 'a',
        }
        response = requests.get(post_url, params=params, cookies=cookies, headers=headers)
        
        #ogni media instagram ha un proprio id
        try:
            post_data = response.json()
            media_id = post_data["items"][0]["id"]
        except Exception as error:
            print("Error while getting media id")
            print(error)
            raise error
        print(post_data)
        print(media_id)
        
        #richiesta per ottnere la lista degli utenti che hanno messo like al post
        headers = {
        'authority': 'www.instagram.com',
        'accept': '*/*',
        'accept-language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'referer': post_url,
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': self.user_agent,
        'x-asbd-id': '129477',
        'x-csrftoken': cookies['csrftoken'],
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': 'hmac.AR0urvaNz7ZHH0rSG_l5k1e2CVYFa4zxrcicMx8JUNX11RQH',
        'x-requested-with': 'XMLHttpRequest',
        }
        likers_url = f'https://www.instagram.com/api/v1/media/{media_id}/likers/'
        
        self.random_sleep(2,4)
        response = requests.get(likers_url, headers=headers, cookies=cookies)
        
        try:
            req_json = response.json()
            print(req_json)
            likers = req_json['users']
            print(likers)
        except Exception as error:
            print("Error while getting likers")
            print(error)
            raise error

        for liker in likers:
            scraping_result.append(liker['username'])
        self.scraped_likes = scraping_result
        return True
    
    def scrape_post_meta(self, post_url):
        cookies = self.session_cookies
        #se non è avvenuto il login ritorna falso
        if not cookies["sessionid"]:

            print("no cookies found")
            return False
        
        #richiesta delle info del post
        headers = {
        'authority': 'www.instagram.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': self.user_agent,
        }
        params = {
            '__a': '1',
            '__d': 'a',
        }
        response = requests.get(post_url, params=params, cookies=cookies, headers=headers)
        
        #ogni media instagram ha un proprio id
        try:
            post_data = response.json()
            if post_data:
                print(post_data)
                self.scraped_post_metadata = post_data
                return True
            else:
                return False
        except Exception as error:
            print("Error while getting media id")
            print(error)
            raise error
        
    def scrape_user_meta(self, username):
        instagram_api_userinfo = Template("https://www.instagram.com/$username/")
        cookies = self.session_cookies
        #se non è avvenuto il login ritorna falso
        if not cookies["sessionid"]:

            print("no cookies found")
            return False
        
        #richiesta delle info del post
        headers = {
        'authority': 'www.instagram.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': self.user_agent,
        }
        params = {
            '__a': '1',
            '__d': 'a',
        }
        response = requests.get(instagram_api_userinfo.substitute(username=username), params=params, cookies=cookies, headers=headers)
        
        #ogni media instagram ha un proprio id
        try:
            user_data = response.json()
            if user_data:
                print(user_data)
                self.scraped_user_metadata = user_data
                return True
            else:
                return False
        except Exception as error:
            print("Error while getting media id")
            print(error)
            raise error

        
        
        #url iniziale per scaricare i followers
        # instagram_api_followers_url = instagram_api_followers_start.substitute(insta_id=insta_id)
        # print("scraping followers...")
        # print(len(scraped_followers)) 
        # followers_number = max_f + min_f #numero totale di utenti da raccogliere 
        # while len(scraped_followers) < followers_number:
                       
        #     try:
        #         self.execute_action({#apertura delle api json
        #         "description": "open instagram followers list JSON api",
        #         "command": "get",
        #         "url": instagram_api_followers_url,
        #         "wait": (2, 3),
        #         })
        #         print("loading followers from JSON...")
        #         #lettura dei dati
        #         driver.page_source
        #         page_source = driver.find_element(By.TAG_NAME,"pre").text
        #         followers = (json.loads(page_source))["data"]["user"]["edge_followed_by"]["edges"]
        #         for follower in followers:#aggiunta dei followers alla lista se non è un acccount privato
        #             if not follower["node"]["is_private"]:
        #                 scraped_followers.append(follower["node"]["username"])
        #         print(f"followers scraped: {len(scraped_followers)}")
                
        #         #lettura delle info ripoettoa alla pagina json
        #         page_info = (json.loads(page_source))["data"]["user"]["edge_followed_by"]["page_info"]                
        #         if not page_info["has_next_page"]:#se non c'è un pagina successiva si ferma
        #             break
        #         else:
        #             end_cursor = page_info["end_cursor"]#altrimenti salva 'id della pagina successiva
        #             instagram_api_followers_url = instagram_api_followers.substitute(insta_id=insta_id, end_cursor=end_cursor)
        #     except Exception as error:
        #         print("error loading followers from JSON")
        #         print(error)
        #         #in caso di errore se sono gia stati salvati dei follower li ritorna altrimenti causa un errore
        #         if len(scraped_followers) == 0:
        #             raise error
        #         else:
        #             break
        # scraped_followers_number = len(scraped_followers)
        # if scraped_followers_number > min_f:
        #     #elliminazione dei followers gia letti in precedenza
        #     scraped_followers = scraped_followers[min_f:]
        # if scraped_followers_number > max_f:
        #     #elliminazione dei followers in eccesso
        #     scraped_followers = scraped_followers[:max_f]
        
        # self.scraped_followers = scraped_followers#salvataggio dei followers nello stato della classe
        # print("scraping followers completed")
        # return True
            
        
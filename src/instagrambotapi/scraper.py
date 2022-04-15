import subprocess
import json
import time
import random
import os
from datetime import datetime

def random_sleep(min: float, max: float):
        wait_time = random.uniform(float(min), float(max))
        time.sleep(wait_time)
        print("wait " + str(wait_time))

def get_users_from_like( post, sessionid, count, start_from):
    #questa funzione esegue lo script javascript e raccoglie l'output json
    #output : persone che hanno messo like alla page indicata
    command = f'''/usr/bin/node "/home/eagle/d/myapp/cassinelli/dir-spam-bot/spambot/scrape_post.js" "{post}" "{sessionid}" {count} {start_from}'''
    output = str(subprocess.check_output(command, shell=True)).replace("b'", "").replace("'", "")
    users_dict = json.loads(output)
    return users_dict


def old_pages_scraper(driver, page, req_number=50, start_from=1, export=False):
    first=True
    count_req = 0
    users_raw = []#dict per i dati raw presi dale api
    users= []#dict per i dati selezionati
    next_page = ""#pagina seguente delle api
    users_scraped = 0
    change = 0
    driver.get(f"view-source:https://www.instagram.com/{page}/?__a=1")#get user id
    page_source = driver.page_source
    page_source = driver.find_element_by_tag_name("pre").text
    insta_id = (json.loads(page_source))["graphql"]["user"]["id"]
    req_number= req_number + start_from - 1
    req_number_final = None
    if req_number < 50:#se è mi9nore di 50 esegue solo uan richiesta 
        req_number_final = 1
    else:
        req_number_final = req_number//50#altiemnti calcola il numero di richieste
        change = req_number- (req_number_final*50)
        if change != 0:
            req_number_final+=1
        req_number_orginal = req_number
        req_number = 50
    if start_from==0:
        start_from=1
    for n in range(req_number_final):
        time.sleep(1.3)
        if first:
            print("prima richiesta")
            count_req +=1
            next_page = ""
            driver.get('''view-source:https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={"id":"'''+ insta_id+'''","include_reel":false,"fetch_mutual":false,"first":'''+str(req_number)+'''}''')
            try:
                users_html = driver.page_source
                users_html = driver.find_element_by_tag_name("pre").text
                users_json = (json.loads(users_html))["data"]["user"]["edge_followed_by"]
                for user_raw in users_json["edges"]:
                    users_scraped+=1
                    if users_scraped >= start_from:
                        users_raw.append(user_raw)
                    else:
                        pass
                if users_json["page_info"]["has_next_page"]:
                    next_page = users_json["page_info"]["end_cursor"]
                else:
                    break
                first = False
                print(count_req)
                print(users_scraped)
            except Exception as error:
                print(error)
                print(count_req)
                continue
        elif (req_number_orginal-users_scraped)<=change or ((req_number_orginal-users_scraped)-change)<=5:
            count_req+=1
            print("gestione resto")
            driver.get('''view-source:https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={"id":"'''+ insta_id+'''","include_reel":false,"fetch_mutual":false,"first":'''+str(change)+''',"after":"'''+next_page+'''"}''')
            try:
                users_html = driver.page_source
                users_html = driver.find_element_by_tag_name("pre").text
                users_json = (json.loads(users_html))["data"]["user"]["edge_followed_by"]
                for user_raw in users_json["edges"]:
                    users_scraped+=1
                    if users_scraped >= start_from:
                        users_raw.append(user_raw)
                    else:
                        pass
                if users_json["page_info"]["has_next_page"]:
                    next_page = users_json["page_info"]["end_cursor"]
                else:
                    break
                first = False
                print(count_req)
                print(users_scraped)
            except Exception as error:
                print(error)
                print(count_req)
                continue
        else:
            count_req+=1
            driver.get('''view-source:https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={"id":"'''+ insta_id+'''","include_reel":false,"fetch_mutual":false,"first":50,"after":"'''+next_page+'''"}''')
            try:
                users_html = driver.page_source
                users_html = driver.find_element_by_tag_name("pre").text
                users_json = (json.loads(users_html))["data"]["user"]["edge_followed_by"]
                for user_raw in users_json["edges"]:
                    users_scraped+=1
                    if users_scraped >= start_from:
                        users_raw.append(user_raw)
                    else:
                        pass
                if users_json["page_info"]["has_next_page"]:
                    next_page = users_json["page_info"]["end_cursor"]
                else:
                    break
                first = False
                print(count_req)
                print(users_scraped)
            except Exception as error:
                print(error)
                print(count_req)
                continue
    final_users_list_count = 0
    for user in users_raw:
        user_node = user["node"]
        if not user_node["is_private"]:
            del user_node["profile_pic_url"]
            del user_node["followed_by_viewer"]
            del user_node["requested_by_viewer"]
            del user_node["follows_viewer"]
            users.append(user_node)
            final_users_list_count+=1

    if export:
        try:
            now = datetime.now()
            file_name = now.strftime("%d-%m-%Y-%H-%M-%S.json")
            with open(file_name, "w") as export_file:
                json_export = json.dumps(users)
                export_file.write(json_export)
        except Exception as error:
            print("error during json export:")
            print(error)

    print("parsed user... "+ str(final_users_list_count))
    return users


def pages_scraper(driver, page,req_number=50, start_from=1, export=False):
    first = True
    if req_number < 50:
        req_number = 50
    users = []
    count_req = 0
    next_page = ""
    user_pass = 0
    driver.get(f"view-source:https://www.instagram.com/{page}/?__a=1")#get user id
    page_source = driver.page_source
    page_source = driver.find_element_by_tag_name("pre").text
    insta_id = (json.loads(page_source))["graphql"]["user"]["id"]
    while len(users) < req_number:
        time.sleep(1.3)
        if first:
            print("prima richiesta")
            count_req +=1
            next_page = ""
            driver.get('''view-source:https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={"id":"'''+ insta_id+'''","include_reel":false,"fetch_mutual":false,"first":50}''')
            try:
                users_html = driver.page_source
                users_html = driver.find_element_by_tag_name("pre").text
                users_json = (json.loads(users_html))["data"]["user"]["edge_followed_by"]
                for user_raw in users_json["edges"]:
                    if not user_raw["node"]["is_private"]:
                        if user_pass <= start_from:
                            start_from += 1
                            pass
                        else:
                            user_node = user_raw["node"]
                            del user_node["profile_pic_url"]
                            del user_node["followed_by_viewer"]
                            del user_node["requested_by_viewer"]
                            del user_node["follows_viewer"]
                            users.append(user_node)
                if users_json["page_info"]["has_next_page"]:
                    next_page = users_json["page_info"]["end_cursor"]
                else:
                    break
                first = False
            except Exception as error:
                print(error)
                print(count_req)
                continue

        else:
            count_req+=1
            driver.get('''view-source:https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={"id":"'''+ insta_id+'''","include_reel":false,"fetch_mutual":false,"first":50,"after":"'''+next_page+'''"}''')
            try:
                users_html = driver.page_source
                users_html = driver.find_element_by_tag_name("pre").text
                page_json = json.loads(users_html)
                if "status" in page_json:
                    if page_json["status"] == "fail":
                        print("error, max requests")
                        break

                users_json = (page_json)["data"]["user"]["edge_followed_by"]
                for user_raw in users_json["edges"]:
                    if not user_raw["node"]["is_private"]:
                        if user_pass <= start_from:
                            user_pass += 1
                            pass
                        else:
                            user_node = user_raw["node"]
                            del user_node["profile_pic_url"]
                            del user_node["followed_by_viewer"]
                            del user_node["requested_by_viewer"]
                            del user_node["follows_viewer"]
                            users.append(user_node)
                if users_json["page_info"]["has_next_page"]:
                    next_page = users_json["page_info"]["end_cursor"]
                else:
                    break
                first = False
            except Exception as error:
                print(error)
                if error == "data":
                    time.sleep(2)
                print(count_req)
                continue
        
        print(len(users))
        print(count_req)

    if export:
        try:
            if not os.path.isdir('./logs'):
                os.mkdir("logs")
            now = datetime.now()
            file_name = now.strftime("logs/%d-%m-%Y-%H-%M-%S.json")
            with open(file_name, "w") as export_file:
                json_export = json.dumps(users)
                export_file.write(json_export)
        except Exception as error:
            print("error during json export:")
            print(error)

    return users




if __name__ == "__main__":
    print(get_users_from_like("https://www.instagram.com/p/CJVvrqyFFDM/", "sessionid=33953216539%3AaVkgkaZi49GKAe%3A27", "20", "0"))

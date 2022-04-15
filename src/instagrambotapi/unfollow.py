import json
def unfollow(driver):
    for n in range(10):
        driver.get("view-source:https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5&variables={%22id%22:%2233953216539%22,%22include_reel%22:false,%22fetch_mutual%22:false,%22first%22:%2050}")
        users_html = driver.page_source
        users_html = driver.find_element_by_tag_name("pre").text
        users_json = (json.loads(users_html))["data"]["user"]["edge_followed_by"]
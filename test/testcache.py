import sys
sys.path.insert(1, "")

from instagrambotapi.cache import Cache

cache = Cache()
cache.cache_dir = "cache"

#cache.check_users_cache(4000)
users_set = set({"victor", "paolo", "maroc", "jo"})

# for user in cache.read_cache(60*60*18):
#     users_set = users_set| {user}

with cache.edit_cache("users", 60*60*18) as cache_file:
    for user in users_set:
        cache_file(user)


print(users_set)
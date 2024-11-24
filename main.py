from datetime import datetime

from storage import Storage
from utils import APIClient
from analysis import HashTagAnalyzer

# API Facebook business account token
api_token = 'EAAT9UWWFoQ0BOZB7fzqUuRUJ90QqvbOnBaW6jTTW5TOeVgU0MKfYGs22XWGFv5kCCDvvXoKUNe162jM9tmLxZAOnBImV3CuZCm0wx3UnEZCB7GxINwfNik2KsHJVZA35Jvcjv64NJFhbAyxrioR30x1Aa2ZBqCCrNoPYAgeIu6e7v5JYeLNqL8JJREJLizao0KoBNIZCPHSbOSQsFkZD'
# Instagram business account
instagram_business_account = 17841400907433963
# Hashtags list
hashcodes = """
    ballonsmünchen
    luftballonsmitherz
    luftballonsmünchen
    kinderdekoideen
    kindergeburtstagmünchen
    luftballonsmithelium
    ballonstrauß
    eventdekomünchen
    """

storage = Storage()
client = APIClient(api_token)
hashTagAnalyzer = HashTagAnalyzer(client=client, instagram_business_account=instagram_business_account, storage=storage)

# 1. Load existing database.
storage.load()

# 2. Save time of load data
load_time = datetime.now()
print(f'Loading time: {load_time}')

for hash_tag in hashcodes.split():
    print(f'Loading statistic for hashtag = [{hash_tag}]')
    hashTagAnalyzer.compute_statistic(hash_tag, load_time)

# 3. Store data for further analysis
storage.save()




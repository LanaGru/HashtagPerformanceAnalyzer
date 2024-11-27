import sys
from datetime import datetime

from storage import Storage
from utils import APIClient
from analysis import HashTagAnalyzer

if len(sys.argv) < 2:
    print('Specify token as program parameter e.g.: python main.py <TOKEN>')
    raise ValueError()

# API Facebook business account token
api_token = sys.argv[1]
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

client = APIClient(api_token, read_api_delay=60, pages_num_max=20)  # 20 stands for 500 items
hashTagAnalyzer = HashTagAnalyzer(client=client, instagram_business_account=instagram_business_account, storage=storage)

# 1. Load existing database.
# storage.load()

# 2. Save time of load data
load_time = datetime.now()
print(f'Loading time: {load_time}')

# for hash_tag in hashcodes.split():
#     print(f'Loading statistic for hashtag = [{hash_tag}]')
#     hashTagAnalyzer.compute_statistic(hash_tag, load_time)
#
#     storage.save()

result = hashTagAnalyzer.compute_trends_and_efficiency('storage.csv')

print(result)


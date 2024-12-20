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
hashtages = """
    ballonsmünchen
    luftballonsmitherz
    luftballonsmünchen
    kinderdekoideen
    kindergeburtstagmünchen
    luftballonsmithelium
    ballonstrauß
    eventdekomünchen
    """
target_storage_file = 'storage.csv'

storage = Storage(file_name=target_storage_file)

client = APIClient(api_token, read_api_delay=60, pages_num_max=20)  # 20 stands for 500 items
hashTagAnalyzer = HashTagAnalyzer(client=client, instagram_business_account=instagram_business_account, storage=storage)

# 1. Load existing database.
storage.load()

# 2. Save time of load data
load_time = datetime.now()
print(f'Loading time: {load_time}')

for hashtag in hashtages.split():
    print(f'Loading statistic for hashtag = [{hashtag}]')
    hashTagAnalyzer.compute_statistic(hashtag, load_time)

    storage.save()

result = hashTagAnalyzer.compute_trends_and_efficiency(res_file_path=target_storage_file)

print(result)


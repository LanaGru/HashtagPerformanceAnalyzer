from datetime import datetime

from storage import Storage
from utils import APIClient

client = APIClient(
    'EAAT9UWWFoQ0BOZB7fzqUuRUJ90QqvbOnBaW6jTTW5TOeVgU0MKfYGs22XWGFv5kCCDvvXoKUNe162jM9tmLxZAOnBImV3CuZCm0wx3UnEZCB7GxINwfNik2KsHJVZA35Jvcjv64NJFhbAyxrioR30x1Aa2ZBqCCrNoPYAgeIu6e7v5JYeLNqL8JJREJLizao0KoBNIZCPHSbOSQsFkZD')
instagram_business_account = 17841400907433963

storage = Storage()
# 1. Load existing database.
storage.load()
load_moment = datetime.now()

print(f'Loading time: {load_moment}')

#ballonsmünchen #luftballonsmitherz #luftballonsmünchen #kinderdekoideen #kindergeburtstagmünchen
# luftballonsmithelium
# ballonstrauß
# eventdekomünchen

for tag_id in client.get_hash_tags_ids(instagram_business_account, 'eventdekomünchen'):
    rec = client.get_top_media(instagram_business_account, tag_id)
    for r in rec:
        storage.add(hash_tag='eventdekomünchen', time_add=load_moment, r=r)
        print(r)


#
# storage.add(load_moment, AnalysisResponse(id=2, caption='caption', like_count=1,
#                                           comments_count=12,media_url="http://",
#                                           media_type='IMGAGE', permalink="per", timestamp=datetime.now().isoformat()))
# storage.add(load_moment, AnalysisResponse(id=12, caption='caption', like_count=1,
#                                           comments_count=13,media_url="http://",
#                                           media_type='IMGAGE', permalink="per", timestamp=datetime.now().isoformat()))
storage.save()
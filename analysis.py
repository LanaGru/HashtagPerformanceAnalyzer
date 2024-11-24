from datetime import datetime

from storage import Storage
from utils import APIClient


class HashTagAnalyzer:
    def __init__(self, client: APIClient, instagram_business_account: int, storage: Storage):
        self.client: APIClient = client
        self.instagram_business_account: int = instagram_business_account
        self.storage: Storage = storage

    def compute_statistic(self, hash_tag: str, load_time: datetime):
        for tag_id in self.client.get_hash_tags_ids(self.instagram_business_account, hash_tag):
            rec = self.client.get_top_media(self.instagram_business_account, tag_id)
            for r in rec:
                self.storage.add(hash_tag=hash_tag, time_add=load_time, r=r)
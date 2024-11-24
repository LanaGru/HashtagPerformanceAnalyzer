from datetime import datetime
from dataclasses import dataclass

import requests
import time

@dataclass
class AnalysisResponse:
    id: int = None
    caption: str = None
    like_count: int = None
    comments_count: int = None
    media_url: str = None
    media_type: str = None
    permalink: str = None
    timestamp: str = None

@dataclass
class StorageRecord:
    hash_tag: str = None
    time_record: datetime = None
    row: AnalysisResponse = None



class APIClient:
    def __init__(self, api_key: str, base_url: str = "https://graph.facebook.com/v21.0"):
        self.api_key: str = api_key
        self.base_url: str = base_url

    def get_hash_tags_ids(self, user_id, hash_tag) -> list[str]:
        data = self._read_get_data("ig_hashtag_search", {'user_id': user_id, 'q': hash_tag})
        return [x['id'] for x in data['data']]

    def get_top_media(self, user_id, tag_id) -> list[AnalysisResponse]:
        data = self._read_paged_data(f"{tag_id}/top_media", {'user_id': user_id,
                                                           'fields': 'id,caption,like_count,comments_count,media_url,media_type,permalink,timestamp'})

        return [AnalysisResponse(
            id=x['id'],
            caption=x['caption'],
            like_count=x.get('like_count'),
            comments_count=x['comments_count'],
            media_url=x['media_url'],
            media_type=x['media_type'],
            permalink=x['permalink'],
            timestamp=x['timestamp']
        ) for x in data]

    def get_recent_media(self, user_id, tag_id) -> list[AnalysisResponse]:
        data = self._read_get_data(f"{tag_id}/recent_media", {'user_id': user_id,
                                                              'fields': 'id,caption,like_count,comments_count,media_url,media_type,permalink,timestamp'})
        return [AnalysisResponse(
            id=x['id'],
            caption=x['caption'],
            like_count=0 if x.get('like_count') is None else x.get('like_count'),
            comments_count=x['comments_count'],
            media_url=x['media_url'],
            media_type=x['media_type'],
            permalink=x['permalink'],
            timestamp=x['timestamp']
        ) for x in data['data']]

    # def get_():
    #     "https://graph.facebook.com/v21.0/17843773402049912?fields=id,name&access_token={{fb_token}}"

    def fetch_hashtag_data(self, hashtag):
        url = f"{self.base_url}{hashtag}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise error for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def _read_paged_data(self, address: str, params: dict[str, str], pages_max: int = 4) -> list[dict]:
        ret = []
        pages_loaded = 0
        while True:
            d = self._read_get_data(address, params)
            pages_loaded += 1
            ret.extend(d['data'])
            print(d)
            if pages_loaded < pages_max and 'paging' in d:
                params['after'] = d['paging']['cursors']['after']
                print(f"run next page {params['after']}")
                time.sleep(1)
            else:
                break

        return ret


    def _read_get_data(self, address: str, params: dict[str, str]) -> dict:
        params['access_token'] = self.api_key
        try:
            response = requests.get(f'{self.base_url}/{address}', params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Got error form server: {e.response.text}")

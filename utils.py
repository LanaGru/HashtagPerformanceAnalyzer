import json
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
    def __init__(self, api_key: str, base_url: str = "https://graph.facebook.com/v21.0",
                 read_api_delay: int = 20, pages_num_max: int = 20):
        self.api_key: str = api_key
        self.base_url: str = base_url
        self.read_api_delay: int = read_api_delay
        self.pages_num_max: int = pages_num_max  # 20 =  4 * 5 -- 500 items

    def get_hash_tags_ids(self, user_id, hash_tag) -> list[str]:
        data = self._read_get_data("ig_hashtag_search", {'user_id': user_id, 'q': hash_tag})
        return [x['id'] for x in data['data']]

    def get_top_media(self, user_id, tag_id) -> list[AnalysisResponse]:
        data = self._read_paged_data(f"{tag_id}/top_media", {'user_id': user_id,
                                                           'fields': 'id,caption,like_count,comments_count,media_url,media_type,permalink,timestamp'})

        return [AnalysisResponse(
            id=x['id'],
            caption=x.get('caption'),
            like_count=x.get('like_count'),
            comments_count=x.get('comments_count'),
            media_url=x.get('media_url'),
            media_type=x.get('media_type'),
            permalink=x.get('permalink'),
            timestamp=x.get('timestamp')
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

    def _read_paged_data(self, address: str, params: dict[str, str], pages_max_p: int = None) -> list[dict]:
        ret = []
        pages_loaded = 0
        pages_max = self.pages_num_max if pages_max_p is None else pages_max_p
        while True:
            d = self._read_get_data(address, params)
            pages_loaded += 1
            ret.extend(d['data'])
            if pages_loaded < pages_max and 'paging' in d:
                params['after'] = d['paging']['cursors']['after']
                print(f"run next page {params['after']}")
            else:
                break

        return ret

    def _flush_to_file(self, address: str, params: dict, body: dict, headers: dict):
        def _ser_dict(d: dict):
            return '\n'.join([f'{k}={v}' for (k, v) in d.items()])
        with open("api-client.log", 'a+t') as api_client_log:
            if api_client_log:
                api_client_log.write(f'<query time="{datetime.now()}" address="{address}">\n')

                api_client_log.write(f'\t<params>\n')
                api_client_log.write(f'\t{_ser_dict(params)}\n')
                api_client_log.write(f'\t</params>\n')

                api_client_log.write(f'\t<headers>\n')
                api_client_log.write(f'\t{_ser_dict(headers)}\n')
                api_client_log.write(f'\t</headers>\n')

                api_client_log.write(f'\t')
                api_client_log.write(json.dumps(body))

                api_client_log.write("\n</query>\n")

    def _read_get_data(self, address: str, params: dict[str, str]) -> dict:
        params['access_token'] = self.api_key
        try:
            time.sleep(self.read_api_delay)
            response = requests.get(f'{self.base_url}/{address}', params=params)

            ret_val = response.json()
            self._flush_to_file(address, params, ret_val, response.headers)

            response.raise_for_status()
            return ret_val
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Got error form server: {e.response.text}")

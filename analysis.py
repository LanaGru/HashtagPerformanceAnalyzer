from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
from storage import Storage
from utils import APIClient


class HashTagAnalyzer:
    def __init__(self, client: APIClient, instagram_business_account: int, storage: Storage):
        self.client: APIClient = client
        self.instagram_business_account: int = instagram_business_account
        self.storage: Storage = storage

    @staticmethod
    def _compute_stats(df: pd.DataFrame) -> pd.DataFrame:
        if 'file' not in df.columns:
            df['file'] = '_'

        ret_val = df.groupby(['file', 'hash_tag', 'time_add']).agg(
            record_count=('record_id', 'count'),
            like_avg=('like_count', 'mean'),
            comment_avg=('comments_count', 'mean')
        ).reset_index()
        return ret_val.sort_values(['file', 'hash_tag', 'time_add'])

    @staticmethod
    def _draw_chart(df: pd.DataFrame):
        groups = df.groupby('hash_tag')
        plt.figure(figsize=(10, 6))

        for name, group in groups:
            group = group.sort_values(by='time_add')
            plt.plot(group['time_add'], group['rank'], marker='o', label=name)

        plt.xlabel('Time')
        plt.ylabel('Rank')
        plt.title('Rank over time for each group')
        plt.legend(title='hash_tag')
        plt.grid(True)

        plt.savefig('result.png', format='png', dpi=300, bbox_inches='tight')

    @staticmethod
    def _hash_tag_category(like: int, comments: int, posts: int) -> str:
        if like > 1000 or comments > 100 or posts > 10_000:
            return 'hight-effective'
        if (200 <= like <= 1000) or (20 <= comments <= 100) or (1000 <= posts <= 10_000):
            return 'mid-effective'
        if like < 200 or comments < 20 or posts < 1_000:
            return 'low-effective'

    @staticmethod
    def _trends_efficiency(df: pd.DataFrame):
        grouped = df.groupby('hash_tag')

        results = []
        for name, group in grouped:
            group = group.sort_values(by='time_add')

            first = group.iloc[0]
            last = group.iloc[-1]

            rank_diff = last['rank'] - first['rank']
            time_diff = (last['time_add'] - first['time_add']).total_seconds() / 60
            slope = rank_diff / time_diff if time_diff != 0 else float('inf')

            efficiency = HashTagAnalyzer._hash_tag_category(last['like_avg'], last['comment_avg'], last['record_count'])
            results.append({'hash_tag': name, 'rank': last['rank'], 'trends': slope * 100, 'efficiency': efficiency})

        return pd.DataFrame(results)

    def compute_statistic(self, hash_tag: str, load_time: datetime):
        for tag_id in self.client.get_hash_tags_ids(self.instagram_business_account, hash_tag):
            rec = self.client.get_top_media(self.instagram_business_account, tag_id)
            for r in rec:
                self.storage.add(hash_tag=hash_tag, time_add=load_time, r=r)

    def compute_trends_and_efficiency(self, res_file_path: str) -> pd.DataFrame:
        df = pd.read_csv(res_file_path, sep='\t', dtype=str)
        df['like_count'] = df['like_count'].fillna('0')
        df['like_count'] = df['like_count'].astype(int)
        df['comments_count'] = df['comments_count'].astype(int)

        result = HashTagAnalyzer._compute_stats(df).sort_values(['hash_tag', 'time_add'])

        result['rank'] = 1 * result['record_count'] + 0.8 * result['like_avg'] + 50 * result['comment_avg']

        result['time_add'] = pd.to_datetime(result['time_add'])
        HashTagAnalyzer._draw_chart(result)

        return HashTagAnalyzer._trends_efficiency(result).sort_values('rank', ascending=False)


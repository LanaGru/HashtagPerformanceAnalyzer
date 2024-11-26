import os.path
from datetime import datetime
import shutil

from utils import StorageRecord, AnalysisResponse

class Storage:
    def __init__(self):
        self.storage: list[StorageRecord] = []

    def add(self, hash_tag: str, time_add: datetime, r: AnalysisResponse):
        self.storage.append(StorageRecord(time_record=time_add, hash_tag=hash_tag, row=r))

    def load(self):
        if not os.path.exists('storage.csv'):
            print('File database does not exist')
            return
        else:
            shutil.copy('storage.csv', f'storage-{datetime.now().isoformat().replace(" ", "_")}.bkp')

        row_num = 0
        with open('storage.csv', 'r') as f:
            for line in f:
                row_num += 1
                if row_num == 1:
                    continue # skip first row
                cells = line.strip().split("\t")
                response = AnalysisResponse(
                    id=int(cells[2]),
                    caption=cells[3],
                    like_count=int(cells[4]) if cells[4] else 0,
                    comments_count=int(cells[5]),
                    media_url=cells[6],
                    media_type=cells[7],
                    permalink=cells[8],
                    timestamp=cells[9]
                )
                record = StorageRecord(
                    hash_tag=cells[0],
                    time_record=datetime.strptime(cells[1], '%Y-%m-%d %H:%M:%S'),
                    row=response
                )

                self.storage.append(record)
        print(f"Loaded {len(self.storage)} items")

    def save(self):
        with open('storage.csv', 'wt') as f:
            f.write(f'hash_tag\ttime_add\trecord_id\tcaption\tlike_count\tcomments_count\tmedia_url'
                        f'\tmedia_type\tpermalink\ttimestamp\n')
            for s in self.storage:
                time_add: str = s.time_record.strftime('%Y-%m-%d %H:%M:%S')
                record = s.row
                text = record.caption.replace("\n", "")

                r = '\t'.join([f'{x}' if x is not None else '' for x in [s.hash_tag, time_add, record.id, text, record.like_count,
                                       record.comments_count, record.media_url, record.media_type,
                                       record.permalink, record.timestamp
                                       ]])
                f.write(f'{r}\n')
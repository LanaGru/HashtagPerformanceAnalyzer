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
                    like_count=int(cells[4]),
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
                f.write(f'{s.hash_tag}\t{time_add}\t{record.id}\t{text}\t{record.like_count}\t{record.comments_count}\t{record.media_url}'
                        f'\t{record.media_type}\t{record.permalink}\t{record.timestamp}\n')
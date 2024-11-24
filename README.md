# Hash Tag Performance Analyzer project
This project uses Facebook Graph API for reading information related to hashtags. To read hashtag information we use endpoints:
1. To read codes for given hashtag we use `GET /ig_hashtag_search` -- https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-hashtag-search
1. For further engagement analisys we use `GET /<ig_hashtag>/top-media` -- https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-hashtag/top-media

## Algorithm description

1. Let `H` be a list of the hashtags. For each `h` from `H`:
  - Save `time_add = now()`
  - Fetch vector `(L, C, P)` for max `max_load_media` topmost medias for given hashtag `h` using endpoint `/<ig_hashtag>/top-media`, where `L` - number of likes, `C` - number of comments, `P` - number of media that referes hashtag `h`: `min(number_of_loaded_media, max_load_media)`. We use max_load_media = 100 to limit load on Facebook API. In future we can increase this parmeter.
  - compute average values `(L, C, P)` over all loaded medias for given `time_add` and `h`
2. doing operations above for each day we will get for each `time_add` and `h` triple `(avg(L), avg(C), avg(P))` that can be treated as value `(L, C, P)` for every date.
3. compute weighted function `F(h, date, L, C, P)`
4. For each hastag `h` compute its effectiveness between dates $d_1 < d_2$ by formula using derivatives:
```math
  E(h) = \frac{F_{d_2}(L, C, P) - F_{d_1}(L, C, P)}{d_2 - d_1}
```

Our assumption is that the number of likes $L$, comments $C$, and the number of pages $P$ are parameters of a weighted linear function `F`, which is _implicitly_ proportional to the engagement value.

```math
F(L, C, P) = w_1 L + w_2  C + w_3  P
```

The weights of these parameters, `w_i`, can be determined later during statistical analysis.

# How to run
## Activate venv:

```python -m venv venv```
## Install dependencies
```pip install -r requirements.txt```

## Run script
```python main.py <FACEBOOK_TOKEN>```

This programm will read information from API and stores all rows `storage.csv` file. Each run of programm will **add** records with `time_add=now()` column value to the end of file.
Previous verion of file will be backed up with timestamp and `.bkp` extension.

# Storage file format
|column name| type | description|
|--------|---|------|
|hash_tag|str|Name of hashtag|
|time_add|datetime|When the row is generated (moment of data fetch)|
|record_id|int| Facebook API record indentifier |
|record_id|int| Facebook API record indentifier |
|caption| str | Text of top-media record |
|like_count| int | number of likes |
|comments_count| int | number of comments  |
|comments_count| int | number of comments  |
|media_url|str | URL of media |
|media_type|str | type of the media |
|permalink| str | permanent link to page | 
|timestamp | datetime | date and time when post was created |

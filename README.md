# Hash Tag Performance Analyzer project
This project uses Facebook Graph API for reading information related to hashtags. To read hashtag information we use endpoints:
1. To read codes for given hashtag we use `GET /ig_hashtag_search` -- https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-hashtag-search
1. For further engagement analisys we use `GET /<ig_hashtag>/top-media` -- https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-hashtag/top-media

Our assumption is that the number of likes `(L)`, comments `(C)`, and the number of pages `(P)` that can be fetched using 
`GET /<ig_hashtag>/top-media` are parameters of a weighted linear function `F`, which is indirectly proportional to the engagement value.

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

This programm will read information and store all `storage.csv` file. You can analise it using Excel or similar software.

# Result file format
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

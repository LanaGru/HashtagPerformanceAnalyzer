from utils import APIClient


def main():
    api_key = "EAAT9UWWFoQ0BO0zAVqoRbMkJw8IHXFO2tZAn0As059TppM6hrBssU37dd3poD9kU2TZAeSmKR63ApJ1FTeH0jCmc7ssYgKj83ANBf47GsPf18sUZAC88BhsH88emMrkCtsgJCZAdNWEVGeodMg3plZBKkcZBNtJ9XAzZBAbDSFiVc4b84ryFold8wjAjeATftr6wZC2kTLWRAHz2jBIZD"
    user_id = '10235331938303665'
    account='331485113866425'
    instagram_business_account = '17841400907433963'
    hashtags = ["#Python", "#Coding", "#DataScience"]
    "https://graph.facebook.com/v21.0/me?access_token={{fb_token}}"
    {
        "name": "Lana Grunskaya",
        "id": "10235331938303665"
    }

    "https://graph.facebook.com/v21.0/me/accounts?access_token={{fb_token}}"
    {
        "access_token": "EAAT9UWWFoQ0BO7GSNNhMQEanoWAYj091fKfbtFbOvYbV2TrS074jkihZAaiR9gYjqo0YH0uqXY4ZBDVJ2u0HQMQ1qVVhMtKKPmWYkZCAxClG7HS5VjerwElcvR7TGhb79CGzI4Fu98TMTZAlmnttY2hyHdbvFlThScLVpaKUl0reVC9lcuK7KZAl7adTr5C1186RoCDYdibtLbxOF0nOTyQZDZD",
        "category": "Одежда (бренд)",
        "category_list": [
            {
                "id": "2209",
                "name": "Одежда (бренд)"
            }
        ],
        "name": "Вязаный трикотаж",
        "id": "331485113866425",
        "tasks": [
            "ADVERTISE",
            "ANALYZE",
            "CREATE_CONTENT",
            "MESSAGING",
            "MODERATE",
            "MANAGE"
        ]
    }

    "https://graph.facebook.com/v21.0/331485113866425?fields=instagram_business_account&access_token={{fb_token}}"
    {
        "instagram_business_account": {
            "id": "17841400907433963"
        },
        "id": "331485113866425"
    }

    "https://graph.facebook.com/v21.0/ig_hashtag_search?user_id=17841400907433963&access_token={{fb_token}}&q=pacan"
    "https://graph.facebook.com/v21.0/17841400907433963/recently_searched_hashtags?access_token={{fb_token}}"
    "https://graph.facebook.com/v21.0/17843773402049912/top_media?user_id=17841400907433963&fields=id,caption,like_count,comments_count&access_token={{fb_token}}"
    "https://graph.facebook.com/v21.0/17843773402049912?fields=id,name&access_token={{fb_token}}"



    api_client = APIClient(api_key)
    data_storage = DataStorage("data.json", "data.csv")
    data_analyzer = DataAnalyzer("data.json")

    for hashtag in hashtags:
        data = api_client.fetch_hashtag_data(hashtag)
        if data:
            data_storage.save_to_json(data)
            data_storage.save_to_csv(data)

    avg_engagement = data_analyzer.calculate_average_engagement()
    print(f"Average Engagement Rate: {avg_engagement:.2f}")

if name == "main":
    main()
import tweepy
from decouple import config
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

def post_tweet(text:str, image_path:list[str]):
    """_summary_

    Args:
        text (str): _description_
        image_path (list[str]): _description_"""
    
    consumer_key = config('consumer_key')
    consumer_secret = config('consumer_secret')
    access_token = config('access_token')
    access_token_secret = config('access_token_secret')
    bearer_token = config('bearer_token')
    try:
        auth = tweepy.OAuth1UserHandler(
            consumer_key, consumer_secret
        )
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)
        media_id = api.media_upload(image_path).media_id_string
        # for i in range(len(image_path)):
            # print(media_id)
        # print(media_id)
        r = client.create_tweet(text=text, media_ids=[media_id])
        print(r)
    except Exception as e:
        print(e)


def post_country_risk_plot():
    post_tweet(text=f'Riesgo País el día: {today}', image_path=['./images/rp.png'])


def post_bm_plot():
    post_tweet(text=f'Base monetaria y Circulante Monetario al día: {today}', image_path=['./images/bm.png'])


def post_tna_plot():
    post_tweet(text=f'TNA al día: {today}', image_path=['./images/tna.png'])


def post_inflacion_plot():
    post_tweet(text=f'Inflación al día: {today}', image_path=['./images/inflacion.png'])
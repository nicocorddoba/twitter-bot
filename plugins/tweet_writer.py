import tweepy
from decouple import config
from datetime import datetime
import os

today = datetime.today().strftime('%d-%m-%Y')

def post_tweet(text:str, image_path:str):
    """Writtes a tweet with the text, uploads an image and posts it

    Args:
        text (str): the text of the tweet
        image_path (str): the image that will be uploaded """

    # Credentials
    consumer_key = config('consumer_key')
    consumer_secret = config('consumer_secret')
    access_token = config('access_token')
    access_token_secret = config('access_token_secret')
    bearer_token = config('bearer_token')
    
    try:
        # Authentication for API
        auth = tweepy.OAuth1UserHandler(
            consumer_key, consumer_secret
        )
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)
        media_id = api.media_upload(image_path).media_id_string
        
        # Upload Image
        r = client.create_tweet(text=text, media_ids=[media_id])
        print(r['id'])
    except Exception as e:
        raise('Error:', e)


def post_country_risk_plot():
    post_tweet(text=f'Riesgo País al día: {today}', image_path='./images/rp.png')


def post_bm_plot():
    post_tweet(text=f'Base Monetaria y Circulación Monetaria al día: {today}', image_path='./images/bm.png')


def post_tna_plot():
    post_tweet(text=f'TNA al día: {today}', image_path='./images/tna.png')


def post_inflacion_plot():
    post_tweet(text=f'Inflación al día: {today}', image_path='./images/inflacion.png')
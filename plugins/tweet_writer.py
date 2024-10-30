import tweepy
from decouple import config
from datetime import datetime
import os

today = datetime.today()
todaystr = today.strftime('%d-%m-%Y')

mes = {1: 'Diciembre', 2: 'Enero', 3: 'Febrero', 4: 'Marzo', 5: 'Abril', 6: 'Mayo', 7: 'Junio', 8: 'Julio', 9: 'Agosto', 10: 'Septiembre', 11: 'Octubre', 12: 'Noviembre'}

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
        print(r)
    except Exception as e:
        raise('Error:', e)


def post_country_risk_plot(fecha:str):
    fecha_dt = datetime.strptime(fecha, '%d-%m-%Y')
    valor_desde = (today - fecha_dt).days / 365
    tweet = f"Riesgo país el día {todaystr}. {'El valor más bajo desde '+ fecha if valor_desde > 0.5 else ''}"
    post_tweet(text=tweet, image_path='./images/rp.png')


def post_bm_plot():
    post_tweet(text=f'Base Monetaria y Circulación Monetaria al día: {todaystr}', image_path='./images/bm.png')


def post_tna_plot():
    post_tweet(text=f'TNA al día: {todaystr}', image_path='./images/tna.png')


def post_inflacion_plot():
    post_tweet(text=f'Inflación del mes de {mes[today.month]}', image_path='./images/inflacion.png')
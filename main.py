import tweepy
from decouple import config

consumer_key = config('consumer_key')
consumer_secret = config('consumer_secret')
access_token = config('access_token')
access_token_secret = config('access_token_secret')
bearer_token = config('bearer_token')
TEXT='Este es un tweet de prueba'


auth = tweepy.OAuth1UserHandler(
   consumer_key, consumer_secret
)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)
media_id = api.media_upload('./imagen.png').media_id_string
print(media_id)
r = client.create_tweet(text=TEXT, media_ids=[media_id])
print(r)
# r = client.create_tweet(text=TEXT)
# print(r.json())